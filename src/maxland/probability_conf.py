import random
from typing import Dict, List

import numpy as np

from maxland.parameter_handler import TrialParameterHandler


class ProbabilityConstructor:
    """
    Module to calculate and handle stimulus sides for the confidentiality task
    Args:
        settings (TrialParameterHandler object): the object for all the session parameters from TrialParameterHandler
    """

    def __init__(self, settings: TrialParameterHandler):
        self.settings = settings
        self.stimulus_sides: Dict[str, bool] = {}
        # insist mode tracking
        self.insist_mode_chosen_side_li: List[str] = list()
        self.insist_mode_active = False
        self.insist_side = ""
        self.active_rule = "RU0"  # id of active rule
        self.is_initial_rule_active = True

        self.get_random_side()

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
        self.settings.stimulus_correct_side_history.append(current_side)
        # check if current trial side == correct side
        if current_side == "right" and self.stimulus_sides["right"]:
            self.settings.trials_correct_side_history.append(True)
            self.current_trial_correct_side_chosen = True
        elif current_side == "left" and self.stimulus_sides["left"]:
            self.settings.trials_correct_side_history.append(True)
            self.current_trial_correct_side_chosen = True
        else:
            self.settings.trials_correct_side_history.append(False)
            self.current_trial_correct_side_chosen = False
        return current_side

    def insist_mode_check(self):
        # check for insist mode activate
        if not self.insist_mode_active:
            if len(self.settings.stimulus_correct_side_history) >= self.settings.insist_range_trigger:
                chosen_sides_li_slice = self.settings.stimulus_correct_side_history[-self.settings.insist_range_trigger :]
            else:
                chosen_sides_li_slice = self.settings.stimulus_correct_side_history
            left_num_chosen = sum(map(lambda x: x == "left", chosen_sides_li_slice))
            right_num_chosen = sum(map(lambda x: x == "right", chosen_sides_li_slice))
            if left_num_chosen >= self.settings.insist_range_trigger:
                self.insist_mode_active = True
                print(self.insist_mode_active)
                self.settings.stimulus_correct_side_history = []
                self.insist_side = "right"
                self.settings.insist_mode_history.append(self.insist_side)
                print("\n--------------------------------\n")
                print("INSIST MODE ACTIVATED: insist right")
                print("\n--------------------------------\n")
                return
            if right_num_chosen >= self.settings.insist_range_trigger:
                self.insist_mode_active = True
                self.settings.stimulus_correct_side_history = []
                self.insist_side = "left"
                self.settings.insist_mode_history.append(self.insist_side)
                print("\n--------------------------------\n")
                print("INSIST MODE ACTIVATED: insist left")
                print("\n--------------------------------\n")
                return
            return
        # deactivate insist mode
        if self.insist_mode_active:
            self.insist_mode_chosen_side_li.append(self.settings.stimulus_correct_side_history[-1])
            if len(self.insist_mode_chosen_side_li) >= self.settings.insist_range_deactivate:
                chosen_sides_li_slice = self.insist_mode_chosen_side_li[-self.settings.insist_range_deactivate :]
            else:
                chosen_sides_li_slice = self.insist_mode_chosen_side_li
            # check range if correct
            insist_correct_choice = sum(map(lambda x: x == self.insist_side, chosen_sides_li_slice))
            if insist_correct_choice >= self.settings.insist_correct_deactivate:
                self.insist_mode_active = False
                self.insist_side = None
                self.settings.insist_mode_history.append("none")
                self.insist_mode_chosen_side_li = []
                print("\n---------------------\n")
                print("INSIST MODE DEACTIVATED")
                print("\n---------------------\n")

    def rule_switch_check(self, current_trial_num):
        if current_trial_num >= self.settings.rule_switch_initial_trials_wait:
            rule_switch_range = self.settings.trials_correct_side_history[self.settings.rule_switch_initial_trials_wait :]
            # > not >= because trial counter in main states loop starts from 1 not 0
            if len(rule_switch_range) >= self.settings.rule_switch_trial_check_range:
                rule_switch_range_slice = rule_switch_range[-self.settings.rule_switch_trial_check_range :]
                correct_chosen = sum(rule_switch_range_slice)
                # check if rule switch
                if self.is_initial_rule_active:
                    if correct_chosen >= self.settings.rule_switch_trials_correct_trigger_switch:
                        self.active_rule = "RU1"  # switch to rule 1

                        self.is_initial_rule_active = False  # deactivate rule switch
                        print("\n--------------------------------\n")
                        print("\n switch to rule RU1\n")
                        print("\n--------------------------------\n")
                        # invert stimulus configuration
                        bk = self.settings.stimulus_correct_side.copy()
                        self.settings.stimulus_correct_side = self.settings.stimulus_wrong_side.copy()
                        self.settings.stimulus_wrong_side = bk
        self.settings.active_rule_history.append(self.active_rule)
