import importlib.util
import os
import shutil
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from maxland.parameter_handler import TrialParameterHandler

USERSETTINGS_EXAMPLE_GAMBLE_TASK = os.path.join(os.path.dirname(__file__), "usersettings_example_gamble_task.py")


class TestTrialParameterHandlerGambleTask(unittest.TestCase):
    def setUp(self):

        currentdir = os.path.dirname(__file__)
        self.test_folder_path = Path(os.path.join(currentdir, "test_folder"))
        self.settings_folder_path = Path(os.path.join(self.test_folder_path, "settings_folder"))
        self.session_folder_path = Path(os.path.join(self.test_folder_path, "session_folder"))
        self.create_test_folders()

        import_file = os.path.join(currentdir, "usersettings_example_gamble_task.py")
        spec = importlib.util.spec_from_file_location("test", import_file)
        usersettings_example_import = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(usersettings_example_import)
        self.usersettings_object = TrialParameterHandler(
            usersettings_example_import, self.settings_folder_path, self.session_folder_path
        )

    def tearDown(self):
        self.delete_test_folders()

    def create_test_folders(self):
        self.settings_folder_path.mkdir(parents=True, exist_ok=True)
        self.session_folder_path.mkdir(parents=True, exist_ok=True)

    def delete_test_folders(self):
        shutil.rmtree(self.test_folder_path, ignore_errors=True)

    def test_get_parameters_from_settings_file(self):
        print(self.usersettings_object.task)
        pass
