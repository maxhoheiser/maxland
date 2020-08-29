
import random

class ProbabilityConstuctor():
    def __init__(self, settings):
        """object to calculate and handle probability for all events with given usersettings in session e.g. reward left and reward right probability

        Args:
            settings (TrialParameterHandler object): the object for all the session parameters from TrialPArameterHandler
        """        
        self.settings = settings
        self.trial_num = self.block_trial_builder("trial_range_block")
        self.probability_list = []
        for block in self.settings.blocks:
            self.probability_list.extend( self.block_list_builder(block, self.settings.gamble_side_left))

    def block_trial_builder(self, trial_range_block):
        """randomly choose block trial length from range and add to block dict

        Args:
            trial_range_block (list): list of integers given the trial range for given block

        Returns:
            int: probabalistically derived trial number in given trial range
        """        
        trial_num = 0
        for block in self.settings.blocks:
            block_trial_range = block[trial_range_block]
            block_trial_num = random.randint(block_trial_range[0], block_trial_range[1])
            # here the value of settings object block variable are changed !
            block["block_trial_num"] = block_trial_num
            trial_num += block_trial_num
        return trial_num


    def probability_builder(self, probability, trial_num):
        """generate a random shuffeled list of defined probability of booleans

        Args:
            probability (float): probability in percentage (0.9 = 90%) for gamble (big) reward
            trial_num (int): number of trials in this block

        Returns:
            list_rand (list): list of boolean values with gamble probability distribution
        """        
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

    def block_list_builder(self, block, gambl_left):
        """create a dictionary for each trial in given block with both save and gamble reward based on given probability in settings

        Args:
            block ([type]): [description]
            gambl_left ([type]): [description]

        Returns:
            [type]: [description]
        """        
        gamble_reward_list = self.probability_builder((block["prob_reward_gambl_block"]/100), block["block_trial_num"])
        save_reward_list = self.probability_builder((block["prob_reward_save_block"]/100), block["block_trial_num"])
        block_list = []
        for trial in range(block["block_trial_num"]):
            trial_dict = {"gambl_left": gambl_left,
                         "gambl_reward": gamble_reward_list[trial],
                         "safe_reward": save_reward_list[trial],
                         }
            block_list.append(trial_dict)
        block["block_rewards"] = block_list
        return block_list
