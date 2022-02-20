import importlib.util
import os
import unittest
from pathlib import Path

from maxland.parameter_handler import TrialParameterHandler
from maxland.probability_conf import ProbabilityConstructor

USERSETTINGS = os.path.join(Path(os.path.dirname(__file__)).parent.absolute(), "usersettings_example_conf_task.py")
CORRECT_SIDE_LEFT = "left"
CORRECT_SIDE_RIGHT = "right"

TEST_DISPLAY = {
    "monitor_width": 1024,
    "monitor_distance": 30,
    "screen_width": 1024,
    "screen_height": 780,
}


class TestStimulusGambleTask(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("usersettings", USERSETTINGS)
        self.usersettings_example_import = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.usersettings_example_import)
        self.parameter_handler = TrialParameterHandler(self.usersettings_example_import, "", "")
        self.parameter_handler.monitor_width = TEST_DISPLAY["monitor_width"]
        self.parameter_handler.monitor_distance = TEST_DISPLAY["monitor_distance"]
        self.parameter_handler.screen_width = TEST_DISPLAY["screen_width"]
        self.parameter_handler.screen_height = TEST_DISPLAY["screen_height"]

        self.probability_constructor = ProbabilityConstructor(self.parameter_handler)

    def tearDown(self):
        self.parameter_handler = None
        self.probability_constructor = None
