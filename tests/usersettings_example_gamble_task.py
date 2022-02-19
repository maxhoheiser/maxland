TASK = "gamble"

GAMBLE_SIDE = "left"
BLOCKS = [
    {"trial_range_block": [4, 7], "prob_reward_gamble_block": 10.0, "prob_reward_save_block": 20.0},
    {"trial_range_block": [3, 5], "prob_reward_gamble_block": 30.0, "prob_reward_save_block": 40.0},
    {"trial_range_block": [5, 8], "prob_reward_gamble_block": 50.0, "prob_reward_save_block": 50.0},
]

# reward in seconds
BIG_REWARD = 0.11
SMALL_REWARD = 0.12
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
TIME_NO_REWARD = 1.0
TIME_INTER_TRIAL = 1.5

# stimulus size and color - only for moving stimulus
STIMULUS_RADIUS = 45  # pixel radius of stimulus
STIMULUS_COLOR = [0, 255, 0]  # color of stimulus
BACKGROUND_COLOR = [0, 0, 0]

# thresholds
ROTARYENCODER_THRESHOLDS = [-90, 90, -2, 2]
STIMULUS_END_POSITION = [-2048, 2048]  # pixel

LIFE_PLOT = False
# animal weight in grams
ANIMAL_WEIGHT = 10.0
