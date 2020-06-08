"""
probability calculator
"""
import random

class ProbabilityConstuctor():
    def __init__(self, settings):
        self.BLOCKS = settings.BLOCKS
        self.TRIAL_NUM = 0
        for block in self.BLOCKS:
            self.TRIAL_NUM += block[settings.TRIAL_NUM_BLOCK]
        self.probability_list = []
        for block in self.BLOCKS:
            self.probability_list.extend( self.block_list_builder(block, \
                                                        settings.GAMB_SIDE_LEFT ,\
                                                        settings.PROB_REWARD_GAMBL_BLOCK, \
                                                        settings.PROB_REWARD_SAVE_BLOCK, \
                                                        settings.TRIAL_NUM_BLOCK) )

    def probability_builder(self, probability, trial_num):
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

    def block_list_builder(self, block, gambl_left, PROB_REWARD_GAMBL_BLOCK, PROB_REWARD_SAVE_BLOCK, TRIAL_NUM_BLOCK):
        gamble_reward_list = self.probability_builder((block[PROB_REWARD_GAMBL_BLOCK]/100), block[TRIAL_NUM_BLOCK])
        save_reward_list = self.probability_builder((block[PROB_REWARD_SAVE_BLOCK]/100), block[TRIAL_NUM_BLOCK])
        block_list = []
        for trial in range(block[TRIAL_NUM_BLOCK]):
            trial_dict = {"gambl_left": gambl_left,
                         "gambl_reward": gamble_reward_list[trial],
                         "safe_reward": save_reward_list[trial],
                         }
            block_list.append(trial_dict)
        return block_list
