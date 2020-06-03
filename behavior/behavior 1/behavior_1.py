import numpy as np
import threading

from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine

from stimulus import Stimulus
from statemachine import StateMachineBuilder
from probability import ProbabilityConstuctor
from rotaryencoder import BpodRotaryEncoder
import settings

#debugging
# 83, 34,

bpod=Bpod()

# rotary encoder config
rotary_encoder_module = BpodRotaryEncoder('COM4', settings)
rotary_encoder_module.load_message(bpod)
rotary_encoder_module.configure()

# softcode handler
def softcode_handler(data):
    if data == settings.SC_PRESENT_STIM:
        stimulus_game.present_stimulus()
    elif data == settings.SC_START_OPEN_LOOP:
        stimulus_game.start_open_loop()
    elif data == settings.SC_STOP_OPEN_LOOP:
        stimulus_game.stop_open_loop()
    elif data == settings.SC_END_PRESENT_STIM:
        stimulus_game.end_present_stimulus()
        print("sc 4")
    # for debugging#================================================================================
    elif data == 5:
        print("wheel not stopping")
    elif data == 6:
        print("stop open loop fail")
        stimulus_game.stop_open_loop()
bpod.softcode_handler_function = softcode_handler

#stimulus
stimulus_game = Stimulus(settings, rotary_encoder_module)


#probability constructor
probability_object = ProbabilityConstuctor(settings)
probability_list = probability_object.probability_list

# state machine configs
TRIAL_NUM = 0
for block in settings.BLOCKS:
    TRIAL_NUM += block[settings.TRIAL_NUM_BLOCK]

def trial():
    for trial in range(TRIAL_NUM):
        probability_dict = probability_list[trial]
        sma = StateMachine(bpod)
        # define states
        sma.add_state(
            state_name="start1",
            state_timer=settings.TIME_START,
            state_change_conditions={"Tup": "reset_rotary_encoder_wheel_stopping_check"},
            output_actions=[],
        )
        # reset rotary encoder bevore checking for wheel not stoping
        sma.add_state(
            state_name="reset_rotary_encoder_wheel_stopping_check",
            state_timer=0,
            state_change_conditions={"Tup":"wheel_stopping_check"},
            output_actions=[("Serial1", settings.RESET_ROTARY_ENCODER)], # activate white light while waiting
        )
        #wheel not stoping check
        sma.add_state(
            state_name="wheel_stopping_check",
            state_timer=settings.TIME_WHEEL_STOPPING_CHECK,
            state_change_conditions={
                    "Tup":"present_stim",
                    settings.THRESH_LEFT:"wheel_stopping_check_failed_punish",
                    settings.THRESH_RIGHT:"wheel_stopping_check_failed_punish",
                    },
            output_actions=[],
        )
        sma.add_state(
            state_name="wheel_stopping_check_failed_punish",
            state_timer=settings.TIME_WHEEL_STOPPING_PUNISH,
            state_change_conditions={"Tup":"start1"},
            #output_actions=[]
            output_actions=[("SoftCode", 5)], #================================================================================
        )

        # ==========================================
        # continue if wheel stopped for time x
        sma.add_state(
            state_name="present_stim",
            state_timer=settings.TIME_PRESENT_STIM,
            state_change_conditions={"Tup": "reset_rotary_encoder_open_loop"},
            output_actions=[("SoftCode", settings.SC_PRESENT_STIM)],#after wait -> present initial stimulus
        )
        # reset rotary encoder bevor open loop starts
        sma.add_state(
            state_name="reset_rotary_encoder_open_loop",
            state_timer=0,
            state_change_conditions={"Tup": "open_loop"},
            output_actions=[("Serial1", settings.RESET_ROTARY_ENCODER),
                            ("SoftCode", settings.SC_START_OPEN_LOOP)
                            ], # reset rotary encoder postition to 0
        )
        # open loop detection
        sma.add_state(
            state_name="open_loop",
            state_timer=settings.TIME_OPEN_LOOP,
            state_change_conditions={
                "Tup": "stop_open_loop_fail",
                settings.STIMULUS_LEFT: "stop_open_loop_reward_left",
                settings.STIMULUS_RIGHT: "stop_open_loop_reward_right",
                },
            output_actions=[],
        )
        #============================================
        # stop open loop fail
        sma.add_state(
            state_name="stop_open_loop_fail",
            state_timer=0,
            state_change_conditions={"Tup": "open_loop_fail_punish"},
            #output_actions=[("SoftCode", settings.SC_STOP_OPEN_LOOP)] # stop open loop in py game
            output_actions=[("SoftCode", 6)]#================================================================================
        )
        # open loop fail punish time & exit trial
        sma.add_state(
            state_name="open_loop_fail_punish",
            state_timer=settings.TIME_OPEN_LOOP_FAIL_PUNISH,
            state_change_conditions={"Tup": "exit"},
            output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM)]
        )

        #=========================================================================================
        # reward left
        sma.add_state(
            state_name="stop_open_loop_reward_left",
            state_timer=settings.TIME_STIM_FREEZ,
            state_change_conditions={"Tup": "reward_left"},
            output_actions=[("SoftCode", settings.SC_STOP_OPEN_LOOP)] # stop open loop in py game
        )

        # check for gmble side:
        if probability_dict["gambl_left"]:
            # check for probability of big reard
            if probability_dict["gambl_reward"]:
                # big rewaerd
                sma.add_state(
                    state_name="reward_left",
                    state_timer=settings.BIG_REWARD_TIME,
                    state_change_conditions={"Tup": "reward_left_waiting"},
                    output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM),
                                    ("Valve1", 255)
                                    ]
                )
                sma.add_state(
                    state_name="reward_left_waiting",
                    state_timer=settings.big_reward_waiting_time,
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[]
                )
            else:
                # no reward
                sma.add_state(
                    state_name="reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "reward_left_waiting"},
                    output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM)],
                )
                sma.add_state(
                    state_name="reward_left_waiting",
                    state_timer=settings.REWARD_TIME,
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[]
                )
        elif probability_dict["safe_reward"]:
            # small reward
            sma.add_state(
                state_name="reward_left",
                state_timer=settings.SMALL_REWARD_TIME,
                state_change_conditions={"Tup": "reward_left_waiting"},
                output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM),
                                ("Valve1", 255)
                                ]
            )
            sma.add_state(
                state_name="reward_left_waiting",
                state_timer=settings.small_reward_waiting_time,
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[]
            )
        else:
            # no reward
            sma.add_state(
                state_name="reward_left",
                state_timer=0,
                state_change_conditions={"Tup": "reward_left_waiting"},
                output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM)]
            )
            sma.add_state(
                state_name="reward_left_waiting",
                state_timer=settings.REWARD_TIME,
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[]
            )

        #=========================================================================================
        # reward right
        sma.add_state(
            state_name="stop_open_loop_reward_right",
            state_timer=settings.TIME_STIM_FREEZ,
            state_change_conditions={"Tup": "reward_right"},
            output_actions=[("SoftCode", settings.SC_STOP_OPEN_LOOP)] # stop open loop in py game
        )

        # check for gmble side:
        if not probability_dict["gambl_left"]:
            # check for probability of big reard
            if probability_dict["gambl_reward"]:
                # big rewaerd
                sma.add_state(
                    state_name="reward_right",
                    state_timer=settings.BIG_REWARD_TIME,
                    state_change_conditions={"Tup": "reward_right_waiting"},
                    output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM),
                                    ("Valve1", 255)
                                    ]
                )
                sma.add_state(
                    state_name="reward_right_waiting",
                    state_timer=settings.big_reward_waiting_time,
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[]
                )
            else:
                # no reward
                sma.add_state(
                    state_name="reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "reward_right_waiting"},
                    output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM)],
                )
                sma.add_state(
                    state_name="reward_right_waiting",
                    state_timer=settings.REWARD_TIME,
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[]
                )
        elif probability_dict["safe_reward"]:
            # small reward
            sma.add_state(
                state_name="reward_right",
                state_timer=settings.SMALL_REWARD_TIME,
                state_change_conditions={"Tup": "reward_right_waiting"},
                output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM),
                                ("Valve1", 255)
                                ]
            )
            sma.add_state(
                state_name="reward_right_waiting",
                state_timer=settings.small_reward_waiting_time,
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[]
            )
        else:
            # no reward
            sma.add_state(
                state_name="reward_right",
                state_timer=0,
                state_change_conditions={"Tup": "reward_right_waiting"},
                output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM)]
            )
            sma.add_state(
                state_name="reward_right_waiting",
                state_timer=settings.REWARD_TIME,
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[]
            )

        # inter trial time
        sma.add_state(
            state_name="inter_trial",
            state_timer=settings.INTER_TRIAL_TIME,
            state_change_conditions={"Tup": "exit"},
            output_actions=[]
        )

        bpod.send_state_machine(sma)
        # Run state machine
        if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
            break
        print(f"trial: {trial} \n probability: {probability_dict} \n")

#==========================================================================================================
t1 = threading.Thread(target=stimulus_game.run_game)
t1.start()

t2 = threading.Thread(target=trial)
t2.start()
t2.join()
print("finished")

rotary_encoder_module.close()
bpod.close()
