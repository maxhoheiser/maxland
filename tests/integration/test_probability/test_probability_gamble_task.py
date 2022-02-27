import importlib.util
import os
import random
import unittest
from pathlib import Path
from unittest.mock import patch

from maxland.parameter_handler import TrialParameterHandler
from maxland.probability_gamble import ProbabilityConstructor

USERSETTINGS = os.path.join(Path(os.path.dirname(__file__)).parent.absolute().parent.absolute(), "usersettings_example_gamble_task.py")


class TestProbabilityConstructorModuleConfidentialityTask(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("usersettings_example_gamble_task", USERSETTINGS)
        self.usersettings_example_import = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.usersettings_example_import)
        self.parameter_handler = TrialParameterHandler(self.usersettings_example_import, "", "")
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
        trial_number = probability_constructor.get_total_trial_count()

        self.assertEqual(trial_number, 19)
