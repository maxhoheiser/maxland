import threading
import os
import sys
import inspect
import json
import random
import time


import numpy as np



# span subprocess
# add module path to sys path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
dir = (os.path.dirname(os.path.dirname(currentdir)))
if os.path.isdir(os.path.join(dir, "modules")):
    maxland_root = dir
else:
    maxland_root = os.path.dirname(dir)
modules_dir = os.path.join(maxland_root, "modules")
sys.path.insert(-1, modules_dir)

# import custom modules
from parameter_handler import TrialParameterHandler
from probability_conf import ProbabilityConstuctor

# import usersettings
import usersettings


# create settings object
session_folder = os.getcwd()
settings_folder = currentdir  # os.path.join(currentdir.split('experiments')[0],"tasks","confidentiality_task_training_simple")
settings_obj = TrialParameterHandler(usersettings, settings_folder, session_folder)

# probability constructor
probability_obj = ProbabilityConstuctor(settings_obj)


sides_li = []
# times
times_li = []

for trial in range(50):
    # create random stimulus side
    probability_obj.get_random_side()
    sides_li.append(probability_obj.stim_side_dict.copy())
    # get random punish time
    punish_time = round(random.uniform(
        float(settings_obj.time_dict['time_range_noreward_punish'][0]),
        float(settings_obj.time_dict['time_range_noreward_punish'][1])
    ), 2)
    times_li.append(punish_time)
    # construct states

    current_trial = type('obj', (object,), {'states_durrations' : dict()})

    if trial <= 5:
        current_trial.states_durrations["check_reward_left"] = [(10,10),]
        current_trial.states_durrations["check_reward_right"] = [(np.nan,np.nan),]
    elif trial > 5 and trial <= 7:
        current_trial.states_durrations["check_reward_left"] = [(np.nan,np.nan),]
        current_trial.states_durrations["check_reward_right"] = [(10,10),]
    elif trial == 8:
        current_trial.states_durrations["check_reward_left"] = [(10,10),]
        current_trial.states_durrations["check_reward_right"] = [(np.nan,np.nan),]
    elif trial >= 9 and trial<12:
        current_trial.states_durrations["check_reward_left"] = [(10,10),]
        current_trial.states_durrations["check_reward_right"] = [(np.nan,np.nan),]
    elif trial >= 12 and trial<21:
        current_trial.states_durrations["check_reward_left"] = [(np.nan,np.nan),]
        current_trial.states_durrations["check_reward_right"] = [(10,10),]

    elif trial > 20:
        current_trial.states_durrations["check_reward_left"] = [(10,10),]
        current_trial.states_durrations["check_reward_right"] = [(np.nan,np.nan),]

    probability_obj.insist_mode_check(current_trial)