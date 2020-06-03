import numpy as np
import threading

from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from pybpodapi.com.arcom import ArCOM, ArduinoTypes

from stimulus import Stimulus
from statemachine import
import user_settings
import system_settings


bpod=Bpod()
trials = 3

#==============================================================================
# rotary encoder config
#==============================================================================
rotary_encoder = [x for x in bpod.modules if x.name == "RotaryEncoder1"][0]
RESET_ROTARY_ENCODER = 1
bpod.load_serial_message(rotary_encoder, RESET_ROTARY_ENCODER, [ord('Z'), ord('E')])
#bpod.load_serial_message(rotary_encoder, 2, [ord("#"), 2])

rotary_encoder=RotaryEncoderModule('COM6')
rotary_encoder.set_thresholds(ALL_THRESHOLDS)
rotary_encoder.enable_thresholds(ENABLE_THRESHOLDS)
rotary_encoder.enable_evt_transmission()

STIMULUS_LEFT="RotaryEncoder1_1"
STIMULUS_RIGHT="RotaryEncoder1_2"

THRESH_LEFT = "RotaryEncoder1_3"
THRESH_RIGHT="RotaryEncoder1_4"

#==============================================================================
# softcode handler
SC_PRESENT_STIM = 1
SC_START_OPEN_LOOP = 2
SC_STOP_OPEN_LOOP = 3
SC_END_PRESENT_STIM = 4
#==============================================================================
def softcode_handler(data):
    if data == SC_PRESENT_STIM:
        stimulus_game.present_stimulus()
        print("present stimulus")
    elif data == SC_START_OPEN_LOOP:
        stimulus_game.start_open_loop()
        print("start oppen loop")
    elif data == SC_STOP_OPEN_LOOP:
        stimulus_game.stop_open_loop()
        print("stop open loop")
    elif data == SC_END_PRESENT_STIM:
        stimulus_game.end_present_stimulus()
        print("end  presentation")

bpod.softcode_handler_function = softcode_handler

#====================================================================================================================
#pygame
settings = {"TRIAL_NUM": trials, "ROTARY_ENCODER":rotary_encoder}
stimulus_game = Stimulus(settings)

#===============================================================================================================
# state machine configs
# states -> thread 1
def trial():
    # construct pygame objec
    #===============================================
    #variables



    #===============================================

    for trial in range(trials):
        # define states
        sma = StateMachine(bpod)
        # sart state blink green two times



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
