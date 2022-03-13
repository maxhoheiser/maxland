import importlib.util
import os
import unittest
from pathlib import Path

from maxland.parameter_handler import TrialParameterHandler
from maxland.userinput import UserInput

USERSETTINGS = os.path.join(Path(os.path.dirname(__file__)).parent.absolute().parent.absolute(), "usersettings_example_conf_task.py")
NEW_TRIAL_NUMBER = 92
NEW_AMOUNT = 33.3
NEW_STIMULUS_END_POSITION_LEFT = "-32"
NEW_STIMULUS_END_POSITION_RIGHT = "35"
NEW_ROTARYENCODER_THRESHOLD_LEFT = "-83"
NEW_ROTARYENCODER_THRESHOLD_RIGHT = "73"
NEW_BACKGROUND_COLOR_RBG = "213, 214, 215"
NEW_STIMULUS_COLOR_RBG = "213, 214, 215"
NEW_SPATIAL_FREQUENCY = 0.21
NEW_ORIENTATION = 45
NEW_STIMULUS_SIZE = 43
NEW_PHASE_SPEED = 0.05
NEW_INSIST_MODE_TRIGGER_RANGE = 93
NEW_TIME_VALUE = 77.4
NEW_STIMULUS_TYPE = "three-stimuli "


class TestUserInputConfidentialityTask(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("usersettings", USERSETTINGS)
        self.usersettings_example_import = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.usersettings_example_import)
        self.parameter_handler = TrialParameterHandler(self.usersettings_example_import, "", "")
        self.window = UserInput(self.parameter_handler)
        self.window.draw_window_before()
        self.widget = self.window.root
        self.widget.update_idletasks()

    def tearDown(self):
        self.window.on_cancel()
        self.window = None
        self.parameter_handler = None

    # test helpers
    def times_tester(self, time_dict_key: str):
        all_time_objects = {
            "time_start": self.window.time_start,
            "time_wheel_stopping_check": self.window.time_wheel_stopping_check,
            "time_wheel_stopping_punish": self.window.time_wheel_stopping_punish,
            "time_present_stimulus": self.window.time_present_stimulus,
            "time_open_loop": self.window.time_open_loop,
            "time_stimulus_freeze": self.window.time_stimulus_freeze,
            "time_reward": self.window.time_reward,
            "time_no_reward": self.window.time_reward,
            "time_inter_trial": self.window.time_inter_trial,
            "time_open_loop_fail_punish": self.window.time_open_loop_fail_punish,
        }
        time_object = all_time_objects[time_dict_key]

        time_object.var.set(NEW_TIME_VALUE)
        self.window.on_confirm()

        self.assertEqual(self.parameter_handler.time_dict[time_dict_key], NEW_TIME_VALUE)

    def get_list_from_rgb_string(self, rgb_string):
        return list(map(int, rgb_string.split(",")))

    # tests
    def test_draw_window_habituation_simple(self):
        self.parameter_handler.stimulus_type = "three-stimuli"
        window = UserInput(self.parameter_handler)
        window.draw_window_before(stage="habituation_simple")
        widget = window.root
        widget.update_idletasks()
        window.on_cancel()

    def test_draw_window_habituation_complex_three_stimuli(self):
        self.parameter_handler.stimulus_type = "three-stimuli"
        window = UserInput(self.parameter_handler)
        window.draw_window_before(stage="habituation_complex")
        widget = window.root
        widget.update_idletasks()
        window.on_cancel()

    def test_draw_window_habituation_complex_two_stimuli(self):
        self.parameter_handler.stimulus_type = "two-stimuli"
        window = UserInput(self.parameter_handler)
        window.draw_window_before(stage="habituation_complex")
        widget = window.root
        widget.update_idletasks()
        window.on_cancel()

    def test_draw_window_training_simple(self):
        self.parameter_handler.stimulus_type = "two-stimuli"
        window = UserInput(self.parameter_handler)
        window.draw_window_before(stage="training_simple")
        widget = window.root
        widget.update_idletasks()
        window.on_cancel()

    def test_draw_userinput_window(self):
        self.window.on_close()

    def test_on_confirm(self):
        self.window.on_confirm()

        self.assertTrue(self.parameter_handler.run_session)

    def test_on_cancel(self):
        self.window.on_cancel()

        self.assertFalse(self.parameter_handler.run_session)

    def test_trial_number(self):
        self.window.var_trial_num.set(NEW_TRIAL_NUMBER)
        self.widget.update_idletasks()
        self.window.on_confirm()

        self.assertEqual(self.parameter_handler.trial_number, NEW_TRIAL_NUMBER)

    def test_reward_amount(self):
        self.window.var_reward.set(NEW_AMOUNT)
        self.widget.update_idletasks()
        self.window.on_confirm()

        self.assertEqual(self.parameter_handler.reward, NEW_AMOUNT)

    # test stimulus
    def test_window_background(self):
        self.window.var_background_color.set(NEW_BACKGROUND_COLOR_RBG)
        self.widget.update_idletasks()
        self.window.on_confirm()

        rgb_list = self.get_list_from_rgb_string(NEW_BACKGROUND_COLOR_RBG)
        self.assertEqual(self.parameter_handler.background_color, rgb_list)

    def test_stimulus_end_positions(self):
        self.window.var_stimulus_end_pos_left.set(NEW_STIMULUS_END_POSITION_LEFT)
        self.window.var_stimulus_end_pos_right.set(NEW_STIMULUS_END_POSITION_RIGHT)
        self.widget.update_idletasks()
        self.window.on_confirm()

        new_stimulus_end_positions = [int(NEW_STIMULUS_END_POSITION_LEFT), int(NEW_STIMULUS_END_POSITION_RIGHT)]
        self.assertEqual(self.parameter_handler.stimulus_end_position, new_stimulus_end_positions)

    def test_wheel_thresholds(self):
        self.window.var_rotary_thresh_left.set(NEW_ROTARYENCODER_THRESHOLD_LEFT)
        self.window.var_rotary_thresh_right.set(NEW_ROTARYENCODER_THRESHOLD_RIGHT)
        self.widget.update_idletasks()
        self.window.on_confirm()

        new_stimulus_end_positions = [int(NEW_ROTARYENCODER_THRESHOLD_LEFT), int(NEW_ROTARYENCODER_THRESHOLD_RIGHT)]
        self.assertEqual(self.parameter_handler.rotaryencoder_thresholds[:2], new_stimulus_end_positions)

    # test correct and incorrect stimulus
    def test_stimulus_correct_settings(self):
        self.window.var_stim_correct_frequency.set(NEW_SPATIAL_FREQUENCY)
        self.window.var_stim_correct_or.set(NEW_ORIENTATION)
        self.window.var_stim_correct_size.set(NEW_STIMULUS_SIZE)
        self.window.var_stim_correct_phase_speed.set(NEW_PHASE_SPEED)
        self.widget.update_idletasks()
        self.window.on_confirm()

        stimulus_correct_side = {
            "grating_sf": NEW_SPATIAL_FREQUENCY,
            "grating_ori": NEW_ORIENTATION,
            "grating_size": NEW_STIMULUS_SIZE,
            "grating_speed": NEW_PHASE_SPEED,
        }
        self.assertEqual(self.parameter_handler.stimulus_correct_side, stimulus_correct_side)

    def test_stimulus_wrong_settings(self):
        self.window.var_stim_wrong_frequency.set(NEW_SPATIAL_FREQUENCY)
        self.window.var_stim_wrong_or.set(NEW_ORIENTATION)
        self.window.var_stim_wrong_size.set(NEW_STIMULUS_SIZE)
        self.window.var_stim_wrong_phase_speed.set(NEW_PHASE_SPEED)
        self.widget.update_idletasks()
        self.window.on_confirm()

        stimulus_wrong_side = {
            "grating_sf": NEW_SPATIAL_FREQUENCY,
            "grating_ori": NEW_ORIENTATION,
            "grating_size": NEW_STIMULUS_SIZE,
            "grating_speed": NEW_PHASE_SPEED,
        }
        self.assertEqual(self.parameter_handler.stimulus_wrong_side, stimulus_wrong_side)

    def test_stimulus_type_dropdown(self):
        self.window.var_drp_stim.set(NEW_STIMULUS_TYPE)
        self.widget.update_idletasks()
        self.window.on_confirm()

        self.assertEqual(self.parameter_handler.stimulus_type, NEW_STIMULUS_TYPE)

    def test_stimulus_radius(self):
        self.window.var_stim_rad.set(NEW_STIMULUS_SIZE)
        self.widget.update_idletasks()
        self.window.on_confirm()

        self.assertEqual(self.parameter_handler.stimulus_radius, NEW_STIMULUS_SIZE)

    def test_stimulus_color(self):
        self.window.var_stim_col.set(NEW_STIMULUS_COLOR_RBG)
        self.widget.update_idletasks()
        self.window.on_confirm()

        rgb_list = self.get_list_from_rgb_string(NEW_STIMULUS_COLOR_RBG)
        self.assertEqual(self.parameter_handler.stimulus_color, rgb_list)

    # test insist mode

    # test times
    def test_time_start(self):
        time_dict_key = "time_start"
        self.times_tester(time_dict_key)

    def test_time_wheel_stopping_check(self):
        time_dict_key = "time_wheel_stopping_check"
        self.times_tester(time_dict_key)

    def test_time_wheel_stopping_punish(self):
        time_dict_key = "time_wheel_stopping_punish"
        self.times_tester(time_dict_key)

    def test_time_stimulus_presentation(self):
        time_dict_key = "time_present_stimulus"
        self.times_tester(time_dict_key)

    def test_time_open_loop(self):
        time_dict_key = "time_open_loop"
        self.times_tester(time_dict_key)

    def test_time_stimulus_freeze(self):
        time_dict_key = "time_stimulus_freeze"
        self.times_tester(time_dict_key)

    def test_time_reward(self):
        time_dict_key = "time_reward"
        self.times_tester(time_dict_key)

    def test_time_no_reward(self):
        time_dict_key = "time_no_reward"
        self.times_tester(time_dict_key)

    def test_time_inter_trial(self):
        time_dict_key = "time_inter_trial"
        self.times_tester(time_dict_key)

    def test_time_open_loop_fail_punish(self):
        time_dict_key = "time_open_loop_fail_punish"
        self.times_tester(time_dict_key)
