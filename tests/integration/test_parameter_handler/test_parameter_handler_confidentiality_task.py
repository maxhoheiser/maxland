import filecmp
import importlib.util
import os
import shutil
import unittest
from pathlib import Path

from maxland.parameter_handler import TrialParameterHandler
from maxland.types_time_dict import TimeDict
from maxland.types_usersettings import TaskName

USERSETTINGS_EXAMPLE_CONFIDENTIALITY_TASK = os.path.join(
    Path(os.path.dirname(__file__)).parent.absolute().parent.absolute(), "usersettings_example_conf_task.py"
)

# Mock usersettings data
NEW_TASK = TaskName.CONFIDENTIALITY
NEW_TRIAL_NUMBER = 31
NEW_STIMULUS_TYPE = "three-stimuli"  # three-stimuli #two-stimuli #one-stimulus
NEW_STIMULUS_CORRECT = {"grating_sf": 0.02, "grating_ori": 0.2, "grating_size": 41.0, "grating_speed": 0.05}
NEW_STIMULUS_WRONG = {"grating_sf": 0.03, "grating_ori": 91.0, "grating_size": 41.0, "grating_speed": 0.03}
# reward in seconds
NEW_REWARD = 0.14
NEW_LAST_CALLIBRATION = "2020.06.10"
# trial times
NEW_TIME_START = 2.0
NEW_TIME_WHEEL_STOPPING_CHECK = 2.0
NEW_TIME_WHEEL_STOPPING_PUNISH = 2.0
NEW_TIME_PRESENT_STIMULUS = 1.2
NEW_TIME_OPEN_LOOP = 10.2
NEW_TIME_OPEN_LOOP_FAIL_PUNISH = 1.0
NEW_TIME_STIMULUS_FREEZE = 2.2
NEW_TIME_REWARD = 1.3
NEW_TIME_RANGE_NO_REWARD_PUNISH = [0.1, 0.2]
NEW_TIME_INTER_TRIAL = 1.4
# insist mode
NEW_INSIST_RANGE_TRIGGER = 20
NEW_INSIST_CORRECT_DEACTIVATE = 4
NEW_INSIST_RANGE_DEACTIVATE = 10
# rule switching
NEW_RULE_SWITCH_INITIAL_TRIALS_WAIT = 12
NEW_RULE_SWITCH_CHECK_TRIAL_RANGE = 12
NEW_RULE_SWITCH_TRIALS_CORRECT_TRIGGER_SWITCH = 89
NEW_FADE_START = 1952
NEW_FADE_END = 3003
# stimulus size and color - only for moving stimulus
NEW_STIMULUS_RADIUS = 46
NEW_STIMULUS_COLOR = [1, 252, 5]
NEW_BACKGROUND_COLOR = [1, 3, 4]
# thresholds
NEW_ROTARYENCODER_THRESHOLDS = [-91, 91, -3, 3]
NEW_STIMULUS_END_POSITION = [-2046, 2047]
NEW_LIFE_PLOT = True
NEW_ANIMAL_WEIGHT = 10.1


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


class TestTrialParameterHandlerConfTask(unittest.TestCase):
    def setUp(self):
        (
            _,
            self.test_folder_path,
            self.settings_folder_path,
            self.session_folder_path,
        ) = get_test_folder_paths(__file__)
        create_folder(self.settings_folder_path)
        create_folder(self.session_folder_path)

        spec = importlib.util.spec_from_file_location("usersettings_example_conf_task", USERSETTINGS_EXAMPLE_CONFIDENTIALITY_TASK)
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
        usersettings_object_before.trial_number = NEW_TRIAL_NUMBER
        usersettings_object_before.stimulus_type = NEW_STIMULUS_TYPE
        usersettings_object_before.stimulus_correct_side = NEW_STIMULUS_CORRECT
        usersettings_object_before.stimulus_wrong_side = NEW_STIMULUS_WRONG
        usersettings_object_before.reward = NEW_REWARD
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
            "time_range_no_reward_punish": NEW_TIME_RANGE_NO_REWARD_PUNISH,
            "time_inter_trial": NEW_TIME_INTER_TRIAL,
        }
        usersettings_object_before.time_dict = new_time_dict

        usersettings_object_before.insist_range_trigger = NEW_INSIST_RANGE_TRIGGER
        usersettings_object_before.insist_correct_deactivate = NEW_INSIST_CORRECT_DEACTIVATE
        usersettings_object_before.insist_range_deactivate = NEW_INSIST_RANGE_DEACTIVATE

        usersettings_object_before.rule_switch_initial_trials_wait = NEW_RULE_SWITCH_INITIAL_TRIALS_WAIT
        usersettings_object_before.rule_switch_check_trial_range = NEW_RULE_SWITCH_CHECK_TRIAL_RANGE
        usersettings_object_before.rule_switch_trials_correct_trigger_switch = NEW_RULE_SWITCH_TRIALS_CORRECT_TRIGGER_SWITCH

        usersettings_object_before.fade_start = NEW_FADE_START
        usersettings_object_before.fade_end = NEW_FADE_END

        usersettings_object_before.stimulus_radius = NEW_STIMULUS_RADIUS
        usersettings_object_before.stimulus_color = NEW_STIMULUS_COLOR
        usersettings_object_before.background_color = NEW_BACKGROUND_COLOR
        usersettings_object_before.rotaryencoder_thresholds = NEW_ROTARYENCODER_THRESHOLDS
        usersettings_object_before.stimulus_end_position = NEW_STIMULUS_END_POSITION
        usersettings_object_before.life_plot = NEW_LIFE_PLOT
        usersettings_object_before.animal_weight = NEW_ANIMAL_WEIGHT

        usersettings_object_before.update_userinput_file_conf()

        import_file = os.path.join(self.settings_folder_path, "usersettings.py")
        spec = importlib.util.spec_from_file_location("write_test_usersettings_example_conf_task", import_file)
        usersettings_example_import_after = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(usersettings_example_import_after)

        usersettings_object_after = TrialParameterHandler(
            usersettings_example_import_after, self.settings_folder_path, self.session_folder_path
        )

        self.assertEqual(usersettings_object_after.task_name, NEW_TASK)
        self.assertEqual(usersettings_object_after.trial_number, NEW_TRIAL_NUMBER)
        self.assertEqual(usersettings_object_after.stimulus_type, NEW_STIMULUS_TYPE)
        self.assertEqual(usersettings_object_after.stimulus_correct_side, NEW_STIMULUS_CORRECT)
        self.assertEqual(usersettings_object_after.stimulus_wrong_side, NEW_STIMULUS_WRONG)

        self.assertEqual(usersettings_object_after.reward, NEW_REWARD)
        self.assertEqual(usersettings_object_after.last_callibration, NEW_LAST_CALLIBRATION)

        for key, item in new_time_dict.items():
            self.assertEqual(usersettings_object_after.time_dict[key], item)

        self.assertEqual(usersettings_object_after.insist_range_trigger, NEW_INSIST_RANGE_TRIGGER)
        self.assertEqual(usersettings_object_after.insist_correct_deactivate, NEW_INSIST_CORRECT_DEACTIVATE)
        self.assertEqual(usersettings_object_after.insist_range_deactivate, NEW_INSIST_RANGE_DEACTIVATE)

        self.assertEqual(usersettings_object_after.rule_switch_initial_trials_wait, NEW_RULE_SWITCH_INITIAL_TRIALS_WAIT)
        self.assertEqual(usersettings_object_after.rule_switch_check_trial_range, NEW_RULE_SWITCH_CHECK_TRIAL_RANGE)
        self.assertEqual(usersettings_object_after.rule_switch_trials_correct_trigger_switch, NEW_RULE_SWITCH_TRIALS_CORRECT_TRIGGER_SWITCH)

        self.assertEqual(usersettings_object_after.fade_start, NEW_FADE_START)
        self.assertEqual(usersettings_object_after.fade_end, NEW_FADE_END)

        self.assertEqual(usersettings_object_after.stimulus_radius, NEW_STIMULUS_RADIUS)
        self.assertEqual(usersettings_object_after.stimulus_color, NEW_STIMULUS_COLOR)
        self.assertEqual(usersettings_object_after.background_color, NEW_BACKGROUND_COLOR)
        self.assertEqual(usersettings_object_after.rotaryencoder_thresholds, NEW_ROTARYENCODER_THRESHOLDS)
        self.assertEqual(usersettings_object_after.stimulus_end_position, NEW_STIMULUS_END_POSITION)
        self.assertEqual(usersettings_object_after.life_plot, NEW_LIFE_PLOT)
        self.assertEqual(usersettings_object_after.animal_weight, NEW_ANIMAL_WEIGHT)

    def test_save_complete_usersettings_to_file(self):
        usersettings_object_before = TrialParameterHandler(
            self.usersettings_example_import, self.settings_folder_path, self.session_folder_path
        )
        usersettings_object_before.update_userinput_file_conf()
        saved_file = os.path.join(self.settings_folder_path, "usersettings.py")

        self.assertFalse(filecmp.cmp(USERSETTINGS_EXAMPLE_CONFIDENTIALITY_TASK, saved_file))

    def test_create_time_dict(self):
        usersettings_object = TrialParameterHandler(self.usersettings_example_import, self.settings_folder_path, self.session_folder_path)
        usersettings_object.create_time_dictionary()
