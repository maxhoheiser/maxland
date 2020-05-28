import numpy as np
import threading

from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from pybpodapi.com.arcom import ArCOM, ArduinoTypes

from stimulus import Stimulus
from statemachine import StateMachineBuilder
from probability import ProbabilityConstuctor
import user_settings
import system_settings


bpod=Bpod()

# rotary encoder config
rotary_encoder = [x for x in bpod.modules if x.name == "RotaryEncoder1"][0]
bpod.load_serial_message(rotary_encoder, settings.RESET_ROTARY_ENCODER, [ord('Z'), ord('E')])

rotary_encoder=RotaryEncoderModule('COM6')
rotary_encoder.set_thresholds(settings.ALL_THRESHOLDS)
rotary_encoder.enable_thresholds(settings.ENABLE_THRESHOLDS)
rotary_encoder.enable_evt_transmission()


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


# state machine configs
probability = ProbabilityConstuctor(settings)
def trial():
    for trial in range(settings.TRIAL_NUM):
        # define states
        sma = StateMachineBuilder(bpod, settings, probability[trial]):
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
