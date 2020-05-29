import numpy as np
import threading

from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from pybpodapi.com.arcom import ArCOM, ArduinoTypes

from stimulus import Stimulus
from statemachine import StateMachineBuilder
from probability import ProbabilityConstuctor
from rotaryencoder import BpodRotaryEncoder
import settings


bpod=Bpod()

# rotary encoder config
rotary_encoder_module = BpodRotaryEncoder('COM4', settings)
rotary_encoder_module.load_message(bpod)
rotary_encoder = rotary_encoder_module.configure()

# softcode handler
def softcode_handler(data):
    if data == settings.SC_PRESENT_STIM:
        stimulus_game.present_stimulus()
        print("present stimulus")
    elif data == settings.SC_START_OPEN_LOOP:
        stimulus_game.start_open_loop()
        print("start oppen loop")
    elif data == settings.SC_STOP_OPEN_LOOP:
        stimulus_game.stop_open_loop()
        print("stop open loop")
    elif data == settings.SC_END_PRESENT_STIM:
        stimulus_game.end_present_stimulus()
        print("end  presentation")
bpod.softcode_handler_function = softcode_handler

#stimulus
stimulus_game = Stimulus(settings, rotary_encoder)


#probability constructor
probability = ProbabilityConstuctor(settings)

# state machine configs
def trial():
    TRIAL_NUM = 0
    for block in settings.BLOCKS:
        TRIAL_NUM += block[settings.TRIAL_NUM_BLOCK]
    for trial in range(TRIAL_NUM):
        # define states
        sma = StateMachineBuilder(bpod, settings, probability.probability_list[trial])
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
