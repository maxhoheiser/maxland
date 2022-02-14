import csv
import json
import os

import system_constants


class TrialParameterHandler:
    """
    class that handles user input and settings for each session

    Args:
        usersettings (object): settings file which loads usersettings input
        settings_folder (path): path to usersettings folder containing usersettings file
        session_folder (path): path to current session folder
    """

    def __init__(self, usersettings, settings_folder, session_folder):
        self.usersettings = usersettings
        self.settings_folder = settings_folder
        self.session_folder = session_folder

        self.task = self.usersettings.TASK
        self.life_plot = self.usersettings.LIFE_PLOT
        # stimulus
        self.stimulus_rad = self.usersettings.STIMULUS_RAD
        self.stimulus_col = self.usersettings.STIMULUS_COL
        self.bg_color = self.usersettings.BACKGROUND_COL

        # specific for gamble task
        if self.task == "gamble":
            self.gamble_side = self.usersettings.GAMBLE_SIDE
            self.gamble_side_left = self.get_is_gamble_side_left()
            self.probability_blocks = self.usersettings.BLOCKS
            self.big_reward = self.usersettings.BIG_REWARD  # reward amount in ml
            self.small_reward = self.usersettings.SMALL_REWARD  # reward amount in ml
            self.manual_reward = None

        # specific for confidentiality task
        if self.task == "conf":
            self.reward = self.usersettings.REWARD
            self.trial_number = self.usersettings.TRIAL_NUMBER
            # stimulus
            self.stimulus_correct_side = self.usersettings.STIMULUS_CORRECT
            self.stimulus_wrong_side = self.usersettings.STIMULUS_WRONG
            self.stimulus_type = self.usersettings.STIMULUS_TYPE
            self.gui_dropdown_list = ("three-stimuli", "two-stimuli", "one-stimulus")

            self.reward = self.usersettings.REWARD
            # insist mode
            self.insist_range_trigger = self.usersettings.RANGE_INSIST_TRIGGER
            self.insist_correct_deactivate = self.usersettings.NUMBER_CORRECT_INSIST_DEACTIVATE
            self.insist_range_deactivate = self.usersettings.RANGE_INSIST_DEACTIVATE
            # rule switching
            self.rule_switch_initial_trials_wait = self.usersettings.RULE_SWITCH_INITIAL_WAIT
            self.rule_switch_trial_check_range = self.usersettings.RULE_SWITCH_RANGE
            self.rule_switch_trials_correct_trigger_switch = self.usersettings.RULE_SWITCH_CORRECT
            # fade away box
            self.fade_start = self.usersettings.FADE_START  # from center to left side where fade away starts
            self.fade_end = self.usersettings.FADE_END  # from left center to left side where fade away ends

        self.time_dict = self.create_time_dictionary()

        self.last_callibration = self.usersettings.LAST_CALLIBRATION
        self.rotaryencoder_thresholds = self.usersettings.ALL_THRESHOLDS
        self.rotaryencoder_stimulus_end_pos = self.usersettings.STIMULUS_END_POS

        # animal variables
        self.animal_weight = self.usersettings.ANIMAL_WEIGHT
        self.animal_weight_after = None

        # system settings for each session
        self.soft_code_present_stimulus = system_constants.SOFT_CODE_PRESENT_STIMULUS
        self.soft_code_start_open_loop = system_constants.SOFT_CODE_START_OPEN_LOOP
        self.soft_code_stop_open_loop = system_constants.SOFT_CODE_STOP_OPEN_LOOP
        self.soft_code_end_present_stimulus = system_constants.SOFT_CODE_END_PRESENT_STIMULUS
        self.soft_code_start_logging = system_constants.SOFT_CODE_START_LOGGING
        self.soft_code_end_logging = system_constants.SOFT_CODE_END_LOGGING
        self.soft_code_stop_close_loop = system_constants.SOFT_CODE_STOP_CLOSE_LOOP
        # rotary encoder
        self.wheel_diameter = system_constants.WHEEL_DIAMETER
        self.reset_rotary_encoder = system_constants.RESET_ROTARY_ENCODER
        self.thresh_left = system_constants.THRESH_LEFT
        self.thresh_right = system_constants.THRESH_RIGHT
        self.stimulus_left = system_constants.STIMULUS_LEFT
        self.stimulus_right = system_constants.STIMULUS_RIGHT
        self.wheel_position = []
        # stimulus
        self.fps = system_constants.FPS
        self.screen_width = system_constants.SCREEN_WIDTH
        self.screen_height = system_constants.SCREEN_HEIGHT
        self.monitor_distance = system_constants.MONITOR_DISTANCE
        self.monitor_width = system_constants.MONITOR_WIDTH
        self.stimulus_position = []
        # tkinter settings
        self.run_session = False
        self.notes = None

    def update_reward_time(self):
        if self.task == "gamble":
            if self.time_dict["time_reward"] < self.time_dict["time_big_reward_open"]:
                self.time_dict["time_reward"] = self.time_dict["time_big_reward_open"]
            if self.time_dict["time_reward"] < self.time_dict["time_small_reward_open"]:
                self.time_dict["time_reward"] = self.time_dict["time_small_reward_open"]
        if self.task == "conf":
            if self.time_dict["time_reward"] < self.time_dict["time_reward_open"]:
                self.time_dict["time_reward"] = self.time_dict["time_reward_open"]

    def update_waiting_times(self):
        if self.task == "gamble":
            self.time_dict["time_big_reward_waiting"] = (
                self.time_dict["time_reward"] - self.time_dict["time_big_reward_open"]
            )
            self.time_dict["time_small_reward_waiting"] = (
                self.time_dict["time_reward"] - self.time_dict["time_small_reward_open"]
            )
        if self.task == "conf":
            self.time_dict["time_reward_waiting"] = self.time_dict["time_reward"] - self.time_dict["time_reward_open"]

    def update_parameters(self):
        if self.task == "gamble":
            # update valve open times
            self.time_dict["time_big_reward_open"] = self.get_valve_open_time(self.big_reward)
            self.time_dict["time_small_reward_open"] = self.get_valve_open_time(self.small_reward)
            self.update_reward_time()
            self.update_waiting_times()
            self.gamble_side_left = self.get_is_gamble_side_left()
        if self.task == "conf":
            self.time_dict["time_reward_open"] = self.get_valve_open_time(self.reward)
            self.update_reward_time()
            self.update_waiting_times()
            # check insist deactivate range and number
            if self.insist_range_deactivate < self.insist_correct_deactivate:
                self.insist_range_deactivate = self.insist_correct_deactivate

    def min_inter_trial_time(self):
        """for the stimulus pygame to run smoothly there has to be a minimum
        time of 1 second between the end of the open loop
        and the change of the flag which quits the pygame and resets it
        """
        minimum_time_after_open_loop = self.time_dict["time_inter_trial"] + self.time_dict["time_open_loop_fail_punish"]
        if minimum_time_after_open_loop < 1.5:
            self.time_dict["time_inter_trial"] = 1.5 - minimum_time_after_open_loop

    def get_valve_open_time(self, time):
        """generate open time for valve for rewards given in ml, depends on
        BIG_REWARD and SMALL_REWARD from usersettings and calibration curve

        Returns:
            open_time (float): valve open time for big reward in ml
        """
        open_time = time
        return open_time

    def to_json(self):
        """create a json serialized object from TrialParameterHandler

        Returns:
            string: json serialized string from TrialsParameterHandler object
        """
        environment_variables = self.__dict__
        if "usersettings" in environment_variables.keys():
            del environment_variables["usersettings"]
        return json.dumps(environment_variables, indent=4)

    def del_from_dict(self, all_keys, dictionary):
        """remove all_keys from dictionary before createing serialized string from self

        Args:
            all_keys (list): list of keys to remove from dictionary
            dictionary (dict): dictionary to remove keys from

        Returns:
            dict: dictionary without keys == all_keys
        """
        new_dictionary = dictionary.copy()
        for key in all_keys:
            if key in new_dictionary.keys():
                del new_dictionary[key]
        return new_dictionary

    def save_usersettings(self, session_name):
        """save usersettings to file session_usersettings.json in current session folder

        Args:
            session_name (string): name of current bpod session
        """
        file_name = session_name + "_settings_obj.json"
        file_path = os.path.join(self.session_folder, file_name)
        del_keys = [
            "usersettings",
            "stimulus_position",
            "wheel_position",
        ]
        dictionary = self.del_from_dict(del_keys, self.__dict__)
        with open(file_path, "w") as f:
            json.dump(dictionary, f, indent=4)

    def update_wheel_position_log(self, log):
        self.wheel_position.append(log)

    def update_stimulus_log(self, log):
        self.stimulus_position.append(log)

    def save_wheel_movement(self, session_name):
        """save wheel movement log to file session_wheel_movement.csv

        Args:
            session_name (string): name of current bpod session
        """
        file_name = session_name + "_wheel_movement.csv"
        file_path = os.path.join(self.session_folder, file_name)
        with open(file_path, "w") as f:
            csv.writer(f).writerows(self.wheel_position)

    def save_stimulus_postition(self, session_name):
        """save stimulus position log to file session_stimulus_position.csv

        Args:
            session_name (string): name of current bpod session
        """
        file_name = session_name + "_stimulus_position.json"
        file_path = os.path.join(self.session_folder, file_name)
        with open(file_path, "w") as f:
            json.dump(self.stimulus_position, f, indent=4)

    def get_is_gamble_side_left(self):
        if self.gamble_side == "Left":
            return True
        else:
            return False

    def create_time_dictionary(self):
        """create a dictionary with all the state times for the bpod state machine for the gamble task

        Returns:
            time_dict (dict): dictionary with all the state times
        """

        time_dict = {
            "time_start": self.usersettings.TIME_START,
            "time_wheel_stopping_check": self.usersettings.TIME_WHEEL_STOPPING_CHECK,
            "time_wheel_stopping_punish": self.usersettings.TIME_WHEEL_STOPPING_PUNISH,
            "time_stimulus_presentation": self.usersettings.TIME_PRESENT_STIMULUS,
            "time_open_loop": self.usersettings.TIME_OPEN_LOOP,
            "time_open_loop_fail_punish": self.usersettings.TIME_OPEN_LOOP_FAIL_PUNISH,
            "time_stimulus_freeze": self.usersettings.TIME_STIMULUS_FREEZE,
            "time_reward": self.usersettings.TIME_REWARD,
            "time_inter_trial": self.usersettings.INTER_TRIAL_TIME,
        }

        if self.task == "gamble":
            gamble_times = {
                "time_no_reward": self.usersettings.TIME_NO_REWARD,
                "time_big_reward_open": self.get_valve_open_time(self.big_reward),
                "time_small_reward_open": self.get_valve_open_time(self.small_reward),
                "time_big_reward_waiting": (self.usersettings.TIME_REWARD - self.get_valve_open_time(self.big_reward)),
                "time_small_reward_waiting": (
                    self.usersettings.TIME_REWARD - self.get_valve_open_time(self.small_reward)
                ),
            }
            time_dict.update(gamble_times)

        if self.task == "conf":
            conf_time = {
                "time_range_no_reward_punish": self.usersettings.TIME_RANGE_OPEN_LOOP_WRONG_PUNISH,
                "time_reward_waiting": (self.usersettings.TIME_REWARD - self.get_valve_open_time(self.reward)),
            }
            time_dict.update(conf_time)

        return time_dict

    def update_userinput_file_gamble(self):
        """updates usersettings file with new variable values"""
        with open(os.path.join(self.settings_folder, "usersettings.py"), "w") as f:
            f.write(
                'task="gamble"\n'
                '"""specify custom settings for session in this file:\n\n'
                "How to:\n"
                "\tedit values for capital variables\n"
                "\tdo not change capital variable names\n\n"
                '"""\n\n'
                "GAMBLE_SIDE = " + json.dumps(self.gamble_side) + "\n\n"
                "# Blocks ========================================================\n"
                '"""Construct a Block like this:\n'
                "\r{\n"
                "\tTRIAL_NUM_BLOCK: [int, int], #(50 - 80) #will chose a random length in between\n"
                "\tPROB_REWARD_GAMBLE_BLOCK: int,  #(0-100)\n"
                "\tprob_reward_save_block: int  #(0-100)\n"
                "},\n"
                '"""\n\n'
                "BLOCKS = " + json.dumps(self.probability_blocks, indent=4) + "\n\n"
                "#========================================================\n"
                "# reward\n"
                # "# big reward in ml\nBIG_REWARD = "+repr(self.big_reward)+"\n"
                "# big reward in ml\nBIG_REWARD = " + repr(self.big_reward) + "\n"
                "# small reward in ml\nSMALL_REWARD = " + repr(self.small_reward) + "\n\n"
                "LAST_CALLIBRATION = " + json.dumps(self.last_callibration) + "\n\n"
                "# state machine settings ======================================\n"
                "# waiting time beginning of each trial\n"
                "TIME_START = " + repr(self.time_dict["time_start"]) + "\n"
                "# time the wheel has to be stopped\n"
                "TIME_WHEEL_STOPPING_CHECK = " + repr(self.time_dict["time_wheel_stopping_check"]) + "\n"
                "# time wait if the wheel is not stopped before new trial starts\n"
                "TIME_WHEEL_STOPPING_PUNISH = " + repr(self.time_dict["time_wheel_stopping_punish"]) + "\n"
                "# time stimulus is presented but not movable\n"
                "TIME_PRESENT_STIMULUS = " + repr(self.time_dict["time_stimulus_presentation"]) + "\n"
                "# time of open loop where wheel moves the stimulus\n"
                "TIME_OPEN_LOOP = " + repr(self.time_dict["time_open_loop"]) + "\n"
                "# time wait if stimulus not moved far enough to position\n"
                "TIME_OPEN_LOOP_FAIL_PUNISH = " + repr(self.time_dict["time_open_loop_fail_punish"]) + "\n"
                "# time stimulus is presented at reached position but not movable anymore\n"
                "TIME_STIMULUS_FREEZE = " + repr(self.time_dict["time_stimulus_freeze"]) + "\n"
                "# time the animal has for the reward = valve open + time after\n"
                "TIME_REWARD = " + repr(self.time_dict["time_reward"]) + "\n"
                "# no reward time\n"
                "TIME_NO_REWARD = " + repr(self.time_dict["time_no_reward"]) + "\n"
                "# time at end of each trial_num\n"
                "INTER_TRIAL_TIME = " + repr(self.time_dict["time_inter_trial"]) + "\n\n"
                "# stimulus size and color - only for moving stimulus\n"
                "STIMULUS_RAD = " + json.dumps(self.stimulus_rad) + " # pixel radius of stimulus\n"
                "STIMULUS_COL = " + json.dumps(self.stimulus_col) + " #color of stimulus\n\n"
                "BACKGROUND_COL = " + json.dumps(self.bg_color) + " #-1,-1,-1 for black\n"
                "# rotary Encoder ==============================================\n"
                '""" Construct thresholds like this:\n'
                "[\n\t-90, 90, # stimulus position in degrees of wheel movement\n"
                "\t-1, 1    # wheel not stoping threshold in degrees of wheel movement\n]\n"
                '"""\n'
                "# thresholds for event signaling between rotary encoder and bpod\n"
                "ALL_THRESHOLDS = " + json.dumps(self.rotaryencoder_thresholds, indent=4) + "\n"
                "# speed of movement\nSTIMULUS_END_POS = "
                + json.dumps(self.rotaryencoder_stimulus_end_pos, indent=4)
                + " # pixel\n"
                '"""\nend of 1st Screen from center = 960 px\nend of 2nd Screen from center = 960 + 1920px\n"""\n\n'
                "LIFE_PLOT = " + repr(self.life_plot) + "\n"
                "# Animal ===================================================\n"
                "# animal weight in grams\nANIMAL_WEIGHT = " + repr(self.animal_weight) + "\n"
            )

    def update_userinput_file_conf(self):
        """updates usersettings file with new variable values"""
        with open(os.path.join(self.settings_folder, "usersettings.py"), "w") as f:
            f.write(
                "task = 'conf'\n\n"
                '"""specify custom settings for session in this file:\n\n'
                "How to:\n"
                "\tedit values for capital variables\n"
                '\tdo not change capital variable names\n\n"""\n'
                "# stimulus ====================================================\n"
                "#grating_SF = 0.25  # 4 cycles per degree visual angle\n"
                "#grating_ori = 0   # in degree\n\n"
                "STIMULUS_CORRECT = " + json.dumps(self.stimulus_correct_side) + "\n\n"
                "STIMULUS_WRONG = " + json.dumps(self.stimulus_wrong_side) + "\n\n"
                "# trials\n"
                "TRIAL_NUMBER = " + json.dumps(self.trial_number) + "\n\n"
                "# stimulus size and color - only for moving stimulus\n"
                "STIMULUS_RAD = " + json.dumps(self.stimulus_rad) + " # pixel radius of stimulus\n"
                "STIMULUS_COL = " + json.dumps(self.stimulus_col) + "#color of stimulus\n\n"
                "BACKGROUND_COL = " + json.dumps(self.bg_color) + "#-1,-1,-1 for black\n"
                "STIMULUS_TYPE = " + json.dumps(self.stimulus_type) + " #three-stimuli #two-stimuli #one-stimulus\n"
                "\n#===============================================================\n"
                "# reward in ml\n"
                "REWARD = " + json.dumps(self.reward) + "\n\n"
                "LAST_CALLIBRATION = " + json.dumps(self.last_callibration) + "\n\n"
                "# state machine settings =======================================\n"
                "# waiting time beginning of each trial\n"
                "TIME_START = " + repr(self.time_dict["time_start"]) + "\n"
                "# time the wheel has to be stopped\n"
                "TIME_WHEEL_STOPPING_CHECK = " + repr(self.time_dict["time_wheel_stopping_check"]) + "\n"
                "# time wait if the wheel is not stopped before new trial starts\n"
                "TIME_WHEEL_STOPPING_PUNISH = " + repr(self.time_dict["time_wheel_stopping_punish"]) + "\n"
                "# time stimulus is presented but not movable\n"
                "TIME_PRESENT_STIMULUS = " + repr(self.time_dict["time_stimulus_presentation"]) + "\n"
                "# time of open loop where wheel moves the stimulus\n"
                "TIME_OPEN_LOOP = " + repr(self.time_dict["time_open_loop"]) + "\n"
                "# time wait if stimulus not moved far enough to position\n"
                "TIME_OPEN_LOOP_FAIL_PUNISH = " + repr(self.time_dict["time_open_loop_fail_punish"]) + "\n"
                "# time stimulus is presented at reached position but not movable anymore\n"
                "TIME_STIMULUS_FREEZE = " + repr(self.time_dict["time_stimulus_freeze"]) + "\n"
                "# time the animal has for the reward = valve open + time after\n"
                "TIME_REWARD =" + repr(self.time_dict["time_reward"]) + "\n"
                "# no reward time\n"
                "TIME_RANGE_OPEN_LOOP_WRONG_PUNISH = " + repr(self.time_dict["time_range_no_reward_punish"]) + "\n"
                "# time at end of each trial_num\n"
                "INTER_TRIAL_TIME = " + repr(self.time_dict["time_inter_trial"]) + "\n\n"
                "# Insist Mode =================================================\n"
                "RANGE_INSIST_TRIGGER = " + json.dumps(self.insist_range_trigger) + "\n"
                "NUMBER_CORRECT_INSIST_DEACTIVATE = " + json.dumps(self.insist_range_deactivate) + "\n"
                "RANGE_INSIST_DEACTIVATE = " + json.dumps(self.insist_correct_deactivate) + "\n\n\n"
                "# Rule Switching Mode =========================================\n"
                "RULE_SWITCH_INITIAL_WAIT = "
                + json.dumps(self.rule_switch_initial_trials_wait)
                + " # wait for n trials before checking for rule switching\n"
                "RULE_SWITCH_RANGE = "
                + json.dumps(self.rule_switch_trial_check_range)
                + "# range of trials for checking for rule switching\n"
                "RULE_SWITCH_CORRECT = "
                + json.dumps(self.rule_switch_trials_correct_trigger_switch)
                + "# number of correct trials for rule switching\n\n"
                "# Fade away ===================================================\n"
                "FADE_START = "
                + repr(self.fade_start)
                + " # from center to left side where stimulus fade away begins\n"
                "FADE_END = " + repr(self.fade_end) + " # from center to left side where stimulus fade away ends\n\n"
                "# rotary Encoder ==============================================\n"
                '""" Construct thresholds like this:\n'
                "[\n\t-90, 90, # stimulus position in degrees of wheel movement\n"
                "\t-1, 1    # wheel not stoping threshold in degrees of wheel movement\n]\n"
                '"""\n'
                "# thresholds for event signaling between rotary encoder and bpod\n"
                "ALL_THRESHOLDS = " + json.dumps(self.rotaryencoder_thresholds, indent=4) + "\n"
                "# speed of movement\nSTIMULUS_END_POS = "
                + json.dumps(self.rotaryencoder_stimulus_end_pos, indent=4)
                + " # pixel\n"
                '"""\nend of 1st screen from center = 960 px\nend of 2nd screen from center = 960 + 1920px\n"""\n\n'
                "LIFE_PLOT = " + repr(self.life_plot) + "\n"
                "# Animal ===================================================\n"
                "# animal weight in grams\nANIMAL_WEIGHT = " + json.dumps(self.animal_weight) + "\n"
            )
