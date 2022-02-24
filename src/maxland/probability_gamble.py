import random
from typing import Dict, List

from maxland.parameter_handler import TrialParameterHandler


class ProbabilityConstructor:
    """
    Module to calculate and handle probability for all events with given usersettings in session e.g.
    reward left and reward right probability
    Args:
        settings (TrialParameterHandler object): the object for all the session parameters from TrialParameterHandler
    """

    def __init__(self, settings: TrialParameterHandler):
        self.settings = settings
        self.set_block_trial_number_from_range()
        self.trial_number = self.get_total_trial_count()
        self.probability_list = self.get_probability_list()
        self.update_settings()

    def set_block_trial_number_from_range(self):
        for block in self.settings.blocks:
            block_trial_range = block["trial_range_block"]
            block_trial_number = random.randint(block_trial_range[0], block_trial_range[1])
            block["block_trial_number"] = block_trial_number

    def get_total_trial_count(self):
        trial_number = 0
        for block in self.settings.blocks:
            trial_number += block["block_trial_number"]
        return trial_number

    def get_probability_list(self):
        probability_list: List[Dict[str, bool]] = list()
        block_number = 0
        for block in self.settings.blocks:
            probability_list.extend(self.get_all_trials_of_blocks(block, self.settings.is_gamble_side_left, block_number))
            block_number += 1
        return probability_list

    def get_rewarded_not_rewarded_trials(self, probability, trial_number):
        rewarded_not_rewarded_trials = []
        total_trials_rewarded = int(trial_number * probability)
        total_trials_not_rewarded = int(trial_number * (1 - probability))
        for _ in range(trial_number):
            if _ < total_trials_rewarded:
                rewarded_not_rewarded_trials.append(True)
            elif _ < (total_trials_not_rewarded + total_trials_rewarded):
                rewarded_not_rewarded_trials.append(False)
        if len(rewarded_not_rewarded_trials) < trial_number:
            rewarded_not_rewarded_trials.append(bool(random.getrandbits(1)))
        random.shuffle(rewarded_not_rewarded_trials)
        return rewarded_not_rewarded_trials

    def get_all_trials_of_blocks(self, block, is_gamble_left, block_number):
        gamble_reward_list = self.get_rewarded_not_rewarded_trials((block["prob_reward_gamble_block"] / 100), block["block_trial_number"])
        save_reward_list = self.get_rewarded_not_rewarded_trials((block["prob_reward_save_block"] / 100), block["block_trial_number"])
        all_trials_of_block = []
        for trial in range(block["block_trial_number"]):
            trial_dict = {
                "gamble_left": is_gamble_left,
                "gamble_reward": gamble_reward_list[trial],
                "safe_reward": save_reward_list[trial],
                "block": block_number,
            }
            all_trials_of_block.append(trial_dict)
        block["block_rewards"] = all_trials_of_block
        return all_trials_of_block

    def update_settings(self):
        self.settings.probability_list = self.probability_list
        self.settings.trial_number = self.trial_number
