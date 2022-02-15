import random

import numpy as np


class ProbabilityConstructor:
    """
    Module to calculate and handle stimulus sides for the confidentiality task
    Args:
        settings (TrialParameterHandler object): the object for all the session parameters from TrialParameterHandler
    """

    def __init__(self, settings):
        self.settings = settings
        self.stimulus_sides = dict()
        self.trials_correct_side_chosen = []
        self.current_trial_correct_side_chosen = False
        # insist mode tracking
        self.chosen_sides_li = []
        self.insist_mode_chosen_side_li = []
        self.insist_mode_active = False
        self.insist_side = None
        self.active_rule = "RU0"  # id of active rule
        self.is_initial_rule_active = True

    def get_random_side(self):
        # check insist mode
        if self.insist_mode_active:
            if self.insist_side == "left":
                random_right = False
            elif self.insist_side == "right":
                random_right = True
        else:
            random_right = bool(random.getrandbits(1))

        self.stimulus_sides["right"] = random_right
        self.stimulus_sides["left"] = not (random_right)

    def get_stimulus_side(self, trial):
        """
        Args:
            trial (Trial object): the current bpod trial object
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
        if current_side == "right" and self.stimulus_sides["right"] == True:
            self.trials_correct_side_chosen.append(True)
            self.current_trial_correct_side_chosen = True
        elif current_side == "left" and self.stimulus_sides["left"] == True:
            self.trials_correct_side_chosen.append(True)
            self.current_trial_correct_side_chosen = True
        else:
            self.trials_correct_side_chosen.append(False)
            self.current_trial_correct_side_chosen = False
        return current_side

    def insist_mode_check(self):
        # check for insist mode activate
        if not self.insist_mode_active:
            if len(self.chosen_sides_li) >= self.settings.insist_range_trigger:
                slice = self.chosen_sides_li[-self.settings.insist_range_trigger :]
            else:
                slice = self.chosen_sides_li
            left_num_chosen = sum(map(lambda x: x == "left", slice))
            right_num_chosen = sum(map(lambda x: x == "right", slice))
            if left_num_chosen >= self.settings.insist_range_trigger:
                self.insist_mode_active = True
                self.chosen_sides_li = []
                self.insist_side = "right"
                print("\n--------------------------------\n")
                print("INSIST MODE ACTIVATED: insist right")
                print("\n--------------------------------")
            if right_num_chosen >= self.settings.insist_range_trigger:
                self.insist_mode_active = True
                self.chosen_sides_li = []
                self.insist_side = "left"
                print("\n--------------------------------\n")
                print("INSIST MODE ACTIVATED: insist left")
                print("\n--------------------------------")
        # deactivate insist mode
        elif self.insist_mode_active:
            self.insist_mode_chosen_side_li.append(self.chosen_sides_li[-1])
            print(self.chosen_sides_li)
            print(self.insist_mode_chosen_side_li)
            # get insist mode slice
            if len(self.insist_mode_chosen_side_li) >= self.settings.insist_range_deactivate:
                slice = self.insist_mode_chosen_side_li[-self.settings.insist_range_deactivate :]
            else:
                slice = self.insist_mode_chosen_side_li
            # check range if correct
            insist_correct_choice = sum(map(lambda x: x == self.insist_side, slice))
            if insist_correct_choice >= self.settings.insist_correct_deactivate:
                self.insist_mode_active = False
                self.insist_side = "none"
                self.insist_mode_chosen_side_li = []  # clear last insist mode list
                print("\n--------------------------------\n")
                print("INSIST MODE DEACTIVATED")
                print("\n--------------------------------")

    def rule_switch_check(self, current_trial_num):
        if (
            current_trial_num >= self.settings.rule_switch_initial_trials_wait
        ):  # wait initial trials bevore checking for rule switch
            rule_switch_range = self.trials_correct_side_chosen[
                self.settings.rule_switch_initial_trials_wait :
            ]  # only check for rule switch after initial wait
            if (
                len(rule_switch_range) >= self.settings.rule_switch_trial_check_range
            ):  # > not >= because trial counter in main states loop starts from 1 not 0
                slice = rule_switch_range[-self.settings.rule_switch_trial_check_range :]
                correct_chosen = sum(slice)  # get number of correct choices
                # check if rule switch
                if self.is_initial_rule_active:
                    if correct_chosen >= self.settings.rule_switch_trials_correct_trigger_switch:
                        self.active_rule = "RU1"  # switch to rule 1
                        self.is_initial_rule_active = False  # deactivate rule switch
                        print("\n--------------------------------\n")
                        print("\n switch to rule RU1\n")
                        print("\n--------------------------------\n")
                        # invert stimulus configuration
                        bk = self.settings.stimulus_correct.copy()
                        self.settings.stimulus_correct = self.settings.stimulus_wrong.copy()
                        self.settings.stimulus_wrong = bk
