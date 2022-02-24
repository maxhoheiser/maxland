import importlib.util
import os
import random
import unittest
from pathlib import Path
from unittest.mock import patch

from maxland.parameter_handler import TrialParameterHandler
from maxland.probability_conf import ProbabilityConstructor

USERSETTINGS = os.path.join(Path(os.path.dirname(__file__)).parent.absolute(), "usersettings_example_conf_task.py")


INITIAL_RULE = "RU0"
SWITCHED_RULE = "RU1"


class TestProbabilityConstructorModuleConfidentialityTask(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("usersettings_example_conf_task", USERSETTINGS)
        self.usersettings_example_import = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.usersettings_example_import)
        self.parameter_handler = TrialParameterHandler(self.usersettings_example_import, "", "")
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
    def test_get_random_side_insist_mode_active_right(self, random):
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
        probability_constructor.settings.stimulus_correct_side_history = ["right", "left", "left", "right"]
        probability_constructor.settings.insist_range_trigger = 4

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, False)

    def test_not_activate_insist_slice(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.settings.stimulus_correct_side_history = ["left", "left", "left", "left", "left", "left", "right", "right"]
        probability_constructor.settings.insist_range_trigger = 5

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, False)

    def test_activate_insist_left(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.settings.stimulus_correct_side_history = ["right", "left", "right", "right", "right"]
        probability_constructor.settings.insist_range_trigger = 3

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, True)
        self.assertEqual(probability_constructor.insist_side, "left")

    def test_activate_insist_right(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.settings.stimulus_correct_side_history = ["left", "right", "left", "left", "left"]
        probability_constructor.settings.insist_range_trigger = 3

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, True)
        self.assertEqual(probability_constructor.insist_side, "right")

    def test_deactivate_insist(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.insist_mode_active = True
        probability_constructor.insist_mode_chosen_side_li = ["left", "right", "left"]
        probability_constructor.settings.stimulus_correct_side_history = ["left"]
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
        probability_constructor.settings.stimulus_correct_side_history = ["right"]
        probability_constructor.insist_side = "left"
        probability_constructor.settings.insist_correct_deactivate = 3
        probability_constructor.settings.insist_range_deactivate = 4

        probability_constructor.insist_mode_check()

        self.assertEqual(probability_constructor.insist_mode_active, True)
        self.assertEqual(probability_constructor.insist_side, "left")
        self.assertEqual(probability_constructor.insist_mode_chosen_side_li, ["left", "right", "left", "right"])

    # test rule switching
    def test_rule_switching_initial_trials_wait_not_switch(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.settings.rule_switch_initial_trials_wait = 2
        probability_constructor.settings.rule_switch_trial_check_range = 4
        probability_constructor.settings.rule_switch_trials_correct_trigger_switch = 3
        current_trial_num = 4
        probability_constructor.settings.trials_correct_side_history = [False, True, True, True]

        probability_constructor.rule_switch_check(current_trial_num)

        self.assertEqual(probability_constructor.active_rule, INITIAL_RULE)

    def test_rule_switching_initial_trials_wait_switch(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.settings.rule_switch_initial_trials_wait = 1
        probability_constructor.settings.rule_switch_trial_check_range = 3
        probability_constructor.settings.rule_switch_trials_correct_trigger_switch = 3
        current_trial_num = 4
        probability_constructor.settings.trials_correct_side_history = [False, True, True, True]

        probability_constructor.rule_switch_check(current_trial_num)

        self.assertEqual(probability_constructor.active_rule, SWITCHED_RULE)
        self.assertEqual(probability_constructor.settings.stimulus_correct_side, self.usersettings_example_import.STIMULUS_WRONG)
        self.assertEqual(probability_constructor.settings.stimulus_wrong_side, self.usersettings_example_import.STIMULUS_CORRECT)

    def test_rule_switching(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.settings.rule_switch_initial_trials_wait = 2
        probability_constructor.settings.rule_switch_trial_check_range = 10
        probability_constructor.settings.rule_switch_trials_correct_trigger_switch = 6
        current_trial_num = 10
        probability_constructor.settings.trials_correct_side_history = [
            False,
            True,
            True,
            True,
            False,
            False,
            True,
            True,
            False,
            True,
            True,
            False,
        ]

        probability_constructor.rule_switch_check(current_trial_num)

        self.assertEqual(probability_constructor.active_rule, SWITCHED_RULE)
        self.assertEqual(probability_constructor.settings.stimulus_correct_side, self.usersettings_example_import.STIMULUS_WRONG)
        self.assertEqual(probability_constructor.settings.stimulus_wrong_side, self.usersettings_example_import.STIMULUS_CORRECT)

    def test_rule_not_switching(self):
        probability_constructor = ProbabilityConstructor(self.parameter_handler)
        probability_constructor.settings.rule_switch_initial_trials_wait = 2
        probability_constructor.settings.rule_switch_trial_check_range = 10
        probability_constructor.settings.rule_switch_trials_correct_trigger_switch = 7
        current_trial_num = 10
        probability_constructor.settings.trials_correct_side_history = [
            False,
            True,
            True,
            True,
            False,
            False,
            True,
            True,
            False,
            True,
            True,
            False,
        ]

        probability_constructor.rule_switch_check(current_trial_num)

        self.assertEqual(probability_constructor.active_rule, INITIAL_RULE)
