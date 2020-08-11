
gamble_side = "Left"
GAMB_SIDE_LEFT = True #False if side = right
# Blocks ========================================================
"""
Construct a Block like this:
    {
    TRIAL_NUM_BLOCK: [int, int], #(50 - 80) #will chose a random length in between
    PROB_REWARD_GAMBL_BLOCK: int,  #(0-100)
    "prob_reward_save_block": int  #(0-100)
    },
"""

BLOCKS = [
            # block 1
            {
            "trial_range_block": [50, 80],
            "prob_reward_gambl_block": 12.5,  #(0-100)
            "prob_reward_save_block": 90  #(0-100)
            },
            # block 3
            {
            "trial_range_block": [10, 30],
            "prob_reward_gambl_block": 12.5,  #(0-100)
            "prob_reward_save_block": 90  #(0-100)
            },
            # block 2
            {
            "trial_range_block": [20, 100],
            "prob_reward_gambl_block": 12.5,  #(0-100)
            "prob_reward_save_block": 90  #(0-100)
            },
        ]


#========================================================
# reward
BIG_REWARD_TIME = 5
# big reard in ml
big_reward = 0.5
# time valve open for small reward
SMALL_REWARD_TIME = 2
# small rewar in ml
small_reward = 0.1

last_calibration = "2020.06.10"

# state machine settings ======================================
# waiting time beginning of each trial
TIME_START = 2
# time the wheel has to be stopped
TIME_WHEEL_STOPPING_CHECK = 5
# time wait if the wheel is not stopped bevore new trial starts
TIME_WHEEL_STOPPING_PUNISH = 5
# time stimulus is presented but not movable
TIME_PRESENT_STIM = 5
# time of open loop where wheel moves the stimulus
TIME_OPEN_LOOP = 10
# time wait if stimulus not moved far enough to position
TIME_OPEN_LOOP_FAIL_PUNISH = 5
# time stimulus is presented at reached position but not movable anymore
TIME_STIM_FREEZ = 2
# time the animal has for the reard = valve open + time after
REWARD_TIME = 10
# time at end of each trial_num
INTER_TRIAL_TIME = 5

time_dict = {
            "time_start": 2,
            # time the wheel has to be stopped
            "time_wheel_stopping_check": 5,
            # time wait if the wheel is not stopped bevore new trial starts
            "time_wheel_stopping_punish": 5,
            # time stimulus is presented but not movable
            "time_stim_pres": 5,
            # time of open loop where wheel moves the stimulus
            "time_open_loop": 10,
            # time wait if stimulus not moved far enough to position
            "time_open_loop_fail_punish": 5,
            # time stimulus is presented at reached position but not movable anymore
            "time_stim_freez": 2,
            # time the animal has for the reard = valve open + time after
            "time_reward": 10,
            # time at end of each trial_num
            "time_inter_trial": 5,
            }

# stimulus ====================================================
STIMULUS = r"C:\test_projekt\test_projekt\tasks\behavior_1_test\stimulus.png"

# rotary Encoder ==============================================
"""
[-float, float, -float, float]
"""
# threhsolds for event signaling between rotary encoder and bpod
ALL_THRESHOLDS = [
                    -90, 90, # stimulus position in degrees of wheel movement
                    -1, 1    # wheel not stoping sthreshold in degrees of wheel movement
                 ]

# speed of movement
STIM_END_POS = [-1920, 1920] # pixel
"""
end of 1st screen from center = 960 px
end of 2nd screen from center = 960 + 1920px
"""
# (e.g. -/+ 1920 = center of side screens)


lifeplot = True

#=======================================================================================================================
#=======================================================================================================================
# system settings - do not touch !
#=======================================================================================================================
#=======================================================================================================================
# trial numbers:


# state machine
big_reward_waiting_time = REWARD_TIME - BIG_REWARD_TIME
small_reward_waiting_time = REWARD_TIME - SMALL_REWARD_TIME

# sofct code
SC_PRESENT_STIM = 1
SC_START_OPEN_LOOP = 2
SC_STOP_OPEN_LOOP = 3
SC_END_PRESENT_STIM = 4

# rotary encoder
WHEEL_DIAMETER = 6.3
RESET_ROTARY_ENCODER = 1
THRESH_LEFT = "RotaryEncoder1_3"
THRESH_RIGHT = "RotaryEncoder1_4"
STIMULUS_LEFT = "RotaryEncoder1_1"
STIMULUS_RIGHT = "RotaryEncoder1_2"

# stimulus
FPS=120
SCREEN_WIDTH = 5760
SCREEN_HEIGHT = 1200
