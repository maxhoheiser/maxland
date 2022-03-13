import importlib.util
import os
import unittest
from pathlib import Path

from maxland.parameter_handler import TrialParameterHandler
from maxland.types_usersettings import GambleSide
from maxland.userinput import UserInput

USERSETTINGS = os.path.join(Path(os.path.dirname(__file__)).parent.absolute().parent.absolute(), "usersettings_example_gamble_task.py")

# Mock user input data
NEW_GAMBLE_SIDE = GambleSide.RIGHT
# Blocks
NEW_BLOCK_TRIAL_RANGE_MIN = 3
NEW_BLOCK_TRIAL_RANGE_MAX = 4
NEW_BLOCK_PROBABILITY_GAMBLE = 80
NEW_BLOCK_PROBABILITY_SAFE = 55
# reward in seconds
NEW_BIG_REWARD = 10.15
NEW_SMALL_REWARD = 11.16
# trial times
NEW_TIME_VALUE = 3.2
# stimulus
NEW_STIMULUS_RADIUS = 46
NEW_STIMULUS_COLOR_RBG = "1, 252, 1"
NEW_BACKGROUND_COLOR_RGB = "1, 2, 3"
# thresholds
NEW_ROTARYENCODER_THRESHOLDS = [-91, 92, -3, 4]
NEW_STIMULUS_END_POSITION = [-2047, 2049]
NEW_LIFE_PLOT = False
NEW_ANIMAL_WEIGHT = 11


class TestUserInputGambleTask(unittest.TestCase):
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
        self.parameter_handler = None
        self.window = None
        self.widget = None

    def click_on_widget(self, widget, x, y, button=1):
        self.widget.focus_force()
        self.widget.event_generate(f"<ButtonPress-{button}>", x=x, y=y)
        self.widget.update_idletasks()

    # test helpers
    def block_time_range_tester(self, block_index):
        self.window.blocks[block_index].var_range_min.set(NEW_BLOCK_TRIAL_RANGE_MIN)
        self.window.blocks[block_index].var_range_max.set(NEW_BLOCK_TRIAL_RANGE_MAX)
        self.widget.update_idletasks()
        self.window.on_confirm()

        trial_range_block = self.parameter_handler.blocks[block_index]["trial_range_block"]
        self.assertEqual(trial_range_block[0], NEW_BLOCK_TRIAL_RANGE_MIN)
        self.assertEqual(trial_range_block[1], NEW_BLOCK_TRIAL_RANGE_MAX)

    def block_probability_tester(self, block_index):
        self.window.blocks[block_index].var_prob_gb.set(NEW_BLOCK_PROBABILITY_GAMBLE)
        self.window.blocks[block_index].var_prob_save.set(NEW_BLOCK_PROBABILITY_SAFE)
        self.widget.update_idletasks()
        self.window.on_confirm()

        probability_gamble = self.parameter_handler.blocks[block_index]["prob_reward_gamble_block"]
        probability_save = self.parameter_handler.blocks[block_index]["prob_reward_save_block"]
        self.assertEqual(probability_gamble, NEW_BLOCK_PROBABILITY_GAMBLE)
        self.assertEqual(probability_save, NEW_BLOCK_PROBABILITY_SAFE)

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
    def test_draw_userinput_window(self):
        self.window.on_close()

    def test_on_confirm(self):
        self.window.on_confirm()

        self.assertTrue(self.parameter_handler.run_session)

    def test_on_cancel(self):
        self.window.on_cancel()

        self.assertFalse(self.parameter_handler.run_session)

    def test_change_gamble_side(self):
        self.window.var_gamble_side.set(NEW_GAMBLE_SIDE)
        self.widget.update_idletasks()
        self.window.on_confirm()

        self.assertEqual(self.parameter_handler.gamble_side, NEW_GAMBLE_SIDE)

    def test_animal_weight(self):
        self.window.var_animal_weight.set(NEW_ANIMAL_WEIGHT)
        self.widget.update_idletasks()
        self.window.on_confirm()

        self.assertEqual(self.parameter_handler.animal_weight, NEW_ANIMAL_WEIGHT)

    def test_block_1_range(self):
        self.block_time_range_tester(0)

    def test_block_1_probability(self):
        self.block_probability_tester(0)

    def test_block_2_range(self):
        self.block_time_range_tester(1)

    def test_block_2_probability(self):
        self.block_probability_tester(1)

    def test_block_3_range(self):
        self.block_time_range_tester(2)

    def test_block_3_probability(self):
        self.block_probability_tester(2)

    # test reward
    def test_big_reward_amount(self):
        self.window.var_big_reward.set(NEW_BIG_REWARD)
        self.widget.update_idletasks()
        self.window.on_confirm()

        self.assertEqual(self.parameter_handler.big_reward, NEW_BIG_REWARD)

    def test_small_reward_amount(self):
        self.window.var_small_reward.set(NEW_SMALL_REWARD)
        self.widget.update_idletasks()
        self.window.on_confirm()

        self.assertEqual(self.parameter_handler.small_reward, NEW_SMALL_REWARD)

    # test stimulus
    def test_stimulus_radius(self):
        self.window.var_stim_rad.set(NEW_STIMULUS_RADIUS)
        self.widget.update_idletasks()
        self.window.on_confirm()

        self.assertEqual(self.parameter_handler.stimulus_radius, NEW_STIMULUS_RADIUS)

    def test_stimulus_color(self):
        self.window.var_stim_col.set(NEW_STIMULUS_COLOR_RBG)
        self.widget.update_idletasks()
        self.window.on_confirm()

        rgb_list = self.get_list_from_rgb_string(NEW_STIMULUS_COLOR_RBG)
        self.assertEqual(self.parameter_handler.stimulus_color, rgb_list)

    def test_window_background(self):

        self.window.var_background_color.set(NEW_BACKGROUND_COLOR_RGB)
        self.widget.update_idletasks()
        self.window.on_confirm()

        rgb_list = self.get_list_from_rgb_string(NEW_BACKGROUND_COLOR_RGB)
        self.assertEqual(self.parameter_handler.background_color, rgb_list)

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
