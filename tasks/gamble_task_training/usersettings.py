task = "gamble"

"""specify custom settings for session in this file:

How to:
	edit values for capital variables
	do not change capital cariable names

"""

GAMBLE_SIDE = 'Right'

# Blocks ========================================================
"""Construct a Block like this:


{
	TRIAL_NUM_BLOCK: [int, int], #(50 - 80) #will chose a random length in between
	PROB_REWARD_GAMBL_BLOCK: int,  #(0-100)
	prob_reward_save_block: int  #(0-100)
	},
"""

BLOCKS = [
    {
        "trial_range_block": [
            50,
            80
        ],
        "prob_reward_gambl_block": 12.5,
        "prob_reward_save_block": 90.0
    },
    {
        "trial_range_block": [
            10,
            30
        ],
        "prob_reward_gambl_block": 12.5,
        "prob_reward_save_block": 90.0
    },
    {
        "trial_range_block": [
            20,
            100
        ],
        "prob_reward_gambl_block": 12.5,
        "prob_reward_save_block": 90.0
    }
]

#========================================================
# reward
# big reward in ml
BIG_REWARD = 0.5
# small rewar in ml
SMALL_REWARD = 0.1

LAST_CALLIBRATION = '2020.06.10'

# state machine settings ======================================
# waiting time beginning of each trial
TIME_START = 1.0
# time the wheel has to be stopped
TIME_WHEEL_STOPPING_CHECK = 1.0
# time wait if the wheel is not stopped bevore new trial starts
TIME_WHEEL_STOPPING_PUNISH = 1.0
# time stimulus is presented but not movable
TIME_PRESENT_STIM = 1.0
# time of open loop where wheel moves the stimulus
TIME_OPEN_LOOP = 10.0
# time wait if stimulus not moved far enough to position
TIME_OPEN_LOOP_FAIL_PUNISH = 5.0
# time stimulus is presented at reached position but not movable anymore
TIME_STIM_FREEZ = 2.0
# time the animal has for the reard = valve open + time after
REWARD_TIME =10.0
# time at end of each trial_num
INTER_TRIAL_TIME = 5.0

# stimulus ====================================================
STIMULUS = 'C:\\test_projekt\\test_projekt\\tasks\\behavior_1_test\\stimulus.png'

# rotary Encoder ==============================================
""" Construct thresholds like this:
[
		-90, 90, # stimulus position in degrees of wheel movement
	-1, 1    # wheel not stoping sthreshold in degrees of wheel movement
"""
# threhsolds for event signaling between rotary encoder and bpod
ALL_THRESHOLDS = [
    -90,
    90,
    -1,
    1
]
# speed of movement
STIM_END_POS = [
    -1920,
    1920
] # pixel
"""
end of 1st screen from center = 960 px
end of 2nd screen from center = 960 + 1920px
"""

LIFE_PLOT = True
# Animal ===================================================
# animal waight in grams
ANIMAL_WAIGHT = 20.0
