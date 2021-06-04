"""
Main config file for the convidentiality task training stage 2a - simple discrimination
This behavior config file makes use of three PyBpod classes the main Bpod and the StateMachine aswell as the RotaryEncoder.

In addition it uses three custom classes:
    Stimulus: handeling the psychopy configuration and drawing of the stimulus on the screens
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
maxland_root = os.path.dirname(os.path.dirname(os.path.dirname(currentdir)))
modules_dir = os.path.join(maxland_root,"modules")
sys.path.insert(0,modules_dir) 

# import custom modules
from stimulus_conf import Stimulus
from probability_conf import ProbabilityConstuctor
from rotaryencoder import BpodRotaryEncoder
from parameter_handler import TrialParameterHandler
from userinput_conf import UserInput

# import usersettings
import usersettings

# create settings object
session_folder = os.getcwd()
settings_folder = os.path.join(session_folder.split('experiments')[0],"tasks","gamble_task_training")
settings_obj = TrialParameterHandler(usersettings, settings_folder, session_folder)

# create bpod object
bpod=Bpod()

# create tkinter userinput dialoge window
window = UserInput(settings_obj)
window.draw_window_bevore()
window.show_window()
window.update_settings() 