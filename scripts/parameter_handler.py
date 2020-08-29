import jsonpickle
import json
import os


class TrialParameterHandler():
    def __init__(self, usersettings, path):
        """class that handls user input and settings for each session

        Args:
            usersettings (object): settings file which loads usersettings input
            path (string): path to usersettings file
        """        
        self.usersettings = usersettings
        self.path = path

        # life ploting
        self.life_plot = usersettings.LIFE_PLOT

        self.gamble_side = usersettings.GAMBLE_SIDE
        # create gamble side bool
        self.gamble_side_left = lambda x: True if self.gamble_side=='Left' else False
        # blocks for probability
        self.blocks = usersettings.BLOCKS
        # reward amount in ml
        self.big_reward = usersettings.BIG_REWARD
        self.small_reward = usersettings.SMALL_REWARD
        # reward valve open times
        (self.big_reward_open_time, self.small_reward_open_time) = self.create_valve_open_time()
        # calibration
        self.last_callibration = usersettings.LAST_CALLIBRATION
        # times
        self.time_dict = self.create_time_dict()
        # stimulus
        self.stim = usersettings.STIMULUS
        # configs for rotary encoder
        self.thresholds = usersettings.ALL_THRESHOLDS
        self.stim_end_pos = usersettings.STIM_END_POS

        # animal variables
        self.animal_waight = usersettings.ANIMAL_WAIGHT

        # system settings for each session
        # sofct code
        self.SC_PRESENT_STIM = 1
        self.SC_START_OPEN_LOOP = 2
        self.SC_STOP_OPEN_LOOP = 3
        self.SC_END_PRESENT_STIM = 4

        # rotary encoder
        self.WHEEL_DIAMETER = 6.3
        self.RESET_ROTARY_ENCODER = 1
        self.THRESH_LEFT = "RotaryEncoder1_3"
        self.THRESH_RIGHT = "RotaryEncoder1_4"
        self.STIMULUS_LEFT = "RotaryEncoder1_1"
        self.STIMULUS_RIGHT = "RotaryEncoder1_2"

        # stimulus
        self.FPS=120
        self.SCREEN_WIDTH = 6144
        self.SCREEN_HEIGHT = 1536


    def create_time_dict(self):
        """create a dictionary with all the state times for the bpod state machine

        Returns:
            time_dict (dict): dictionary with all the state times
        """        
        time_dict = {
            "time_start": self.usersettings.TIME_START,
            "time_wheel_stopping_check": self.usersettings.TIME_WHEEL_STOPPING_CHECK,
            "time_wheel_stopping_punish": self.usersettings.TIME_WHEEL_STOPPING_PUNISH,
            "time_stim_pres": self.usersettings.TIME_PRESENT_STIM,
            "time_open_loop": self.usersettings.TIME_OPEN_LOOP,
            "time_open_loop_fail_punish": self.usersettings.TIME_OPEN_LOOP_FAIL_PUNISH,
            "time_stim_freez": self.usersettings.TIME_STIM_FREEZ,
            "time_reward": self.usersettings.REWARD_TIME,
            "time_inter_trial": self.usersettings.INTER_TRIAL_TIME,
            "time_big_reward_waiting": (self.usersettings.REWARD_TIME - self.big_reward_open_time),
            "time_small_reward_waiting": (self.usersettings.REWARD_TIME - self.small_reward_open_time),
            "open_time_big_reward": self.big_reward_open_time,
            "open_time_small_reward": self.small_reward_open_time,
            }
        return time_dict

    def create_valve_open_time(self):
        """generate open time for valve for rewards given in ml, depends on BIG_REWARD and SALL_REWARD from usersettings and calibration courfe

        Returns:
            big_open_time (float): valve open time for big reward in ml
            small_open_time (float): valve open time for small reward in ml
        """        
        # ToDo -> add function that takes linear approx from calibaration ad calculates time for given reward in ml 
        big_open_time = self.usersettings.BIG_REWARD
        small_open_time = self.usersettings.SMALL_REWARD
        return big_open_time, small_open_time

    def toJSON(self):
        """create json serialised object from TrialsParameterHandler object

        Returns:
            (json string):
        """        
        return jsonpickle.encode(self, indent=4)

    def update_userinput_file(self):
        """updates usersettings file with new variable values
        """        
        with open(os.path.join(self.path,'usersettings.py'), 'w') as f:
            f.write(
                "\"\"\"specify custom settings for session in this file:\n\n"
                "How to:\n"
                "\tedit values for capital variables\n"
                "\tdo not change capital cariable names\n\n"
                "\"\"\"\n\n"
                "GAMBLE_SIDE = "+json.dumps(self.gamble_side)+"\n\n"
                "# Blocks ========================================================\n"
                "\"\"\"Construct a Block like this:\n"
                "\r{\n"
                "\tTRIAL_NUM_BLOCK: [int, int], #(50 - 80) #will chose a random length in between\n"
                "\tPROB_REWARD_GAMBL_BLOCK: int,  #(0-100)\n"
                "\tprob_reward_save_block: int  #(0-100)\n"
                "},\n"
                "\"\"\"\n\n"
                "BLOCKS = "+json.dumps(self.blocks, indent=4) +"\n\n"
                "#========================================================\n"
                "# reward\n"
                "# big reward in ml\nBIG_REWARD = "+repr(self.big_reward)+"\n"
                "# small rewar in ml\nSMALL_REWARD = "+repr(self.small_reward)+"\n\n"
                "LAST_CALLIBRATION = "+json.dumps(self.last_callibration)+"\n\n"
                "# state machine settings ======================================\n"
                "# waiting time beginning of each trial\n"
                "TIME_START = "+repr(self.time_dict["time_start"])+"\n"
                "# time the wheel has to be stopped\n"
                "TIME_WHEEL_STOPPING_CHECK = "+repr(self.time_dict["time_wheel_stopping_check"])+"\n"
                "# time wait if the wheel is not stopped bevore new trial starts\n"
                "TIME_WHEEL_STOPPING_PUNISH = "+repr(self.time_dict["time_wheel_stopping_punish"])+"\n"
                "# time stimulus is presented but not movable\n"
                "TIME_PRESENT_STIM = "+repr(self.time_dict["time_stim_pres"])+"\n"
                "# time of open loop where wheel moves the stimulus\n"
                "TIME_OPEN_LOOP = "+repr(self.time_dict["time_open_loop"])+"\n"
                "# time wait if stimulus not moved far enough to position\n"
                "TIME_OPEN_LOOP_FAIL_PUNISH = "+repr(self.time_dict["time_open_loop_fail_punish"])+"\n"
                "# time stimulus is presented at reached position but not movable anymore\n"
                "TIME_STIM_FREEZ = "+repr(self.time_dict["time_stim_freez"])+"\n"
                "# time the animal has for the reard = valve open + time after\n"
                "REWARD_TIME ="+repr(self.time_dict["time_reward"])+"\n"
                "# time at end of each trial_num\n"
                "INTER_TRIAL_TIME = "+repr(self.time_dict["time_inter_trial"])+"\n\n"
                "# stimulus ====================================================\nSTIMULUS = "+json.dumps(self.stim)+"\n\n"
                "# rotary Encoder ==============================================\n"
                "\"\"\" Construct thresholds like this:\n"
                "[\n\t-90, 90, # stimulus position in degrees of wheel movement\n"
                "\t-1, 1    # wheel not stoping sthreshold in degrees of wheel movement\n]\n"
                "\"\"\"\n"
                "# threhsolds for event signaling between rotary encoder and bpod\n"
                "ALL_THRESHOLDS = "+json.dumps(self.thresholds,indent=4)+"\n"
                "# speed of movement\nSTIM_END_POS = "+json.dumps(self.stim_end_pos,indent=4)+" # pixel\n"
                "\"\"\"\nend of 1st screen from center = 960 px\nend of 2nd screen from center = 960 + 1920px\n\"\"\"\n\n"
                "LIFE_PLOT = "+repr(self.life_plot)+"\n"
                "# Animal ===================================================\n"
                "# animal waight in grams\nANIMAL_WAIGHT = "+repr(self.animal_waight)+"\n"
                )
