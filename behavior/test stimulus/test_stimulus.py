import threading

from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine

from stimulus import Stimulus
from rotaryencoder import BpodRotaryEncoder
import settings


# create bpod object
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
bpod.softcode_handler_function = softcode_handler

#stimulus
stimulus_game = Stimulus(settings, rotary_encoder_module)

# state machine configs
for trial in range(3):
    sma = StateMachine(bpod)
    # define states
    sma.add_state(
        state_name="start1",
        state_timer=1,
        state_change_conditions={"Tup": "reset_rotary_encoder_wheel_stopping_check"},
        output_actions=[],
    )
    # reset rotary encoder bevore checking for wheel not stoping
    sma.add_state(
        state_name="reset_rotary_encoder_wheel_stopping_check",
        state_timer=0,
        state_change_conditions={"Tup":"wheel_stopping_check"},
        output_actions=[("Serial5", settings.RESET_ROTARY_ENCODER)],
    )
    #wheel not stoping check
    sma.add_state(
        state_name="wheel_stopping_check",
        state_timer=2,
        state_change_conditions={
                "Tup":"present_stim",
                settings.THRESH_LEFT:"wheel_stopping_check_failed_punish",
                settings.THRESH_RIGHT:"wheel_stopping_check_failed_punish",
                },
        output_actions=[],
    )
    sma.add_state(
        state_name="wheel_stopping_check_failed_punish",
        state_timer=0,
        state_change_conditions={"Tup":"start1"},
        #output_actions=[]
        output_actions=[("SoftCode", 5)], #================================================================================
    )

    # ==========================================
    # continue if wheel stopped for time x
    sma.add_state(
        state_name="present_stim",
        state_timer=2,
        state_change_conditions={"Tup": "reset_rotary_encoder_open_loop"},
        output_actions=[("SoftCode", settings.SC_PRESENT_STIM)],#after wait -> present initial stimulus
    )
    # reset rotary encoder bevor open loop starts
    sma.add_state(
        state_name="reset_rotary_encoder_open_loop",
        state_timer=0,
        state_change_conditions={"Tup": "open_loop"},
        output_actions=[("Serial5", settings.RESET_ROTARY_ENCODER),
                        ("SoftCode", settings.SC_START_OPEN_LOOP)
                        ], # reset rotary encoder postition to 0
    )
    # open loop detection
    sma.add_state(
        state_name="open_loop",
        state_timer=10,
        state_change_conditions={
            "Tup": "stop_open_loop_fail",
            settings.STIMULUS_LEFT: "stop_open_loop_success",
            settings.STIMULUS_RIGHT: "stop_open_loop_success",
            },
        output_actions=[],
    )

    # threshold not reached
    sma.add_state(
        state_name="stop_open_loop_fail",
        state_timer=0,
        state_change_conditions={"Tup": "open_loop_fail_punish"},
        output_actions=[("SoftCode", settings.SC_STOP_OPEN_LOOP)] # stop open loop in py game
    )
    sma.add_state(
        state_name="open_loop_fail_punish",
        state_timer=0,
        state_change_conditions={"Tup": "exit"},
        output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM)]
    )

    # treshold reached
    sma.add_state(
        state_name="stop_open_loop_success",
        state_timer=1,
        state_change_conditions={"Tup": "reward_left"},
        output_actions=[("SoftCode", settings.SC_STOP_OPEN_LOOP)] # stop open loop in py game
    )
    sma.add_state(
        state_name="reward_left",
        state_timer=1,
        state_change_conditions={"Tup": "exit"},
        output_actions=[("SoftCode", settings.SC_END_PRESENT_STIM)]
    )

    # create pygame daemon
    threading.Thread(target=stimulus_game.run_game, daemon=True).start()

    # send & run state machine
    bpod.send_state_machine(sma)

    # wiat until state machine finished
    if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
        break

#==========================================================================================================

print("finished")

rotary_encoder_module.close()
bpod.close()
