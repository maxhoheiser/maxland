import random
import unittest
from unittest.mock import MagicMock, patch

from maxland.parameter_handler import TrialParameterHandler
from maxland.probability_conf import ProbabilityConstructor


class Dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


USERSETTINGS = Dotdict(
    {
        "TASK": "conf",
        "TRIAL_NUMBER": 30,
        "STIMULUS_TYPE": "two-stimuli",
        "STIMULUS_CORRECT": {"grating_sf": 0.01, "grating_ori": 0.1, "grating_size": 40.0, "grating_speed": 0.04},
        "STIMULUS_WRONG": {"grating_sf": 0.04, "grating_ori": 90.0, "grating_size": 40.0, "grating_speed": 0.01},
        "REWARD": 0.12,
        "LAST_CALLIBRATION": "2020.06.10",
        "TIME_START": 1.0,
        "TIME_WHEEL_STOPPING_CHECK": 1.0,
        "TIME_WHEEL_STOPPING_PUNISH": 0.0,
        "TIME_PRESENT_STIMULUS": 1.0,
        "TIME_OPEN_LOOP": 10.0,
        "TIME_OPEN_LOOP_FAIL_PUNISH": 0.0,
        "TIME_STIMULUS_FREEZE": 2.0,
        "TIME_REWARD": 1.0,
        "TIME_RANGE_OPEN_LOOP_WRONG_PUNISH": [0.0, 0.0],
        "TIME_INTER_TRIAL": 1.5,
        "INSIST_RANGE_TRIGGER": 5,
        "INSIST_CORRECT_DEACTIVATE": 3,
        "INSIST_RANGE_DEACTIVATE": 35,
        "RULE_SWITCH_INITIAL_WAIT": 10,
        "RULE_SWITCH_RANGE": 10,
        "RULE_SWITCH_CORRECT": 8,
        "FADE_START": 1950,
        "FADE_END": 3000,
        "STIMULUS_RAD": 45,
        "STIMULUS_COL": [0, 255, 0],
        "BACKGROUND_COL": [0, 0, 0],
        "ROTARYENCODER_THRESHOLDS": [-90, 90, -2, 2],
        "STIMULUS_END_POS": [-2048, 2048],
        "LIFE_PLOT": False,
        "ANIMAL_WEIGHT": 10.0,
    }
)

INITIAL_RULE = "RU0"
SWITCHED_RULE = "RU1"


class TestProbabilityConstructorConfidentialityTask(unittest.TestCase):
    def setUp(self):
        self.parameter_handler = TrialParameterHandler(USERSETTINGS, "", "")
        random.seed(666)
        self.random = random

    def tearDown(self):
        self.parameter_handler = None

    def test_load_probability_constructor_module(self):
        ProbabilityConstructor(self.parameter_handler)

    @patch("maxland.probability_conf.random")
    def test_get_random_side(self, random):
        random.getrandbits._mock_side_effect = self.random.getrandbits
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.get_random_side()

        self.assertEqual(probability_constructor.stimulus_sides["right"], False)
        self.assertEqual(probability_constructor.stimulus_sides["left"], True)

    @patch("maxland.probability_conf.random")
    def test_ret_random_side_insist_mode_active_right(self, random):
        random.getrandbits._mock_side_effect = self.random.getrandbits
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.insist_mode_active = True
        probability_constructor.insist_side = "right"
        probability_constructor.get_random_side()

        self.assertEqual(probability_constructor.stimulus_sides["right"], True)
        self.assertEqual(probability_constructor.stimulus_sides["left"], False)

    @patch("maxland.probability_conf.random")
    def test_ret_random_side_insist_mode_active_left(self, random):
        random.seed(555)
        random.getrandbits._mock_side_effect = random.getrandbits
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.insist_mode_active = True
        probability_constructor.insist_side = "left"
        probability_constructor.get_random_side()

        self.assertEqual(probability_constructor.stimulus_sides["right"], False)
        self.assertEqual(probability_constructor.stimulus_sides["left"], True)

    # test insist mode
    def test_not_activate_insist(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.chosen_sides_li = ["right", "left", "left", "right"]
        probability_constructor.settings.insist_range_trigger = 4

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, False)

    def test_not_activate_insist_slice(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.chosen_sides_li = ["left", "left", "left", "left", "left", "left", "right", "right"]
        probability_constructor.settings.insist_range_trigger = 5

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, False)

    def test_activate_insist_left(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.chosen_sides_li = ["right", "left", "right", "right", "right"]
        probability_constructor.settings.insist_range_trigger = 3

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, True)
        self.assertEqual(probability_constructor.insist_side, "left")

    def test_activate_insist_right(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.chosen_sides_li = ["left", "right", "left", "left", "left"]
        probability_constructor.settings.insist_range_trigger = 3

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, True)
        self.assertEqual(probability_constructor.insist_side, "right")

    def test_deactivate_insist(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.insist_mode_active = True
        probability_constructor.insist_mode_chosen_side_li = ["left", "right", "left"]
        probability_constructor.chosen_sides_li = ["left"]
        probability_constructor.insist_side = "left"
        probability_constructor.settings.insist_correct_deactivate = 3
        probability_constructor.settings.insist_range_deactivate = 4

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, False)
        self.assertEqual(probability_constructor.insist_side, None)
        self.assertEqual(probability_constructor.insist_mode_chosen_side_li, [])

    def test_not_deactivate_insist(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.insist_mode_active = True
        probability_constructor.insist_mode_chosen_side_li = ["left", "right", "left"]
        probability_constructor.chosen_sides_li = ["right"]
        probability_constructor.insist_side = "left"
        probability_constructor.settings.insist_correct_deactivate = 3
        probability_constructor.settings.insist_range_deactivate = 4

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, True)
        self.assertEqual(probability_constructor.insist_side, "left")
        self.assertEqual(probability_constructor.insist_mode_chosen_side_li, ["left", "right", "left", "right"])
