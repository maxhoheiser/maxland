TRIAL_RANGE_BLOCK = "trial_range_block"
PROB_REWARD_GAMBL_BLOCK = "prob_reward_gambl_block"
PROB_REWARD_SAVE_BLOCK = "prob_reward_save_block"

#==================================================================================================================
# Edit from here ==================================================================================================

# main settings ====================
GAMB_SIDE_LEFT = True #False if side = right
# Blocks ========================================================
"""
Construct a Block like this:
    {
    TRIAL_NUM_BLOCK: [int, int], #(50 - 80) #will chose a random length in between
    PROB_REWARD_GAMBL_BLOCK: int,  #(0-100)
    PROB_REWARD_SAVE_BLOCK: int  #(0-100)
    },
"""

BLOCKS = [
            # block 1
            {
            TRIAL_RANGE_BLOCK: [50, 80],
            PROB_REWARD_GAMBL_BLOCK: 12.5,  #(0-100)
            PROB_REWARD_SAVE_BLOCK: 90  #(0-100)
            },
            # block 1
            {
            TRIAL_RANGE_BLOCK: [10, 50],
            PROB_REWARD_GAMBL_BLOCK: 25.5,  #(0-100)
            PROB_REWARD_SAVE_BLOCK: 90  #(0-100)
            },
            # block 1
            {
            TRIAL_RANGE_BLOCK: [50, 100],
            PROB_REWARD_GAMBL_BLOCK: 75.5,  #(0-100)
            PROB_REWARD_SAVE_BLOCK: 90  #(0-100)
            },
        ]


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
# time valve open for big reard
BIG_REWARD_TIME = 5
# time valve open for small reward
SMALL_REWARD_TIME = 2
# time at end of each trial_num
INTER_TRIAL_TIME = 5

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
