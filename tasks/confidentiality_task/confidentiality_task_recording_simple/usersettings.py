TASK = "conf"
STAGE = "recording"

TRIAL_NUMBER = 500
STIMULUS_TYPE = "two-stimuli"  # three-stimuli #two-stimuli #one-stimulus
STIMULUS_CORRECT = {"grating_frequency": 0.002, "grating_orientation": 0.0, "grating_size": 45.0, "grating_speed": 0.015}
STIMULUS_WRONG = {"grating_frequency": 0.002, "grating_orientation": 90.0, "grating_size": 45.0, "grating_speed": 0.015}


# reward in seconds
REWARD = 0.1
LAST_CALLIBRATION = "2020.06.10"

# trial times
TIME_START = 0.0
TIME_WHEEL_STOPPING_CHECK = 0.5
TIME_WHEEL_STOPPING_PUNISH = 0.0
TIME_PRESENT_STIMULUS = 0.0
TIME_OPEN_LOOP = 6.0
TIME_OPEN_LOOP_FAIL_PUNISH = 0.0
TIME_STIMULUS_FREEZE = 0.0
TIME_REWARD = 0.1
TIME_RANGE_NO_REWARD_PUNISH = [0.0, 0.0]
TIME_INTER_TRIAL = 1.5

# insist mode
INSIST_RANGE_TRIGGER = 7
INSIST_CORRECT_DEACTIVATE = 3
INSIST_RANGE_DEACTIVATE = 3

# rule switching
RULE_SWITCH_INITIAL_TRIALS_WAIT = 30
RULE_SWITCH_CHECK_TRIAL_RANGE = 12
RULE_SWITCH_TRIALS_CORRECT_TRIGGER_SWITCH = 9

# fade away
FADE_START = 1900
FADE_END = 3000

# stimulus size and color - only for moving stimulus
STIMULUS_RADIUS = 44  # pixel radius of stimulus
STIMULUS_COLOR = [0, 255, 1]  # color of stimulus
BACKGROUND_COLOR = [-1, -1, -1]

# thresholds
ROTARYENCODER_THRESHOLDS = [-70, 70, -1, 1]
STIMULUS_END_POSITION = [-1600, 1600]  # pixel

LIFE_PLOT = True
# animal weight in grams
ANIMAL_WEIGHT = 20.0
