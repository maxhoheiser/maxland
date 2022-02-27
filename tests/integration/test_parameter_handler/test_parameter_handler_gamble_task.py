import filecmp
import importlib.util
import os
import shutil
import unittest
from pathlib import Path

from maxland.parameter_handler import TrialParameterHandler

USERSETTINGS_EXAMPLE_GAMBLE_TASK = os.path.join(
    Path(os.path.dirname(__file__)).parent.absolute().parent.absolute(), "usersettings_example_gamble_task.py"
)
NEW_BIG_REWARD = 10.15
NEW_SMALL_REWARD = 11.16


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
        usersettings_object_before.big_reward = NEW_BIG_REWARD
        usersettings_object_before.small_reward = NEW_SMALL_REWARD
        usersettings_object_before.update_userinput_file_gamble()

        import_file = os.path.join(self.settings_folder_path, "usersettings.py")
        spec = importlib.util.spec_from_file_location("write_test_usersettings_example_gamble_task", import_file)
        usersettings_example_import_after = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(usersettings_example_import_after)
        usersettings_object_after = TrialParameterHandler(
            usersettings_example_import_after, self.settings_folder_path, self.session_folder_path
        )

        self.assertEqual(usersettings_object_after.big_reward, NEW_BIG_REWARD)
        self.assertEqual(usersettings_object_after.small_reward, NEW_SMALL_REWARD)

    def test_save_complete_usersettings_to_file(self):
        usersettings_object_before = TrialParameterHandler(
            self.usersettings_example_import, self.settings_folder_path, self.session_folder_path
        )
        usersettings_object_before.update_userinput_file_gamble()
        saved_file = os.path.join(self.settings_folder_path, "usersettings.py")

        self.assertFalse(filecmp.cmp(USERSETTINGS_EXAMPLE_GAMBLE_TASK, saved_file))
