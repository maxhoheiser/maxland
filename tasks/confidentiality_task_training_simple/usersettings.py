task = 'conf'

"""specify custom settings for session in this file:

How to:
	edit values for capital variables
	do not change capital variable names

"""
# stimulus ====================================================
#grating_SF = 0.25  # 4 cycles per degree visual angle
#grating_ori = 0   # in degree

STIMULUS_CORRECT = {"grating_sf": 0.01, "grating_ori": 0.1, "grating_size": 46.0, "grating_speed": 0.04}

STIMULUS_WRONG = {"grating_sf": 0.004, "grating_ori": 93.0, "grating_size": 42.0, "grating_speed": 0.01}

# trials
TRIAL_NUMBER = 1

# stimulus size and color - only for moving stimulus
STIMULUS_RAD = 44 # pixel radius of stimulus
STIMULUS_COL = [0, 255, 1]#color of stimulus

BACKGROUND_COL = [-1, -1, -1]#-1,-1,-1 for black
STIMULUS_TYPE = "three-stimuli" #three-stimuli #two-stimuli #one-stimulus

#===============================================================
# reward in ml
REWARD = 2.0

LAST_CALLIBRATION = "2020.06.10"

# state machine settings =======================================
# waiting time beginning of each trial
TIME_START = 2.0
# time the wheel has to be stopped
TIME_WHEEL_STOPPING_CHECK = 3.0
# time wait if the wheel is not stopped bevore new trial starts
TIME_WHEEL_STOPPING_PUNISH = 4.0
# time stimulus is presented but not movable
TIME_PRESENT_STIM = 5.0
# time of open loop where wheel moves the stimulus
TIME_OPEN_LOOP = 6.0
# time wait if stimulus not moved far enough to position
TIME_OPEN_LOOP_FAIL_PUNISH = 7.0
# time stimulus is presented at reached position but not movable anymore
TIME_STIM_FREEZ = 8.0
# time the animal has for the reard = valve open + time after
REWARD_TIME =9.0
# no reward time
TIME_RANGE_OPEN_LOOP_WRONG_PUNISH = [10.0, 11.0]
# time at end of each trial_num
INTER_TRIAL_TIME = 13.0

# Insist Mode =================================================
RANGE_INSIST_TRIGGER = 10
NUMBER_CORRECT_INSIST_DEACTIVATE = 13
RANGE_INSIST_DEACTIVATE = 12


# rotary Encoder ==============================================
""" Construct thresholds like this:
[
	-90, 90, # stimulus position in degrees of wheel movement
	-1, 1    # wheel not stoping sthreshold in degrees of wheel movement
]
"""
# threhsolds for event signaling between rotary encoder and bpod
ALL_THRESHOLDS = [
    -91,
    92,
    -1,
    1
]
# speed of movement
STIM_END_POS = [
    -1901,
    1903
] # pixel
"""
end of 1st screen from center = 960 px
end of 2nd screen from center = 960 + 1920px
"""

LIFE_PLOT = True
# Animal ===================================================
# animal waight in grams
ANIMAL_WAIGHT = 20.0
