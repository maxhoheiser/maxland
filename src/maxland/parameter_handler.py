import csv
import json
import os
import random
from typing import Dict, List

import maxland.system_constants as system_constants
from maxland.types_rule_definition import Rule, RuleDefinitionType, RuleType
from maxland.types_stimuli_definition import Stimulus, StimulusType
from maxland.types_time_dict import TimeDict
from maxland.types_usersettings import (
    GambleSide,
    StageName,
    TaskName,
    UsersettingsTypes,
)


class TrialParameterHandler:
    """
    class that handles user input and settings for each session

    Args:
        usersettings (object): settings file which loads usersettings input
        settings_folder (path): path to usersettings folder containing usersettings file
        session_folder (path): path to current session folder
    """

    def __init__(self, usersettings: UsersettingsTypes, settings_folder, session_folder):
        self.usersettings = usersettings
        self.settings_folder = settings_folder
        self.session_folder = session_folder

        self.task_name = self.usersettings.TASK
        self.stage = self.usersettings.STAGE
        self.life_plot = self.usersettings.LIFE_PLOT
        # stimulus
        self.stimulus_radius = self.usersettings.STIMULUS_RADIUS
        self.stimulus_color = self.usersettings.STIMULUS_COLOR
        self.background_color = self.usersettings.BACKGROUND_COLOR

        # specific for gamble task
        if self.task_name == TaskName.GAMBLE:
            self.gamble_side = self.usersettings.GAMBLE_SIDE
            self.is_gamble_side_left = self.get_is_gamble_side_left()
            self.blocks = self.usersettings.BLOCKS
            self.big_reward = self.usersettings.BIG_REWARD  # reward amount in ml
            self.small_reward = self.usersettings.SMALL_REWARD  # reward amount in ml
            self.manual_reward: int = int()

        # specific for confidentiality task
        if self.task_name == TaskName.CONFIDENTIALITY:
            self.reward = self.usersettings.REWARD
            self.trial_number = self.usersettings.TRIAL_NUMBER
            self.stimulus_type = self.usersettings.STIMULUS_TYPE
            self.gui_dropdown_list = ("three-stimuli", "two-stimuli", "one-stimulus")

            if self.stage == StageName.HABITUATION or self.stage == StageName.TRAINING:
                # stimulus correct and wrong predefined
                self.stimulus_correct_side = self.usersettings.STIMULUS_CORRECT
                self.stimulus_wrong_side = self.usersettings.STIMULUS_WRONG

            if self.stage == StageName.TRAINING_COMPLEX:
                # rule_a and rule_b defined
                self.rule_a_definition = self.usersettings.RULE_A
                self.rule_b_definition = self.usersettings.RULE_B
                self.stimulus_defintion = self.get_stimuli_definitions(self.settings_folder)
                self.rule_a = self.get_rule_from_rule_definition_and_stimuli_definition(self.rule_a_definition, self.stimulus_defintion)
                self.rule_b = self.get_rule_from_rule_definition_and_stimuli_definition(self.rule_b_definition, self.stimulus_defintion)
                self.rule_active = self.rule_a

                self.stimulus_correct_side, self.stimulus_wrong_side = self.get_stimuli_from_rule_for_current_trial(self.rule_active)

            self.reward = self.usersettings.REWARD
            # insist mode
            self.insist_range_trigger = self.usersettings.INSIST_RANGE_TRIGGER
            self.insist_correct_deactivate = self.usersettings.INSIST_CORRECT_DEACTIVATE
            self.insist_range_deactivate = self.usersettings.INSIST_RANGE_DEACTIVATE
            # rule switching
            self.rule_switch_initial_trials_wait = self.usersettings.RULE_SWITCH_INITIAL_TRIALS_WAIT
            self.rule_switch_check_trial_range = self.usersettings.RULE_SWITCH_CHECK_TRIAL_RANGE
            self.rule_switch_trials_correct_trigger_switch = self.usersettings.RULE_SWITCH_TRIALS_CORRECT_TRIGGER_SWITCH
            # fade away box
            self.fade_start = self.usersettings.FADE_START  # from center to left side where fade away starts
            self.fade_end = self.usersettings.FADE_END  # from left center to left side where fade away ends

        self.time_dict: TimeDict = self.create_time_dictionary()

        self.last_callibration = self.usersettings.LAST_CALLIBRATION
        self.rotaryencoder_thresholds = self.usersettings.ROTARYENCODER_THRESHOLDS
        self.stimulus_end_position = self.usersettings.STIMULUS_END_POSITION

        # animal variables
        self.animal_weight = self.usersettings.ANIMAL_WEIGHT
        self.animal_weight_after: int = int()

        # system settings for each session
        self.soft_code_present_stimulus = system_constants.SOFT_CODE_PRESENT_STIMULUS
        self.soft_code_start_open_loop = system_constants.SOFT_CODE_START_OPEN_LOOP
        self.soft_code_stop_open_loop = system_constants.SOFT_CODE_STOP_OPEN_LOOP
        self.soft_code_end_present_stimulus = system_constants.SOFT_CODE_END_PRESENT_STIMULUS
        self.soft_code_start_logging = system_constants.SOFT_CODE_START_LOGGING
        self.soft_code_end_logging = system_constants.SOFT_CODE_END_LOGGING
        self.soft_code_stop_close_loop = system_constants.SOFT_CODE_STOP_CLOSE_LOOP
        self.soft_code_wheel_not_stopping = system_constants.SOFT_CODE_WHEEL_NOT_STOPPING
        # rotary encoder
        self.wheel_diameter = system_constants.WHEEL_DIAMETER
        self.serial_message_reset_rotary_encoder = system_constants.SERIAL_MESSAGE_RESET_ROTARY_ENCODER
        self.rotaryencoder_thresholds = self.usersettings.ROTARYENCODER_THRESHOLDS
        self.rotaryencoder_stimulus_end_pos = self.usersettings.STIMULUS_END_POSITION
        self.rotary_encoder_threshhold_left = system_constants.ROTARY_ENCODER_THRESHHOLD_LEFT
        self.rotary_encoder_threshhold_right = system_constants.ROTARY_ENCODER_THRESHHOLD_RIGHT
        self.stimulus_threshold_left = system_constants.STIMULUS_THRESHOLD_LEFT
        self.stimulus_threshold_right = system_constants.STIMULUS_THRESHOLD_RIGHT
        self.wheel_position = List[float]
        # stimulus
        self.fps = system_constants.FPS
        self.screen_width = system_constants.SCREEN_WIDTH
        self.screen_height = system_constants.SCREEN_HEIGHT
        self.monitor_distance = system_constants.MONITOR_DISTANCE
        self.monitor_width = system_constants.MONITOR_WIDTH
        self.stimulus_position = List[float]
        # tkinter settings
        self.run_session = False
        self.notes: str = ""
        # probability
        self.probability_list: List[Dict[str, bool]] = list()
        # historic trial values
        self.chosen_sides_history: List[str] = list()
        self.trials_correct_side_history: List[bool] = list()
        self.time_punish_history: List[float] = list()
        self.insist_mode_history: List[str] = list()
        self.active_rule_history: List[str] = list()

    def update_reward_time(self):
        if self.task_name == "gamble":
            if self.time_dict["time_reward"] < self.time_dict["time_big_reward_open"]:
                self.time_dict["time_reward"] = self.time_dict["time_big_reward_open"]
            if self.time_dict["time_reward"] < self.time_dict["time_small_reward_open"]:
                self.time_dict["time_reward"] = self.time_dict["time_small_reward_open"]
        if self.task_name == "conf":
            if self.time_dict["time_reward"] < self.time_dict["time_reward_open"]:
                self.time_dict["time_reward"] = self.time_dict["time_reward_open"]

    def update_waiting_times(self):
        if self.task_name == "gamble":
            self.time_dict["time_big_reward_waiting"] = self.time_dict["time_reward"] - self.time_dict["time_big_reward_open"]
            self.time_dict["time_small_reward_waiting"] = self.time_dict["time_reward"] - self.time_dict["time_small_reward_open"]
        if self.task_name == "conf":
            self.time_dict["time_reward_waiting"] = self.time_dict["time_reward"] - self.time_dict["time_reward_open"]

    def update_parameters(self):
        if self.task_name == "gamble":
            # update valve open times
            self.time_dict["time_big_reward_open"] = self.get_valve_open_time(self.big_reward)
            self.time_dict["time_small_reward_open"] = self.get_valve_open_time(self.small_reward)
            self.update_reward_time()
            self.update_waiting_times()
            self.is_gamble_side_left = self.get_is_gamble_side_left()
        if self.task_name == "conf":
            self.time_dict["time_reward_open"] = self.get_valve_open_time(self.reward)
            self.update_reward_time()
            self.update_waiting_times()
            # check insist deactivate range and number
            if self.insist_range_deactivate < self.insist_correct_deactivate:
                self.insist_range_deactivate = self.insist_correct_deactivate

    def set_min_time_inter_trial(self):
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
        if self.gamble_side == GambleSide.LEFT:
            return True
        else:
            return False

    def create_time_dictionary(self):
        """create a dictionary with all the state times for the bpod state machine for the gamble task

        Returns:
            time_dict (dict): dictionary with all the state times
        """

        time_dict_construction = {
            "time_start": self.usersettings.TIME_START,
            "time_wheel_stopping_check": self.usersettings.TIME_WHEEL_STOPPING_CHECK,
            "time_wheel_stopping_punish": self.usersettings.TIME_WHEEL_STOPPING_PUNISH,
            "time_present_stimulus": self.usersettings.TIME_PRESENT_STIMULUS,
            "time_open_loop": self.usersettings.TIME_OPEN_LOOP,
            "time_open_loop_fail_punish": self.usersettings.TIME_OPEN_LOOP_FAIL_PUNISH,
            "time_stimulus_freeze": self.usersettings.TIME_STIMULUS_FREEZE,
            "time_reward": self.usersettings.TIME_REWARD,
            "time_inter_trial": self.usersettings.TIME_INTER_TRIAL,
        }

        if self.task_name == "gamble":
            gamble_times = {
                "time_no_reward": self.usersettings.TIME_NO_REWARD,
                "time_big_reward_open": self.get_valve_open_time(self.big_reward),
                "time_small_reward_open": self.get_valve_open_time(self.small_reward),
                "time_big_reward_waiting": (self.usersettings.TIME_REWARD - self.get_valve_open_time(self.big_reward)),
                "time_small_reward_waiting": (self.usersettings.TIME_REWARD - self.get_valve_open_time(self.small_reward)),
                # add placeholder for
            }
            time_dict_construction.update(gamble_times)

        if self.task_name == "conf":
            conf_time = {
                "time_range_no_reward_punish": self.usersettings.TIME_RANGE_NO_REWARD_PUNISH,
                "time_reward_waiting": (self.usersettings.TIME_REWARD - self.get_valve_open_time(self.reward)),
                "time_reward_open": self.get_valve_open_time(self.reward),
            }
            time_dict_construction.update(conf_time)

        time_dict: TimeDict = time_dict_construction

        return time_dict

    def get_punish_time(self):
        punish_time = round(
            random.uniform(
                float(self.time_dict["time_range_no_reward_punish"][0]),
                float(self.time_dict["time_range_no_reward_punish"][1]),
            ),
            2,
        )
        self.time_punish_history.append(punish_time)
        return punish_time

    def update_userinput_file_gamble(self):
        """updates usersettings file with new variable values"""
        with open(os.path.join(self.settings_folder, "usersettings.py"), "w") as f:
            f.write(
                'TASK = "gamble"\n\n'
                "STAGE = " + json.dumps(self.stage) + "\n"
                "GAMBLE_SIDE = " + json.dumps(self.gamble_side) + "\n"
                "BLOCKS = " + json.dumps(self.blocks) + "\n\n"
                "# reward in seconds\n"
                "BIG_REWARD = " + repr(self.big_reward) + "\n"
                "SMALL_REWARD = " + repr(self.small_reward) + "\n\n"
                "LAST_CALLIBRATION = " + json.dumps(self.last_callibration) + "\n\n"
                "# trial times\n"
                "TIME_START = " + repr(self.time_dict["time_start"]) + "\n"
                "TIME_WHEEL_STOPPING_CHECK = " + repr(self.time_dict["time_wheel_stopping_check"]) + "\n"
                "TIME_WHEEL_STOPPING_PUNISH = " + repr(self.time_dict["time_wheel_stopping_punish"]) + "\n"
                "TIME_PRESENT_STIMULUS = " + repr(self.time_dict["time_present_stimulus"]) + "\n"
                "TIME_OPEN_LOOP = " + repr(self.time_dict["time_open_loop"]) + "\n"
                "TIME_OPEN_LOOP_FAIL_PUNISH = " + repr(self.time_dict["time_open_loop_fail_punish"]) + "\n"
                "TIME_STIMULUS_FREEZE = " + repr(self.time_dict["time_stimulus_freeze"]) + "\n"
                "TIME_REWARD = " + repr(self.time_dict["time_reward"]) + "\n"
                "TIME_NO_REWARD = " + repr(self.time_dict["time_no_reward"]) + "\n"
                "TIME_INTER_TRIAL = " + repr(self.time_dict["time_inter_trial"]) + "\n\n"
                "# stimulus size and color - only for moving stimulus\n"
                "STIMULUS_RADIUS = " + json.dumps(self.stimulus_radius) + " # pixel radius of stimulus\n"
                "STIMULUS_COLOR = " + json.dumps(self.stimulus_color) + " #color of stimulus\n"
                "BACKGROUND_COLOR = " + json.dumps(self.background_color) + "\n\n"
                "# thresholds\n"
                "ROTARYENCODER_THRESHOLDS = " + json.dumps(self.rotaryencoder_thresholds) + "\n"
                "STIMULUS_END_POSITION = " + json.dumps(self.stimulus_end_position) + " # pixel\n\n"
                "LIFE_PLOT = " + repr(self.life_plot) + "\n"
                "# animal weight in grams\n"
                "ANIMAL_WEIGHT = " + repr(self.animal_weight) + "\n\n"
            )

    def update_userinput_file_conf(self):
        """updates usersettings file with new variable values"""
        with open(os.path.join(self.settings_folder, "usersettings.py"), "w") as f:
            f.write(
                'TASK = "conf"\n'
                "STAGE = " + json.dumps(self.stage) + "\n\n"
                "TRIAL_NUMBER = " + json.dumps(self.trial_number) + "\n"
                "STIMULUS_TYPE = " + json.dumps(self.stimulus_type) + " #three-stimuli #two-stimuli #one-stimulus\n"
            )
            if self.stage == StageName.HABITUATION or StageName.HABITUATION_COMPLEX or self.stage == StageName.TRAINING:
                f.write(
                    "STIMULUS_CORRECT = " + json.dumps(self.stimulus_correct_side) + "\n"
                    "STIMULUS_WRONG = " + json.dumps(self.stimulus_wrong_side) + "\n\n"
                )
            if self.stage == StageName.TRAINING_COMPLEX:
                f.write("RULE_A = " + str(self.rule_a_definition) + "\n\n" "RULE_B = " + str(self.rule_b_definition) + "\n\n")
            f.write(
                "# reward in seconds\n"
                "REWARD = " + json.dumps(self.reward) + "\n"
                "LAST_CALLIBRATION = " + json.dumps(self.last_callibration) + "\n\n"
                "# trial times\n"
                "TIME_START = " + repr(self.time_dict["time_start"]) + "\n"
                "TIME_WHEEL_STOPPING_CHECK = " + repr(self.time_dict["time_wheel_stopping_check"]) + "\n"
                "TIME_WHEEL_STOPPING_PUNISH = " + repr(self.time_dict["time_wheel_stopping_punish"]) + "\n"
                "TIME_PRESENT_STIMULUS = " + repr(self.time_dict["time_present_stimulus"]) + "\n"
                "TIME_OPEN_LOOP = " + repr(self.time_dict["time_open_loop"]) + "\n"
                "TIME_OPEN_LOOP_FAIL_PUNISH = " + repr(self.time_dict["time_open_loop_fail_punish"]) + "\n"
                "TIME_STIMULUS_FREEZE = " + repr(self.time_dict["time_stimulus_freeze"]) + "\n"
                "TIME_REWARD = " + repr(self.time_dict["time_reward"]) + "\n"
                "TIME_RANGE_NO_REWARD_PUNISH = " + repr(self.time_dict["time_range_no_reward_punish"]) + "\n"
                "TIME_INTER_TRIAL = " + repr(self.time_dict["time_inter_trial"]) + "\n\n"
                "# insist mode\n"
                "INSIST_RANGE_TRIGGER = " + json.dumps(self.insist_range_trigger) + "\n"
                "INSIST_CORRECT_DEACTIVATE = " + json.dumps(self.insist_correct_deactivate) + "\n"
                "INSIST_RANGE_DEACTIVATE = " + json.dumps(self.insist_range_deactivate) + "\n\n"
                "# rule switching\n"
                "RULE_SWITCH_INITIAL_TRIALS_WAIT = " + json.dumps(self.rule_switch_initial_trials_wait) + "\n"
                "RULE_SWITCH_CHECK_TRIAL_RANGE = " + json.dumps(self.rule_switch_check_trial_range) + "\n"
                "RULE_SWITCH_TRIALS_CORRECT_TRIGGER_SWITCH = " + json.dumps(self.rule_switch_trials_correct_trigger_switch) + "\n\n"
                "# fade away \n"
                "FADE_START = " + repr(self.fade_start) + "\n"
                "FADE_END = " + repr(self.fade_end) + "\n\n"
                "# stimulus size and color - only for moving stimulus\n"
                "STIMULUS_RADIUS = " + json.dumps(self.stimulus_radius) + " # pixel radius of stimulus\n"
                "STIMULUS_COLOR = " + json.dumps(self.stimulus_color) + " #color of stimulus\n"
                "BACKGROUND_COLOR = " + json.dumps(self.background_color) + "\n\n"
                "# thresholds\n"
                "ROTARYENCODER_THRESHOLDS = " + json.dumps(self.rotaryencoder_thresholds) + "\n"
                "STIMULUS_END_POSITION = " + json.dumps(self.stimulus_end_position) + " # pixel\n\n"
                "LIFE_PLOT = " + repr(self.life_plot) + "\n"
                "# animal weight in grams\n"
                "ANIMAL_WEIGHT = " + repr(self.animal_weight) + "\n\n"
            )

    # confidentiality training complex
    def get_stimuli_definitions(self, folder):
        with open(os.path.join(folder, "stimuli_definition.json")) as f:
            stimuli_definitions = json.load(f)
        return stimuli_definitions

    def get_stimulus_from_id(self, id, stimulus_definition):
        stimulus: Stimulus = {
            "grating_frequency": stimulus_definition[id]["grating_frequency"],
            "grating_orientation": stimulus_definition[id]["grating_orientation"],
            "grating_size": stimulus_definition[id]["grating_size"],
            "grating_speed": stimulus_definition[id]["grating_speed"],
        }
        return stimulus

    def get_rule_from_rule_definition_and_stimuli_definition(self, rule_definition: RuleDefinitionType, stimulus_definition: StimulusType):
        """
        Returns a rule definition with the stimuli parameters
        :param rule_definition:
        :param stimuli_definitions:
        :return:
        """
        rule: RuleType = list()

        for pair in rule_definition:
            new_pair: Rule = {
                "correct": self.get_stimulus_from_id(pair["correct"], stimulus_definition),
                "wrong": self.get_stimulus_from_id(pair["wrong"], stimulus_definition),
                "conflicting": pair["conflicting"],
                "percentage": pair["percentage"],
            }
            rule.append(new_pair)
        return rule

    def get_stimuli_from_rule_for_current_trial(self, rule):
        """Randomly load a pair of stimuli from the current active rule"""
        random_pair = random.choice(list(rule))
        random_correct = random_pair["correct"]
        random_wrong = random_pair["wrong"]

        return random_correct, random_wrong

    def update_stimuli_from_rule_for_current_trial(self):
        self.stimulus_correct_side, self.stimulus_wrong_side = self.get_stimuli_from_rule_for_current_trial(self.rule_active)
