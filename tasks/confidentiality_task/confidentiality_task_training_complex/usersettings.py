TASK = "conf"
STAGE = "training-complex"

TRIAL_NUMBER = 30
STIMULUS_TYPE = "two-stimuli"  # three-stimuli #two-stimuli #one-stimulus

RULE_A = [
    {
        "correct": "a00b03",
        "wrong": "a03b00",
        "conflicting": True,
        "percentage": 0.4,
    },
    {
        "correct": "a00b02",
        "wrong": "a03b02",
        "conflicting": True,
        "percentage": 0.3,
    },
    {
        "correct": "a00b01",
        "wrong": "a03b03",
        "conflicting": True,
        "percentage": 0.3,
    },
]

RULE_B = [
    {
        "correct": "a01b01",
        "wrong": "a02b01",
        "conflicting": True,
        "percentage": 0.4,
    },
    {
        "correct": "a01b02",
        "wrong": "a02b02",
        "conflicting": True,
        "percentage": 0.3,
    },
    {
        "correct": "a01b03",
        "wrong": "a02b03",
        "conflicting": True,
        "percentage": 0.3,
    },
]

# reward in seconds
REWARD = 0.12
LAST_CALLIBRATION = "2020.06.10"

# trial times
TIME_START = 1.0
TIME_WHEEL_STOPPING_CHECK = 1.0
TIME_WHEEL_STOPPING_PUNISH = 0.0
TIME_PRESENT_STIMULUS = 1.0
TIME_OPEN_LOOP = 10.0
TIME_OPEN_LOOP_FAIL_PUNISH = 0.0
TIME_STIMULUS_FREEZE = 2.0
TIME_REWARD = 1.0
TIME_RANGE_NO_REWARD_PUNISH = [0.0, 0.0]
TIME_INTER_TRIAL = 1.5

# insist mode
INSIST_RANGE_TRIGGER = 5
INSIST_CORRECT_DEACTIVATE = 3
INSIST_RANGE_DEACTIVATE = 35

# rule switching
RULE_SWITCH_INITIAL_TRIALS_WAIT = 10
RULE_SWITCH_CHECK_TRIAL_RANGE = 10
RULE_SWITCH_TRIALS_CORRECT_TRIGGER_SWITCH = 8

# fade away
FADE_START = 1950
FADE_END = 3000

# stimulus size and color - only for moving stimulus
STIMULUS_RADIUS = 45  # pixel radius of stimulus
STIMULUS_COLOR = [0, 255, 0]  # color of stimulus
BACKGROUND_COLOR = [0, 0, 0]

# thresholds
ROTARYENCODER_THRESHOLDS = [-90, 90, -2, 2]
STIMULUS_END_POSITION = [-400, 400]  # pixel

LIFE_PLOT = False
# animal weight in grams
ANIMAL_WEIGHT = 10.0
