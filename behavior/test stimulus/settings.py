TRIAL_RANGE_BLOCK = "trial_range_block"
PROB_REWARD_GAMBL_BLOCK = "prob_reward_gambl_block"
PROB_REWARD_SAVE_BLOCK = "prob_reward_save_block"

#==================================================================================================================
# Edit from here ==================================================================================================


# stimulus ========================
STIMULUS = r"C:\test_projekt\test_projekt\tasks\behavior_1_test\stimulus.png"

# rotary Encoder ==================
"""
[-float, float, -float, float]
"""
# threhsolds for event signaling between rotary encoder and bpod
ALL_THRESHOLDS = [
                    -45, 45, # stimulus position in degrees of wheel movement
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
