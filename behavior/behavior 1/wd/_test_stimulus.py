# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:21:52 2020

@author: User
"""
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from stimulus import Stimulus
from rotaryencoder import BpodRotaryEncoder

import settings

import threading
import time

rotary_encoder = BpodRotaryEncoder("COM4", settings.ALL_THRESHOLDS, 6.3)
rotary_encoder.configure()


stimulus_game = Stimulus(settings, rotary_encoder)

def trial():
    for tiral in range(settings.TRIAL_NUM):
        time.sleep(2)
        stimulus_game.present_stimulus()
        print("present stimulus")
        time.sleep(2)
        stimulus_game.start_open_loop()
        print("start oppen loop")
        time.sleep(10)
        stimulus_game.stop_open_loop()
        print("stop open loop")
        time.sleep(2)
        stimulus_game.end_present_stimulus()
        print("trial end")

t1 = threading.Thread(target=stimulus_game.run_game)
t1.start()

t2 = threading.Thread(target=trial)
t2.start()
t2.join()

rotary_encoder.close()


#liste = stimulus_game.list_new_new