"""PyBpod Gambl Task - Training Environment

main behavior file for pybpod gui
load this file via the pybpod gui as a protocol

The gambl tasks is designed for headfixed mice with three screens. The mouse can move a stimulus image or gif
from the center screen to eather the right or left screen via a wheel. Depending on the conditions the mouse
will get a reward of defined amount if chosen the correct side.

This behavior config file makes use of three PyBpod classes the main Bpod and the StateMachine aswell as the RotaryEncoder.

In addition it uses three custom classes:
    Stimulus: handeling the pygames configuration and drawing of the stimulus on the screens
    ProbabilityConstructor: generating the necessary probabilites for each trial
    BpodRotaryEncoder: handeling the rotary encoder and reading the position
    TrialParameterHandler: generating the necessary parameters for each session from the user input and predefined parameters

"""

import threading
import os,sys,inspect
import json

# import pybpod modules
from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpodgui_api.models.session import Session

# add module path to sys path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir = (os.path.dirname(os.path.dirname(currentdir)))
if os.path.isdir(os.path.join(dir,"modules")):
    maxland_root = dir
else:
    maxland_root = os.path.dirname(dir)
modules_dir = os.path.join(maxland_root,"modules")
sys.path.insert(-1,modules_dir) 

# import custom modules
from stimulus_gamble import Stimulus
from probability_gamble import ProbabilityConstuctor
from rotaryencoder import BpodRotaryEncoder
from parameter_handler import TrialParameterHandler
from userinput import UserInput

# import usersettings
import usersettings

# create settings object
session_folder = os.getcwd()
settings_folder = currentdir #os.path.join(session_folder.split('experiments')[0],"tasks","gamble_task_recording")
settings_obj = TrialParameterHandler(usersettings, settings_folder, session_folder)

# create bpod object
bpod=Bpod('COM7')

# create tkinter userinput dialoge window
window = UserInput(settings_obj)
window.draw_window_bevore_gamble()
window.show_window()
window.update_settings() 

# create multiprocessing variabls
# flags
display_stim_event = threading.Event()
start_open_loop_event = threading.Event()
still_show_event = threading.Event()
display_stim_event.clear()
start_open_loop_event.clear()
still_show_event.clear()

# run session
if settings_obj.run_session:
    settings_obj.update_userinput_file_gamble()
    # rotary encoder config
    # enable thresholds
    rotary_encoder_module = BpodRotaryEncoder('COM6', settings_obj, bpod)
    rotary_encoder_module.load_message()
    rotary_encoder_module.configure()
    #rotary_encoder_module.enable_stream()

    # softcode handler
    def softcode_handler(data):
        if data == settings_obj.SC_PRESENT_STIM:
            display_stim_event.set()
            print("PRESENT STIMULUS")
        elif data == settings_obj.SC_START_OPEN_LOOP:
            start_open_loop_event.set()
            print("START OPEN LOOP")
        elif data == settings_obj.SC_STOP_OPEN_LOOP:
            stimulus_game.stop_open_loop()
            print("stop open loop")
        elif data == settings_obj.SC_END_PRESENT_STIM:
            still_show_event.set()
            print("end present stim")
        elif data == settings_obj.SC_START_LOGGING:
            rotary_encoder_module.rotary_encoder.enable_logging()
            #rotary_encoder_module.enable_logging()
            print("enable logging")
        elif data == settings_obj.SC_END_LOGGING:
            #rotary_encoder_module.disable_logging()
            rotary_encoder_module.rotary_encoder.disable_logging()
            print("disable logging")

    bpod.softcode_handler_function = softcode_handler

    #stimulus
    stimulus_game = Stimulus(settings_obj, rotary_encoder_module)

    #probability constructor
    probability_obj = ProbabilityConstuctor(settings_obj)
    # update settings object
    #settings_obj.probability_list = probability_obj.probability_list
    #settings_obj.trial_num = probability_obj.trial_num


    # create main state machine aka trial loop ====================================================================
    # state machine configs
    for trial in range(settings_obj.trial_num):
        #variables to print summary
        probability_dict = settings_obj.probability_list[trial]
        sma = StateMachine(bpod)
        # define states
        # start state to define block of trial
        sma.add_state(
            state_name="start",
            state_timer=settings_obj.time_dict["time_start"],
            state_change_conditions={"Tup": "sync_state_1"},
            output_actions=[("SoftCode", settings_obj.SC_START_LOGGING),
                            ('BNC1',1),('BNC2',1)
                            ],
        )
        sma.add_state(
            state_name="sync_state_1",
            state_timer=0,
            state_change_conditions={"Tup": "reset_rotary_encoder_wheel_stopping_check"},
            output_actions=[('BNC1',0),('BNC2',0)],
        )
        # reset rotary encoder bevore checking for wheel not stoping
        sma.add_state(
            state_name="reset_rotary_encoder_wheel_stopping_check",
            state_timer=0,
            state_change_conditions={"Tup":"wheel_stopping_check"},
            output_actions=[("Serial1", settings_obj.RESET_ROTARY_ENCODER),
                            ('BNC1',0),('BNC2',1)
                            ], # activate white light while waiting
        )
        #wheel not stoping check
        sma.add_state(
            state_name="wheel_stopping_check",
            state_timer=settings_obj.time_dict["time_wheel_stopping_check"],
            state_change_conditions={
                    "Tup":"present_stim",
                    settings_obj.THRESH_LEFT:"wheel_stopping_check_failed_punish",
                    settings_obj.THRESH_RIGHT:"wheel_stopping_check_failed_punish",
                    },
            output_actions=[('BNC1',0),('BNC2',0)],
        )
        sma.add_state(
            state_name="wheel_stopping_check_failed_punish",
            state_timer=settings_obj.time_dict["time_wheel_stopping_punish"],
            state_change_conditions={"Tup":"wheel_stopping_check_failed_reset"},
            output_actions=[('BNC1',0),('BNC2',1)]
        )
        sma.add_state(
            state_name="wheel_stopping_check_failed_reset",
            state_timer=0,
            state_change_conditions={"Tup":"reset_rotary_encoder_wheel_stopping_check"},
            output_actions=[('BNC1',0),('BNC2',0)]
        )

        # continue if wheel stopped for time x
        sma.add_state(
            state_name="present_stim",
            state_timer=settings_obj.time_dict["time_stim_pres"],
            state_change_conditions={"Tup": "sync_state_2"},
            output_actions=[("SoftCode", settings_obj.SC_PRESENT_STIM),
                            ('BNC1',0),('BNC2',1)
                            ],#after wait -> present initial stimulus
        )
        sma.add_state(
            state_name="sync_state_2",
            state_timer=0,
            state_change_conditions={"Tup": "reset_rotary_encoder_open_loop"},
            output_actions=[('BNC1',0),('BNC2',0)]
        )
        
        # reset rotary encoder bevor open loop starts
        sma.add_state(
            state_name="reset_rotary_encoder_open_loop",
            state_timer=0,
            state_change_conditions={"Tup": "open_loop"},
            output_actions=[("Serial1", settings_obj.RESET_ROTARY_ENCODER),
                            ('BNC1',0),('BNC2',1)
                            ], # reset rotary encoder postition to 0
        )

        # open loop detection
        sma.add_state(
            state_name="open_loop",
            state_timer=settings_obj.time_dict["time_open_loop"],
            state_change_conditions={"Tup": "stop_open_loop_fail",
                                    settings_obj.STIMULUS_LEFT: "stop_open_loop_reward_left",
                                    settings_obj.STIMULUS_RIGHT: "stop_open_loop_reward_right",
                                    },
            output_actions=[("SoftCode", settings_obj.SC_START_OPEN_LOOP),
                            ('BNC1',0),('BNC2',0)
                            ], # softcode to start open loop
        )

        # stop open loop fail
        sma.add_state(
            state_name="stop_open_loop_fail",
            state_timer=0,
            state_change_conditions={"Tup": "sync_state_3"},
            output_actions=[("SoftCode", settings_obj.SC_STOP_OPEN_LOOP),
                            ('BNC1',0),('BNC2',1)
                            ] # stop open loop in py game
        )

        sma.add_state(
            state_name="sync_state_3",
            state_timer=0,
            state_change_conditions={"Tup": "open_loop_fail_punish"},
            output_actions=[('BNC1',0),('BNC2',0)]
        )

        # open loop fail punish time & exit trial
        sma.add_state(
            state_name="open_loop_fail_punish",
            state_timer=settings_obj.time_dict["time_open_loop_fail_punish"],
            state_change_conditions={"Tup": "inter_trial"},
            output_actions=[("SoftCode", settings_obj.SC_END_PRESENT_STIM),
                            ('BNC1',0),('BNC2',1) # must  be 0 1
                            ]
        )

        # reward left
        sma.add_state(
            state_name="stop_open_loop_reward_left",
            state_timer=settings_obj.time_dict["time_stim_freez"],
            state_change_conditions={"Tup": "check_reward_left"},
            output_actions=[("SoftCode", settings_obj.SC_STOP_OPEN_LOOP),
                            ('BNC1',0),('BNC2',1)
                            ] # stop open loop in py game
        )

        # check for gamble side:
        if probability_dict["gamble_left"]:
            # check for probability of big reard
            if probability_dict["gamble_reward"]:
                print("Gamble_reward_left")
                # big rewaerd
                sma.add_state(
                    state_name="check_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "big_reward_left"},
                    output_actions=[('BNC1',0),('BNC2',0)]
                )
                sma.add_state(
                    state_name="big_reward_left",
                    state_timer=settings_obj.time_dict["open_time_big_reward"],
                    state_change_conditions={"Tup": "reward_left_waiting"},
                    output_actions=[("SoftCode", settings_obj.SC_END_PRESENT_STIM),
                                    ("Valve1", 255),
                                    ('BNC1',1),('BNC2',0)
                                    ]
                )
                sma.add_state(
                    state_name="reward_left_waiting",
                    state_timer=settings_obj.time_dict["time_big_reward_waiting"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[('BNC1',0),('BNC2',1)]
                )
            else:
                # no reward
                print("Gamble_No_Reward_left")
                sma.add_state(
                    state_name="check_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "no_reward_left"},
                    output_actions=[('BNC1',0),('BNC2',0)]
                )
                sma.add_state(
                    state_name="no_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "reward_left_waiting"},
                    output_actions=[("SoftCode", settings_obj.SC_END_PRESENT_STIM),
                                    ('BNC1',1),('BNC2',0)
                                    ],
                )
                sma.add_state(
                    state_name="reward_left_waiting",
                    state_timer=settings_obj.time_dict["time_reward"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[('BNC1',0),('BNC2',1)]
                )
        elif probability_dict["safe_reward"]:
            print("safereward_gambleleft")
            # small reward
            sma.add_state(
                    state_name="check_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "small_reward_left"},
                    output_actions=[('BNC1',0),('BNC2',0)]
                )
            sma.add_state(
                state_name="small_reward_left",
                state_timer=settings_obj.time_dict["open_time_small_reward"],
                state_change_conditions={"Tup": "reward_left_waiting"},
                output_actions=[("SoftCode", settings_obj.SC_END_PRESENT_STIM),
                                ("Valve1", 255),
                                ('BNC1',1),('BNC2',0)
                                ]
            )
            sma.add_state(
                state_name="reward_left_waiting",
                state_timer=settings_obj.time_dict["time_small_reward_waiting"],
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[('BNC1',0),('BNC2',1)]
            )
        else:
            print("nosafereward_gamble_left")
            # no reward
            sma.add_state(
                    state_name="check_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "no_reward_left"},
                    output_actions=[('BNC1',0),('BNC2',0)]
                )
            sma.add_state(
                state_name="no_reward_left",
                state_timer=0,
                state_change_conditions={"Tup": "reward_left_waiting"},
                output_actions=[("SoftCode", settings_obj.SC_END_PRESENT_STIM),
                                ('BNC1',1),('BNC2',0)
                                ]
            )
            sma.add_state(
                state_name="reward_left_waiting",
                state_timer=settings_obj.REWARD_TIME,
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[('BNC1',0),('BNC2',1)]
            )

        #=========================================================================================
        # reward right
        sma.add_state(
            state_name="stop_open_loop_reward_right",
            state_timer=settings_obj.time_dict["time_stim_freez"],
            state_change_conditions={"Tup": "check_reward_right"},
            output_actions=[("SoftCode", settings_obj.SC_STOP_OPEN_LOOP),
                            ('BNC1',0),('BNC2',1)
                            ] # stop open loop in py game
        )

        # check for gmble side:
        if not probability_dict["gamble_left"]:
            # check for probability of big reard
            if probability_dict["gamble_reward"]:
                print("Gamble_Reward_right")
                # big rewaerd
                sma.add_state(
                    state_name="check_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "big_reward_right"},
                    output_actions=[('BNC1',0),('BNC2',0)]
                )
                sma.add_state(
                    state_name="big_reward_right",
                    state_timer=settings_obj.time_dict["open_time_big_reward"],
                    state_change_conditions={"Tup": "reward_right_waiting"},
                    output_actions=[("SoftCode", settings_obj.SC_END_PRESENT_STIM),
                                    ("Valve1", 255),
                                    ('BNC1',1),('BNC2',0)
                                    ]
                )
                sma.add_state(
                    state_name="reward_right_waiting",
                    state_timer=settings_obj.time_dict["time_big_reward_waiting"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[('BNC1',0),('BNC2',1)]
                )
            else:
                print("gamble_No_Reward_right")
                # no reward
                sma.add_state(
                    state_name="check_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "no_reward_right"},
                    output_actions=[('BNC1',0),('BNC2',0)]
                )
                sma.add_state(
                    state_name="no_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "reward_right_waiting"},
                    output_actions=[("SoftCode", settings_obj.SC_END_PRESENT_STIM),
                                    ('BNC1',1),('BNC2',0)
                                    ],
                )
                sma.add_state(
                    state_name="reward_right_waiting",
                    state_timer=settings_obj.time_dict["time_reward"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[('BNC1',0),('BNC2',1)]
                )
        elif probability_dict["safe_reward"]:
            print("safe_reward_right")
            # small reward
            sma.add_state(
                    state_name="check_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "small_reward_right"},
                    output_actions=[('BNC1',0),('BNC2',0)]
                )
            sma.add_state(
                state_name="small_reward_right",
                state_timer=settings_obj.time_dict["open_time_small_reward"],
                state_change_conditions={"Tup": "reward_right_waiting"},
                output_actions=[("SoftCode", settings_obj.SC_END_PRESENT_STIM),
                                ("Valve1", 255),
                                ('BNC1',1),('BNC2',0)
                                ]
            )
            sma.add_state(
                state_name="reward_right_waiting",
                state_timer=settings_obj.time_dict["time_small_reward_waiting"],
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[('BNC1',0),('BNC2',1)]
            )
        else:
            print("safe_No_reward_right")
            # no reward
            sma.add_state(
                    state_name="check_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "no_reward_right"},
                    output_actions=[('BNC1',0),('BNC2',0)]
                )
            sma.add_state(
                state_name="no_reward_right",
                state_timer=0,
                state_change_conditions={"Tup": "reward_right_waiting"},
                output_actions=[("SoftCode", settings_obj.SC_END_PRESENT_STIM),
                                ('BNC1',1),('BNC2',0)
                                ]
            )
            sma.add_state(
                state_name="reward_right_waiting",
                state_timer=settings_obj.time_dict["time_reward"],
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[('BNC1',0),('BNC2',1)]
            )

        # inter trial time
        sma.add_state(
            state_name="inter_trial",
            state_timer=settings_obj.time_dict["time_inter_trial"],
            state_change_conditions={"Tup": "end_state_signal"},
            output_actions=[('BNC1',0),('BNC2',0)],
        )

        # end state necessary for bnc1 and bnc2 = +1 
        sma.add_state(
            state_name="end_state_signal",
            state_timer=0,
            state_change_conditions={"Tup":"end_state"},
            output_actions=[('BNC1',1),('BNC2',1)],
        )
        sma.add_state(
            state_name="end_state",
            state_timer=0,
            state_change_conditions={"Tup":"exit"},
            output_actions=[("SoftCode", settings_obj.SC_END_LOGGING),
                            ('BNC1',0),('BNC2',0)
                            ],
        )

        # create pygame daemon
        threading.Thread(target=stimulus_game.run_game, daemon=True).start()

        # send & run state machine
        bpod.send_state_machine(sma)
        pa = threading.Thread(target=bpod.run_state_machine, args=(sma,), daemon=True)
        pa.start()


        # run stimulus game
        stimulus_game.run_game(display_stim_event, 
                                start_open_loop_event,
                                still_show_event,
                                )

        # post trial cleanup
        pa.join()
        print("---------------------------------------------------")
        #print(f"trial: {trial}")
        #print(f"side: {var_side}")
        #print(f"reward: {var_reward}")
        #print(f"probability: {probability_dict}")

    #==========================================================================================================
    stimulus_game.stop_open_loop()  
    stimulus_game.end_present_stimulus()  
    stimulus_game.end_trial()
    print("finished")

    # user input after session
    window = UserInput(settings_obj)
    window.draw_window_after()
    window.show_window()

    # save session settings
    session_name = bpod.session_name
    # save usersettings of session
    settings_obj.save_usersettings(session_name)
    # save wheel movement of session
    rotary_encoder_module.rotary_encoder.disable_logging()
    # append wheel postition
    #log = rotary_encoder_module.get_logging()
    #print(log)
    #settings_obj.update_wheel_log(rotary_encoder_module.get_logging())
    # append stimulus postition
    #settings_obj.update_stim_log(stimulus_game.stimulus_posititon)
    #settings_obj.save_wheel_movement(session_name)
    # save stimulus postition of session
    #settings_obj.save_stimulus_postition(session_name)

    # push session to alyx


    #print(len(rotary_encoder_module.rotary_encoder.get_logged_data()))

# remove session from pybpod if not run_loop
else:
    #todo donst save current session
    None
try:
    stimulus_game.quite()
except:
    pass
rotary_encoder_module.close()
bpod.close()