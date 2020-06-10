"""
probability calculator
"""
import random

class ProbabilityConstuctor():
    def __init__(self, settings):
        self.BLOCKS = settings.BLOCKS
        self.trial_num = self.block_trial_builder(settings.TRIAL_RANGE_BLOCK)
        self.probability_list = []
        for block in self.BLOCKS:
            self.probability_list.extend( self.block_list_builder(block, \
                                                        settings.GAMB_SIDE_LEFT ,\
                                                        settings.PROB_REWARD_GAMBL_BLOCK, \
                                                        settings.PROB_REWARD_SAVE_BLOCK, \
                                                        )
                                                    )

    def block_trial_builder(self, TRIAL_RANGE_BLOCK):
        '''randomly choose block trial length from range and add to block dict'''
        trial_num = 0
        for block in self.BLOCKS:
            block_trial_range = block[TRIAL_RANGE_BLOCK]
            block_trial_num = random.randint(block_trial_range[0], block_trial_range[1])
            block["block_trial_num"] = block_trial_num
            trial_num += block_trial_num
        return trial_num

    def probability_builder(self, probability, trial_num):
        '''generate a random shuffeled list of defined probability of boolean'''
        list_rand = []
        number_true = int(trial_num*probability)
        number_false = int(trial_num*(1-probability))
        for _ in range(trial_num):
            if _ < number_true:
                list_rand.append(True)
            elif _ < (number_false + number_true):
                list_rand.append(False)
        if len(list_rand) < trial_num:
            list_rand.append(bool(random.getrandbits(1)))
        random.shuffle(list_rand)
        return list_rand

    def block_list_builder(self, block, gambl_left, PROB_REWARD_GAMBL_BLOCK, PROB_REWARD_SAVE_BLOCK):
        '''create a dictionary for each trial in given block with both save and gamble reward based on given probability in settings'''
        gamble_reward_list = self.probability_builder((block[PROB_REWARD_GAMBL_BLOCK]/100), block["block_trial_num"])
        save_reward_list = self.probability_builder((block[PROB_REWARD_SAVE_BLOCK]/100), block["block_trial_num"])
        block_list = []
        for trial in range(block["block_trial_num"]):
            trial_dict = {"gambl_left": gambl_left,
                         "gambl_reward": gamble_reward_list[trial],
                         "safe_reward": save_reward_list[trial],
                         }
            block_list.append(trial_dict)
        block["block_rewards"] = block_list
        return block_list
