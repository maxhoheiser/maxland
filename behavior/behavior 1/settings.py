# main settings
TRIAL_NUM_PROP_1 = 3
TRIAL_NUM_PROP_2 = 3
TRIAL_NUM_PROP_3 = 3
# set True if gamble side is legt , else false
GAMB_SIDE_LEFT = True
#probability for reward on gamble side in %
PROB_REWARD_GAMBL_1 = 12.5
PROB_REWARD_GAMBL_2 = 25.5
PROB_REWARD_GAMBL_3 = 75.5
#probability for reward on save side
PROB_REWARD_SAVE_1 = 90
PROB_REWARD_SAVE_2 = 90
PROB_REWARD_SAVE_3 = 90

# rotary Encoder
ALL_THRESHOLDS = [-150, 150, -2, 2]
ENABLE_THRESHOLDS = [True, True, True, True, False, False, False, False]

# state machine settings
TIME_START = 2
TIME_WHEEL_STOPPING_CHECK = 5
TIME_WHEEL_STOPPING_PUNISH = 5
TIME_PRESENT_STIM = 5
TIME_OPEN_LOOP = 10
TIME_OPEN_LOOP_FAIL_PUNISH = 5
TIME_STIM_FREEZ = 2
REWARD_TIME = 10
BIG_REWARD_TIME = 5
SMALL_REWARD_TIME = 5

# stimulus
STIMULUS = r"C:\test_projekt\test_projekt\tasks\behavior_1_test\stimulus.png"



#=======================================================================================================================
#=======================================================================================================================
# system settings - do not touch !
#=======================================================================================================================
#=======================================================================================================================
# state machine
big_reward_waiting_time = REWARD_TIME - BIG_REWARD_TIME
small_reward_waiting_time = REWARD_TIME - SMALL_REWARD_TIME

# sofct code
SC_PRESENT_STIM = 1
SC_START_OPEN_LOOP = 2
SC_STOP_OPEN_LOOP = 3
SC_END_PRESENT_STIM = 4

# rotary encoder message
RESET_ROTARY_ENCODER = 1
THRESH_LEFT = "RotaryEncoder1_3"
THRESH_RIGHT = "RotaryEncoder1_4"
STIMULUS_LEFT = "RotaryEncoder1_1"
STIMULUS_RIGHT = "RotaryEncoder1_2"

# stimulus
GAIN = 3
THRESHOLD = 2000
FPS=120
SCREEN_WIDTH = 5760
SCREEN_HEIGHT = 1200
