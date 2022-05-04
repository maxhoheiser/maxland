task = 'conf'

"""specify custom settings for session in this file:

How to:
	edit values for capital variables
	do not change capital variable names

"""
# stimulus ====================================================
#grating_SF = 0.25  # 4 cycles per degree visual angle
#grating_ori = 0   # in degree

STIMULUS_CORRECT = {"grating_sf": 0.0077, "grating_ori": 0.0, "grating_size": 45.0, "grating_speed": 0.024}

STIMULUS_WRONG = {"grating_sf": 0.0013, "grating_ori": 0.0, "grating_size": 45.0, "grating_speed": 0.024}

# trials
TRIAL_NUMBER = 700

# stimulus size and color - only for moving stimulus
STIMULUS_RAD = 44 # pixel radius of stimulus
STIMULUS_COL = [0, 255, 1]#color of stimulus

BACKGROUND_COL = [0, 0, 0]#-1,-1,-1 for black
STIMULUS_TYPE = "two-stimuli" #three-stimuli #two-stimuli #one-stimulus

#===============================================================
# reward in ml
REWARD = 0.08

LAST_CALLIBRATION = "2020.06.10"

# state machine settings =======================================
# waiting time beginning of each trial
TIME_START = 0.0
# time the wheel has to be stopped
TIME_WHEEL_STOPPING_CHECK = 0.5
# time wait if the wheel is not stopped bevore new trial starts
TIME_WHEEL_STOPPING_PUNISH = 0.0
# time stimulus is presented but not movable
TIME_PRESENT_STIM = 0.0
# time of open loop where wheel moves the stimulus
TIME_OPEN_LOOP = 6.0
# time wait if stimulus not moved far enough to position
TIME_OPEN_LOOP_FAIL_PUNISH = 0.0
# time stimulus is presented at reached position but not movable anymore
TIME_STIM_FREEZ = 0.5
# time the animal has for the reard = valve open + time after
REWARD_TIME =0.08
# no reward time
TIME_RANGE_OPEN_LOOP_WRONG_PUNISH = [2.5, 3.0]
# time at end of each trial_num
INTER_TRIAL_TIME = 2.0

# Insist Mode =================================================
RANGE_INSIST_TRIGGER = 7
NUMBER_CORRECT_INSIST_DEACTIVATE = 3
RANGE_INSIST_DEACTIVATE = 3


# Rule Switching Mode =========================================
RULE_SWITCH_INITIAL_WAIT = 20 # wait for n trials bevore checking for rule switching
RULE_SWITCH_RANGE = 15# range of trials for checking for rule switching
RULE_SWITCH_CORRECT = 13# number of correct trials for rule switching

# Fade away ===================================================
FADE_START = 1400 # from center to left side where stimulus fade away begins
FADE_END = 2500 # from center to left side where stimulus fade away ends

# rotary Encoder ==============================================
""" Construct thresholds like this:
[
	-90, 90, # stimulus position in degrees of wheel movement
	-1, 1    # wheel not stoping sthreshold in degrees of wheel movement
]
"""
# threhsolds for event signaling between rotary encoder and bpod
ALL_THRESHOLDS = [
    -40,
    40,
    -1,
    1
]
# speed of movement
STIM_END_POS = [
    -1600,
    1600
] # pixel
"""
end of 1st screen from center = 960 px
end of 2nd screen from center = 960 + 1920px
"""

LIFE_PLOT = True
# Animal ===================================================
# animal waight in grams
ANIMAL_WAIGHT = 20.0
