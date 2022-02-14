task = "gamble"

GAMBLE_SIDE = "Left"
BLOCKS = [
    {"trial_range_block": [1, 2], "prob_reward_gamble_block": 10.0, "prob_reward_save_block": 20.0},
    {"trial_range_block": [3, 4], "prob_reward_gamble_block": 30.0, "prob_reward_save_block": 40.0},
    {"trial_range_block": [5, 6], "prob_reward_gamble_block": 50.0, "prob_reward_save_block": 50.0},
]

# reward in ml
BIG_REWARD = 0.11
SMALL_REWARD = 0.12
LAST_CALLIBRATION = "2020.06.10"

# trial times
TIME_START = 1.0
TIME_WHEEL_STOPPING_CHECK = 1.0
TIME_WHEEL_STOPPING_PUNISH = 0.0
TIME_PRESENT_STIM = 1.0
TIME_OPEN_LOOP = 10.0
TIME_OPEN_LOOP_FAIL_PUNISH = 0.0
TIME_STIM_FREEZ = 2.0
REWARD_TIME = 1.0
NOREWARD_TIME = 1.0
INTER_TRIAL_TIME = 1.5
# stimulus size and color - only for moving stimulus
STIMULUS_RAD = 45  # pixel radius of stimulus
STIMULUS_COL = [0, 255, 0]  # color of stimulus
BACKGROUND_COL = [0, 0, 0]  # -1,-1,-1 for black

# threhsolds
ALL_THRESHOLDS = [-90, 90, -2, 2]
STIM_END_POS = [-2048, 2048]  # pixel

LIFE_PLOT = False
# animal waight in grams
ANIMAL_WAIGHT = 10.0
