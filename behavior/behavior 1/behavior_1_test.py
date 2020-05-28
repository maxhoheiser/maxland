from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
import numpy as np
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from pybpodapi.com.arcom import ArCOM, ArduinoTypes

from stimulus_class import Stimulus
import threading

bpod=Bpod()
trials = 3

#==============================================================================
# rotary encoder config
#==============================================================================
rotary_encoder = [x for x in bpod.modules if x.name == "RotaryEncoder1"][0]
reset_re = 1
bpod.load_serial_message(rotary_encoder, 1, [ord('Z'), ord('E')])
#bpod.load_serial_message(rotary_encoder, 2, [ord("#"), 2])

rotary_encoder=RotaryEncoderModule('COM6')

ALL_THRESHOLDS = [-150, 150, -2, 2]
ENABLE_THRESHOLDS = [True, True, True, True, False, False, False, False]

rotary_encoder.set_thresholds(ALL_THRESHOLDS)
rotary_encoder.enable_thresholds(ENABLE_THRESHOLDS)
rotary_encoder.enable_evt_transmission()

movement_left="RotaryEncoder1_1"
movement_right="RotaryEncoder1_2"
incr_left="RotaryEncoder1_3"
incr_right="RotaryEncoder1_4"

#==============================================================================
# softcode handler
#==============================================================================
def softcode_handler(data):
    if data == 1:
        stimulus_game.present_stimulus()
        print("present stimulus")
    elif data == 2:
        stimulus_game.start_open_loop()
        print("start oppen loop")
    elif data == 3:
        stimulus_game.stop_open_loop()
        print("stop open loop")
    elif data == 4:
        stimulus_game.end_present_stimulus()
        print("end  presentation")

bpod.softcode_handler_function = softcode_handler

#====================================================================================================================
#pygame
#====================================================================================================================
settings = {"TRIAL_NUM": trials, "ROTARY_ENCODER":rotary_encoder}
stimulus_game = Stimulus(settings)

#===============================================================================================================
# state machine configs
#===============================================================================================================
# states -> thread 1
def trial():
    # construct pygame objec

    for trial in range(trials):
        #====================================
        # start pygmae threading
        #====================================
        # define states
        sma = StateMachine(bpod)
        # sart state blink green two times
        sma.add_state(
            state_name="1",
            state_timer=1,
            state_change_conditions={"Tup": "2"},
            output_actions=[("BNC1", 1), ("BNC2", 1) #blink white + red
                            ],
        )
        sma.add_state(
            state_name="2",
            state_timer=1,
            state_change_conditions={"Tup": "2_1"},
            output_actions=[("SoftCode", 1)],
        )

        sma.add_state(
            state_name="2_1",
            state_timer=1,
            state_change_conditions={"Tup": "3"},
            output_actions=[("Serial1", 1)],
        )

        sma.add_state(
            state_name="3",
            state_timer=10,
            state_change_conditions={"Tup": "4"},
            output_actions=[("SoftCode", 2)],
        )

        sma.add_state(
            state_name="4",
            state_timer=1,
            state_change_conditions={"Tup": "5"},
            output_actions=[("SoftCode", 3)],
        )
        sma.add_state(
            state_name="5",
            state_timer=1,
            state_change_conditions={"Tup": "exit"},
            output_actions=[("SoftCode", 4)],
        )

        bpod.send_state_machine(sma)
        # Run state machine
        if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
            break




#==========================================================================================================
t1 = threading.Thread(target=stimulus_game.run_game)
t1.start()

t2 = threading.Thread(target=trial)
t2.start()

t2.join()
print("finished")


rotary_encoder.close()
bpod.close()
