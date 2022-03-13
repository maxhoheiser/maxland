import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

import maxland.helperfunctions as hf


class TestHelperFunctionsTryRunFunction(unittest.TestCase):
    def test_try_run_function_succeed(self):
        def test_function():
            return 1 + 1

        wrapper = hf.try_run_function(test_function)
        wrapper_return = wrapper()()

        self.assertEqual(wrapper_return, 2)

    def test_try_run_function_fail(self):
        def broken_test_function():
            raise Exception("Test exception")

        wrapper = hf.try_run_function(broken_test_function)
        wrapper_return = wrapper()

        self.assertRaises(Exception, wrapper_return)


class TestHelperFunctionsPostSessionCleanup(unittest.TestCase):
    def setUp(self):
        self.bpod = MagicMock()
        self.sma = MagicMock()
        self.bpod.run_state_machine.return_value = False

        self.flag_one = MagicMock()
        self.flag_one.set.return_value = None
        self.flag_two = MagicMock()
        self.flag_two.set.return_value = None
        self.flag_three = MagicMock()
        self.flag_three.set.return_value = None

        self.event_flags_gamble = {
            "event_still_show_stimulus": self.flag_one,
            "event_display_stimulus": self.flag_two,
            "event_start_open_loop": self.flag_three,
        }
        self.event_flags_confidentiality = {
            "event_still_show_stimulus": self.flag_one,
            "event_display_stimulus": self.flag_two,
        }

        self.stimulus_game = MagicMock()
        self.stimulus_game.win.close.return_value = None
        self.stimulus_game.close.return_value = None

        self.rotary_encoder_module = MagicMock()
        self.rotary_encoder_module.close.return_value = None

    def tearDown(self):
        pass

    def test_post_session_cleanup_bpod_sma_not_running_gamble(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            hf.post_session_cleanup(self.stimulus_game, self.bpod, self.sma, self.event_flags_gamble)
            self.assertEqual(mock_stdout.getvalue(), "\nCLOSED\n\n")

    def test_post_session_cleanup_bpod_sma_not_running_confidentiality(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            hf.post_session_cleanup(self.stimulus_game, self.bpod, self.sma, self.event_flags_confidentiality)
            self.assertEqual(mock_stdout.getvalue(), "\nCLOSED\n\n")

    def test_post_session_cleanup_gamble_bpod_sma_running_gamble(self):
        self.bpod.run_state_machine.return_value = True

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            hf.post_session_cleanup(self.stimulus_game, self.bpod, self.sma, self.event_flags_gamble)
            self.assertEqual(mock_stdout.getvalue(), "")

    def test_post_session_cleanup_gamble_bpod_sma_running_confidentiality(self):
        self.bpod.run_state_machine.return_value = True

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            hf.post_session_cleanup(self.stimulus_game, self.bpod, self.sma, self.event_flags_confidentiality)
            self.assertEqual(mock_stdout.getvalue(), "")
