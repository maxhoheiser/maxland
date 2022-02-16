import random
import unittest
from unittest.mock import MagicMock, patch

from maxland.parameter_handler import TrialParameterHandler
from maxland.probability_gamble import ProbabilityConstructor


class Dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


USERSETTINGS = Dotdict(
    {
        "TASK": "gamble",
        "GAMBLE_SIDE": "Left",
        "BLOCKS": [
            {"trial_range_block": [4, 7], "prob_reward_gamble_block": 10.0, "prob_reward_save_block": 20.0},
            {"trial_range_block": [3, 5], "prob_reward_gamble_block": 30.0, "prob_reward_save_block": 40.0},
            {"trial_range_block": [5, 8], "prob_reward_gamble_block": 50.0, "prob_reward_save_block": 50.0},
        ],
        "BIG_REWARD": 0.11,
        "SMALL_REWARD": 0.12,
        "LAST_CALLIBRATION": "2020.06.10",
        "TIME_START": 1.0,
        "TIME_WHEEL_STOPPING_CHECK": 1.0,
        "TIME_WHEEL_STOPPING_PUNISH": 0.0,
        "TIME_PRESENT_STIMULUS": 1.0,
        "TIME_OPEN_LOOP": 10.0,
        "TIME_OPEN_LOOP_FAIL_PUNISH": 0.0,
        "TIME_STIMULUS_FREEZE": 2.0,
        "TIME_REWARD": 1.0,
        "TIME_NO_REWARD": 1.0,
        "TIME_INTER_TRIAL": 1.5,
        "STIMULUS_RAD": 45,
        "STIMULUS_COL": [0, 255, 0],
        "BACKGROUND_COL": [0, 0, 0],
        "ROTARYENCODER_THRESHOLDS": [-90, 90, -2, 2],
        "STIMULUS_END_POS": [-2048, 2048],
        "LIFE_PLOT": False,
        "ANIMAL_WEIGHT": 10.0,
    }
)


class TestProbabilityConstructorModuleConfidentialityTask(unittest.TestCase):
    def setUp(self):
        self.parameter_handler = TrialParameterHandler(USERSETTINGS, "", "")
        random.seed(666)
        self.random = random

    def tearDown(self):
        self.parameter_handler = None

    def test_load_probability_constructor_module(self):
        ProbabilityConstructor(self.parameter_handler)

    @patch("maxland.probability_gamble.random")
    def test_set_block_trial_number_from_range(self, random):
        random.randint._mock_side_effect = self.random.randint
        probability_constructor = ProbabilityConstructor(self.parameter_handler)

        self.assertEqual(probability_constructor.settings.blocks[0]["block_trial_number"], 7)
        self.assertEqual(probability_constructor.settings.blocks[1]["block_trial_number"], 4)
        self.assertEqual(probability_constructor.settings.blocks[2]["block_trial_number"], 8)

    @patch("maxland.probability_gamble.random")
    def test_get_total_trial_count(self, random):
        random.randint._mock_side_effect = self.random.randint
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        trial_num = probability_constructor.get_total_trial_count()

        self.assertEqual(trial_num, 19)
