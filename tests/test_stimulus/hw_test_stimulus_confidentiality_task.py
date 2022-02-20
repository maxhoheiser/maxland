import importlib.util
import os
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from maxland.parameter_handler import TrialParameterHandler
from maxland.probability_conf import ProbabilityConstructor
from maxland.stimulus_conf import Stimulus

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

    # def test_load_stimulus_conf(self):
    #     rotary_encoder = MagicMock()
    #     rotary_encoder.rotary_encoder.read_stream.return_value = None

    #     game = Stimulus(self.parameter_handler, rotary_encoder, CORRECT_SIDE_LEFT)
    #     time.sleep(1)
    #     game.on_close()

    # def test_run_game_3_left(self):
    #     rotary_encoder = MagicMock()
    #     rotary_encoder.rotary_encoder.read_stream.return_value = None
    #     event_flag = MagicMock()
    #     event_flag.wait.return_value = time.sleep(2)

    #     event_flags = {
    #         "event_display_stimulus": event_flag,
    #         "event_still_show_stimulus": event_flag,
    #     }

    #     # game = Stimulus(self.parameter_handler, rotary_encoder, CORRECT_SIDE_LEFT)
    #     # game.run_game_3(event_flags)
    #     time.sleep(2)
    #     # game.run_closed_loop_before = False
    #     time.sleep(2)
    #     # game.run_open_loop = False
    #     time.sleep(6)
    #     # game.on_close()
