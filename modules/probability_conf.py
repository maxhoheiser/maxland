
import random
from tasks.confidentiality_task_training_simple.usersettings import RULE_SWITCH_RANGE
import numpy as np


class ProbabilityConstuctor():
    def __init__(self, settings):
        """object to calculate and handle stimulus sides
        Args:
            settings (TrialParameterHandler object): the object for all the session parameters from TrialPArameterHandler
        """
        self.settings = settings
        # initialize random sides
        self.stim_side_dict = dict()
        self.correct_choice = []
        self.current_coice = False
        # insist mode tracking
        self.chosen_sides_li = []
        self.insist_mode_chosen_side_li = []
        self.insist_range_trigger = settings.insist_range_trigger  # range to check for same side
        self.insist_range_deactivate = settings.insist_range_deactivate  # range in which number of correct choices have to occure to deactivate insit mode
        self.insist_correct_deactivate = settings.insist_correct_deactivate  # number of correct choice to deactivate insist mode
        self.insist_mode_active = False
        self.insist_side = None
        # rule switching
        self.rule_switch_initial_wait = settings.rule_switch_initial_wait # trials to wait bevore checking for rule switch
        self.rule_switch_range = settings.rule_switch_range  # range in which the rule switch is activated
        self.rule_switch_correct = settings.rule_switch_correct  # number of correct choices to switch rule
        self.rule_active = "RU0"  # id of active rule switch RU1 active
        self.rule_switch = True # flag to check if rule switch is active - deactivate after first rule switch


    def get_random_side(self):
        # check insist mode
        if self.insist_mode_active:
            if self.insist_side == "left":
                random_right = False
            elif self.insist_side == "right":
                random_right = True
        else:
            random_right = bool(random.getrandbits(1))
        # asign sides to dict
        self.stim_side_dict["right"] = random_right
        self.stim_side_dict["left"] = not(random_right)

    def get_stim_side(self, trial):
        """
        Args:
            trial (Trial object): the current trial object
        Returns:
            current_side (str): the side the stimulus is on
        """
        # get chosen side
        if not np.isnan(trial.states_durations["check_reward_left"][0][0]):
            current_side = "left"
            print("current side: left")
        elif not np.isnan(trial.states_durations["check_reward_right"][0][0]):
            current_side = "right"
            print("current side: right")
        else:
            current_side = "non"
        self.chosen_sides_li.append(current_side)
        # check if current trial side == correct side
        if current_side == "right" and self.stim_side_dict["right"] == True:
            self.correct_choice.append(True)
            self.current_coice = True
        elif current_side == "left" and self.stim_side_dict["left"] == True:
            self.correct_choice.append(True)
            self.current_coice = True
        else:
            self.correct_choice.append(False)
            self.current_coice = False
        return current_side

    def insist_mode_check(self):
        # check for insist mode activate
        if not self.insist_mode_active:
            if len(self.chosen_sides_li) >= self.insist_range_trigger:
                slice = self.chosen_sides_li[-self.insist_range_trigger:]
            else:
                slice = self.chosen_sides_li
            left_num_chosen = sum(map(lambda x: x == "left", slice))
            right_num_chosen = sum(map(lambda x: x == "right", slice))
            if left_num_chosen >= self.insist_range_trigger:
                self.insist_mode_active = True
                self.chosen_sides_li = [] #TODO: if not wanted remove this
                self.insist_side = "right"
                print("\n--------------------------------\n")
                print("INSIST MODE ACTIVATED: insist right")
                print("\n--------------------------------")
            if right_num_chosen >= self.insist_range_trigger:
                self.insist_mode_active = True
                self.chosen_sides_li = [] #TODO: if not wanted remove this
                self.insist_side = "left"
                print("\n--------------------------------\n")
                print("INSIST MODE ACTIVATED: insist left")
                print("\n--------------------------------")
        # deactivate insist mode
        elif self.insist_mode_active:
            self.insist_mode_chosen_side_li.append(current_side)
            # get insist mode slice
            if len(self.insist_mode_chosen_side_li) >= self.insist_range_deactivate:
                slice = self.insist_mode_chosen_side_li[-self.insist_range_deactivate:]
            else:
                slice = self.insist_mode_chosen_side_li
            # check range if correct
            insist_correct_choice = sum(map(lambda x: x == self.insist_side, slice))
            if insist_correct_choice >= self.insist_correct_deactivate:
                self.insist_mode_active = False
                self.insist_side = "none"
                self.inist_mode_chosen_sde = []  # clear last insist mode list
                print("\n--------------------------------\n")
                print("INSIST MODE DEACTIVATED")
                print("\n--------------------------------")

    def rule_switch_check(self,current_trial_num):
        if current_trial_num >= self.rule_switch_initial_wait: # wait initial trials bevore checking for rule switch
            rule_switch_range = self.correct_choice[self.rule_switch_initial_wait:] # only check for rule switch after initial wait
            if len(rule_switch_range) > self.rule_switch_range: #> not >= because trial counter in main states loop starts from 1 not 0
                slice = rule_switch_range[-self.rule_switch_range:]
            else:
                slice = rule_switch_range
            correct_chosen = sum(slice) # get number of correct choices
            # check if rule switch
            if self.rule_switch:
                if correct_chosen >= self.rule_switch_correct:
                    self.rule_active = "RU1" # switch to rule 1
                    self.rule_switch = False # deactivate rule switch
                    print("\n--------------------------------\n")
                    print("\n switch to rule RU1\n")
                    print("\n--------------------------------\n")
                    # invert stimulus configuration
                    bk = self.settings.stimulus_correct.copy()
                    self.settings.stimulus_correct = self.settings.stimulus_wrong.copy()
                    self.settings.stimulus_wrong = bk
