import filecmp
import importlib.util
import os
import shutil
import unittest
from pathlib import Path

from maxland.parameter_handler import TrialParameterHandler
from maxland.types_time_dict import TimeDict
from maxland.types_usersettings import GambleSide, TaskName

USERSETTINGS_EXAMPLE_GAMBLE_TASK = os.path.join(
    Path(os.path.dirname(__file__)).parent.absolute().parent.absolute(), "usersettings_example_gamble_task.py"
)

# Mock usersettings data
NEW_TASK = TaskName.GAMBLE
NEW_GAMBLE_SIDE = GambleSide.RIGHT
NEW_BLOCKS = [
    {"trial_range_block": [3, 4], "prob_reward_gamble_block": 11.0, "prob_reward_save_block": 21.0},
    {"trial_range_block": [2, 3], "prob_reward_gamble_block": 31.0, "prob_reward_save_block": 41.0},
    {"trial_range_block": [5, 4], "prob_reward_gamble_block": 51.0, "prob_reward_save_block": 51.0},
]
# reward in seconds
NEW_BIG_REWARD = 10.15
NEW_SMALL_REWARD = 11.16
NEW_LAST_CALLIBRATION = "2020.06.10"
# trial times
NEW_TIME_START = 3.0
NEW_TIME_WHEEL_STOPPING_CHECK = 2.0
NEW_TIME_WHEEL_STOPPING_PUNISH = 2.0
NEW_TIME_PRESENT_STIMULUS = 2.0
NEW_TIME_OPEN_LOOP = 10.1
NEW_TIME_OPEN_LOOP_FAIL_PUNISH = 1.0
NEW_TIME_STIMULUS_FREEZE = 2.3
NEW_TIME_REWARD = 1.6
NEW_TIME_NO_REWARD = 2.4
TIME_INTER_TRIAL = 3
# stimulus
NEW_STIMULUS_RADIUS = 46
NEW_STIMULUS_COLOR = [1, 252, 1]
NEW_BACKGROUND_COLOR = [1, 2, 3]
# thresholds
NEW_ROTARYENCODER_THRESHOLDS = [-91, 92, -3, 4]
NEW_STIMULUS_END_POSITION = [-2047, 2049]
NEW_LIFE_PLOT = False
NEW_ANIMAL_WEIGHT = 11


def get_test_folder_paths(file_path):
    execution_folder_path = os.path.dirname(__file__)
    test_folder_path = Path(os.path.join(execution_folder_path, "test_folder"))
    settings_folder_path = Path(os.path.join(test_folder_path, "settings_folder"))
    session_folder_path = Path(os.path.join(test_folder_path, "session_folder"))
    return execution_folder_path, test_folder_path, settings_folder_path, session_folder_path


def create_folder(folder_path):
    folder_path.mkdir(parents=True, exist_ok=True)


def delete_folder(folder_path):
    shutil.rmtree(folder_path, ignore_errors=True)


class TestTrialParameterHandlerGambleTask(unittest.TestCase):
    def setUp(self):
        (
            _,
            self.test_folder_path,
            self.settings_folder_path,
            self.session_folder_path,
        ) = get_test_folder_paths(__file__)
        create_folder(self.settings_folder_path)
        create_folder(self.session_folder_path)

        spec = importlib.util.spec_from_file_location("usersettings_example_gamble_task", USERSETTINGS_EXAMPLE_GAMBLE_TASK)
        self.usersettings_example_import = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.usersettings_example_import)

    def tearDown(self):
        delete_folder(self.test_folder_path)
        self.usersettings_example_import = None

    def test_create_trialparameterhandler_from_usersettings(self):
        TrialParameterHandler(self.usersettings_example_import, self.settings_folder_path, self.session_folder_path)

    def test_save_usersettings_to_file(self):
        usersettings_object_before = TrialParameterHandler(
            self.usersettings_example_import, self.settings_folder_path, self.session_folder_path
        )
        usersettings_object_before.task_name = NEW_TASK
        usersettings_object_before.gamble_side = NEW_GAMBLE_SIDE
        usersettings_object_before.blocks = NEW_BLOCKS
        usersettings_object_before.big_reward = NEW_BIG_REWARD
        usersettings_object_before.small_reward = NEW_SMALL_REWARD
        usersettings_object_before.last_callibration = NEW_LAST_CALLIBRATION

        new_time_dict: TimeDict = {
            "time_start": NEW_TIME_START,
            "time_wheel_stopping_check": NEW_TIME_WHEEL_STOPPING_CHECK,
            "time_wheel_stopping_punish": NEW_TIME_WHEEL_STOPPING_PUNISH,
            "time_present_stimulus": NEW_TIME_PRESENT_STIMULUS,
            "time_open_loop": NEW_TIME_OPEN_LOOP,
            "time_open_loop_fail_punish": NEW_TIME_OPEN_LOOP_FAIL_PUNISH,
            "time_stimulus_freeze": NEW_TIME_STIMULUS_FREEZE,
            "time_reward": NEW_TIME_REWARD,
            "time_no_reward": NEW_TIME_NO_REWARD,
            "time_inter_trial": TIME_INTER_TRIAL,
        }
        usersettings_object_before.time_dict = new_time_dict

        usersettings_object_before.stimulus_radius = NEW_STIMULUS_RADIUS
        usersettings_object_before.stimulus_color = NEW_STIMULUS_COLOR
        usersettings_object_before.background_color = NEW_BACKGROUND_COLOR
        usersettings_object_before.rotaryencoder_thresholds = NEW_ROTARYENCODER_THRESHOLDS
        usersettings_object_before.stimulus_end_position = NEW_STIMULUS_END_POSITION
        usersettings_object_before.life_plot = NEW_LIFE_PLOT
        usersettings_object_before.animal_weight = NEW_ANIMAL_WEIGHT

        usersettings_object_before.update_userinput_file_gamble()

        import_file = os.path.join(self.settings_folder_path, "usersettings.py")
        spec = importlib.util.spec_from_file_location("write_test_usersettings_example_gamble_task", import_file)
        usersettings_example_import_after = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(usersettings_example_import_after)
        usersettings_object_after = TrialParameterHandler(
            usersettings_example_import_after, self.settings_folder_path, self.session_folder_path
        )

        self.assertEqual(usersettings_object_after.task_name, NEW_TASK)
        self.assertEqual(usersettings_object_after.gamble_side, NEW_GAMBLE_SIDE)
        self.assertEqual(usersettings_object_after.blocks, NEW_BLOCKS)
        self.assertEqual(usersettings_object_after.big_reward, NEW_BIG_REWARD)
        self.assertEqual(usersettings_object_after.small_reward, NEW_SMALL_REWARD)
        self.assertEqual(usersettings_object_after.last_callibration, NEW_LAST_CALLIBRATION)

        for key, item in new_time_dict.items():
            self.assertEqual(usersettings_object_after.time_dict[key], item)

        self.assertEqual(usersettings_object_after.stimulus_radius, NEW_STIMULUS_RADIUS)
        self.assertEqual(usersettings_object_after.stimulus_color, NEW_STIMULUS_COLOR)
        self.assertEqual(usersettings_object_after.background_color, NEW_BACKGROUND_COLOR)
        self.assertEqual(usersettings_object_after.rotaryencoder_thresholds, NEW_ROTARYENCODER_THRESHOLDS)
        self.assertEqual(usersettings_object_after.stimulus_end_position, NEW_STIMULUS_END_POSITION)
        self.assertEqual(usersettings_object_after.life_plot, NEW_LIFE_PLOT)
        self.assertEqual(usersettings_object_after.animal_weight, NEW_ANIMAL_WEIGHT)

        self.assertEqual(usersettings_object_after.big_reward, NEW_BIG_REWARD)
        self.assertEqual(usersettings_object_after.small_reward, NEW_SMALL_REWARD)
        self.assertEqual(usersettings_object_after.gamble_side, NEW_GAMBLE_SIDE)

    def test_save_complete_usersettings_to_file(self):
        usersettings_object_before = TrialParameterHandler(
            self.usersettings_example_import, self.settings_folder_path, self.session_folder_path
        )
        usersettings_object_before.update_userinput_file_gamble()
        saved_file = os.path.join(self.settings_folder_path, "usersettings.py")

        self.assertFalse(filecmp.cmp(USERSETTINGS_EXAMPLE_GAMBLE_TASK, saved_file))
