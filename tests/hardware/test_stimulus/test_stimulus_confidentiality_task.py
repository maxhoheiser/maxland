import importlib.util
import os
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from maxland.parameter_handler import TrialParameterHandler
from maxland.probability_conf import ProbabilityConstructor
from maxland.stimulus_conf import Stimulus

USERSETTINGS = os.path.join(Path(os.path.dirname(__file__)).parent.absolute().parent.absolute(), "usersettings_example_conf_task.py")

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

    def thread_function(self, game):
        time.sleep(2)
        game.stop_closed_loop_before()
        time.sleep(2)
        game.stop_open_loop()

    def test_load_stimulus_conf(self):
        rotary_encoder = MagicMock()
        rotary_encoder.rotary_encoder.read_stream.return_value = []

        game = Stimulus(self.parameter_handler, rotary_encoder, self.probability_constructor.stimulus_sides)
        time.sleep(1)
        game.on_close()

    def test_run_game_3(self):
        rotary_encoder = MagicMock()
        rotary_encoder.rotary_encoder.read_stream.return_value = [["a", "b", 10]]
        event_flag = MagicMock()
        event_flag.wait.return_value = time.sleep(2)

        print(self.probability_constructor.stimulus_sides)

        game = Stimulus(self.parameter_handler, rotary_encoder, self.probability_constructor.stimulus_sides)

        event_flags = {
            "event_display_stimulus": event_flag,
            "event_still_show_stimulus": event_flag,
        }

        thread = threading.Thread(target=self.thread_function, args=(game,))

        thread.start()
        game.run_game_3(event_flags)

        thread.join()
        game.on_close()

    def test_run_game_2(self):
        rotary_encoder = MagicMock()
        rotary_encoder.rotary_encoder.read_stream.return_value = [["a", "b", 10]]
        event_flag = MagicMock()
        event_flag.wait.return_value = time.sleep(2)

        game = Stimulus(self.parameter_handler, rotary_encoder, self.probability_constructor.stimulus_sides)

        event_flags = {
            "event_display_stimulus": event_flag,
            "event_still_show_stimulus": event_flag,
        }

        thread = threading.Thread(target=self.thread_function, args=(game,))

        thread.start()
        game.run_game_2(event_flags)

        thread.join()
        game.on_close()

    def test_run_game_1(self):
        rotary_encoder = MagicMock()
        rotary_encoder.rotary_encoder.read_stream.return_value = [["a", "b", 10]]
        event_flag = MagicMock()
        event_flag.wait.return_value = time.sleep(2)

        game = Stimulus(self.parameter_handler, rotary_encoder, self.probability_constructor.stimulus_sides)

        event_flags = {
            "event_display_stimulus": event_flag,
            "event_still_show_stimulus": event_flag,
        }

        thread = threading.Thread(target=self.thread_function, args=(game,))

        thread.start()
        game.run_game_1(event_flags)

        thread.join()
        game.on_close()

    def test_run_game_habituation_3_simple(self):
        rotary_encoder = MagicMock()
        rotary_encoder.rotary_encoder.read_stream.return_value = [["a", "b", 10]]
        event_flag = MagicMock()
        event_flag.wait.return_value = time.sleep(2)

        game = Stimulus(self.parameter_handler, rotary_encoder, self.probability_constructor.stimulus_sides)

        event_flags = {
            "event_display_stimulus": event_flag,
            "event_still_show_stimulus": event_flag,
        }

        thread = threading.Thread(target=self.thread_function, args=(game,))

        thread.start()
        game.run_game_habituation_3_simple(event_flags)

        thread.join()
        game.on_close()

    def test_run_game_habituation_3_complex(self):
        rotary_encoder = MagicMock()
        rotary_encoder.rotary_encoder.read_stream.return_value = [["a", "b", 10]]
        event_flag = MagicMock()
        event_flag.wait.return_value = time.sleep(2)

        game = Stimulus(self.parameter_handler, rotary_encoder, self.probability_constructor.stimulus_sides)

        event_flags = {
            "event_display_stimulus": event_flag,
            "event_still_show_stimulus": event_flag,
        }

        thread = threading.Thread(target=self.thread_function, args=(game,))

        thread.start()
        game.run_game_habituation_3_complex(event_flags)

        thread.join()
        game.on_close()

    def test_run_game_habituation_2(self):
        rotary_encoder = MagicMock()
        rotary_encoder.rotary_encoder.read_stream.return_value = [["a", "b", 10]]
        event_flag = MagicMock()
        event_flag.wait.return_value = time.sleep(2)

        game = Stimulus(self.parameter_handler, rotary_encoder, self.probability_constructor.stimulus_sides)

        event_flags = {
            "event_display_stimulus": event_flag,
            "event_still_show_stimulus": event_flag,
        }

        thread = threading.Thread(target=self.thread_function, args=(game,))

        thread.start()
        game.run_game_habituation_2(event_flags)

        thread.join()
        game.on_close()
