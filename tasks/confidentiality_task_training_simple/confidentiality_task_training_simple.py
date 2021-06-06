"""
Main config file for the convidentiality task training stage 2a - simple discrimination
This behavior config file makes use of three 
Bpod classes the main Bpod and the StateMachine aswell as the RotaryEncoder.

In addition it uses three custom classes:
    Stimulus: handeling the psychopy configuration and drawing of the stimulus on the screens
    ProbabilityConstructor: generating the necessary probabilites for each trial
    BpodRotaryEncoder: handeling the rotary encoder and reading the position
    TrialParameterHandler: generating the necessary parameters for each session from the user input and predefined parameters

"""

import threading
import os,sys,inspect
import json
import random

# import pybpod modules
from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpodgui_api.models.session import Session

# add module path to sys path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
maxland_root = os.path.dirname(os.path.dirname(currentdir))
modules_dir = os.path.join(maxland_root,"modules")
sys.path.insert(0,modules_dir) 

# import custom modules
from stimulus_conf import Stimulus
#from probability_conf import ProbabilityConstuctor
from rotaryencoder import BpodRotaryEncoder
from parameter_handler import TrialParameterHandler
from userinput import UserInput

# import usersettings
import usersettings

# create settings object
session_folder = os.getcwd()
# TODO: correct for final foderl
#settings_folder = os.path.join(session_folder.split('experiments')[0],"tasks","confidentiality_task_training_simple")
settings_folder = session_folder
settings_obj = TrialParameterHandler(usersettings, settings_folder, session_folder,"conf")

# create bpod object
bpod=Bpod('/dev/cu.usbmodem62917601')

# create tkinter userinput dialoge window
window = UserInput(settings_obj)
window.draw_window_bevore_conf()
window.show_window()
#window.update_settings() 

# run session
if settings_obj.run_session:
    settings_obj.update_userinput_file_conf()
    # rotary encoder config
    # enable thresholds
    rotary_encoder_module = BpodRotaryEncoder('/dev/cu.usbmodem65305701', settings_obj, bpod)
    rotary_encoder_module.load_message()
    rotary_encoder_module.configure()
    #rotary_encoder_module.enable_stream()

    # softcode handler
    def softcode_handler(data):
        if data == settings_obj.SC_PRESENT_STIM:
            stimulus_game.present_stimulus()
        elif data == settings_obj.SC_START_OPEN_LOOP:
            stimulus_game.start_open_loop()
        elif data == settings_obj.SC_STOP_OPEN_LOOP:
            stimulus_game.stop_open_loop()
        elif data == settings_obj.SC_END_PRESENT_STIM:
            stimulus_game.end_present_stimulus()
        elif data == settings_obj.SC_START_LOGGING:
            rotary_encoder_module.rotary_encoder.enable_logging()
            print("enable logging")
        elif data == settings_obj.SC_END_LOGGING:
            rotary_encoder_module.rotary_encoder.disable_logging()
            print("disable logging")

    bpod.softcode_handler_function = softcode_handler

    #probability constructor
    correct_stim_side = {
        "right" : True, # True = correct
        "left" : False  # False = wrong
    }
    def random_side(stim_dict):
        random_side = bool(random.getrandbits(1))
        stim_dict["right"]=random_side
        stim_dict["left"]= not(random_side)
    # TODO: remove
    stim_side_list = [correct_stim_side]
    #stimulus
    stimulus_game = Stimulus(settings_obj, rotary_encoder_module, correct_stim_side)


    # create main state machine aka trial loop ====================================================================
    # state machine configs
    for trial in range(settings_obj.trial_number):
        # create random side
        random_side(correct_stim_side)
        print(ranadom_side)




bpod=Bpod('/dev/cu.usbmodem62917601')
modules = bpod.modules

for x in modules:
    print(x.name)


rotary_encoder = [x for x in self.bpod.modules if x.name == "RotaryEncoder1"][0]

test = [x for x in bpod.modules if x.name=="RotaryEncoder1"][0]