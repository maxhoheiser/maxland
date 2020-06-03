# -*- coding: utf-8 -*-
"""
Created on Fri May 29 21:12:44 2020

@author: User
"""

import numpy as np
import random

from probability import ProbabilityConstuctor
import settings

test = ProbabilityConstuctor(settings)

test_list = test.probability_list


# TRIAL_NUM_BLOCK = "trial_num_block"
# PROB_REWARD_GAMBL_BLOCK = "prob_reward_gambl_block"
# PROB_REWARD_SAVE_BLOCK = "prob_reward_save_block"

# BLOCKS = [
#             # block 1
#             {
#             TRIAL_NUM_BLOCK: 20,
#             PROB_REWARD_GAMBL_BLOCK: 12.5,  #(0-100)
#             PROB_REWARD_SAVE_BLOCK: 90  #(0-100)
#             },
#             # block 1
#             {
#             TRIAL_NUM_BLOCK: 20,
#             PROB_REWARD_GAMBL_BLOCK: 25.5,  #(0-100)
#             PROB_REWARD_SAVE_BLOCK: 90  #(0-100)
#             },
#             # block 1
#             {
#             TRIAL_NUM_BLOCK: 20,
#             PROB_REWARD_GAMBL_BLOCK: 75.5,  #(0-100)
#             PROB_REWARD_SAVE_BLOCK: 90  #(0-100)
#             },
#         ]

# # trial numbers:
# def probability_builder(probability, trial_num):
#     list_rand = []
#     number_true = int(trial_num*probability)
#     number_false = int(trial_num*(1-probability))
#     for _ in range(trial_num):
#         if _ < number_true:
#             list_rand.append(True)
#         elif _ < (number_false + number_true):
#             list_rand.append(False)
#     if len(list_rand) < trial_num:
#         list_rand.append(bool(random.getrandbits(1)))
#     random.shuffle(list_rand)
#     return list_rand
    
    
# for block in BLOCKS:
#    gamble_reward_list = probability_builder((block[PROB_REWARD_GAMBL_BLOCK]/100), block[TRIAL_NUM_BLOCK])        
    
    
# test = probability_builder((75.5/100), 20)
    




# terst = probability_builder(0.5, 15)


