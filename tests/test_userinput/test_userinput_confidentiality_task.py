import importlib.util
import os
import unittest
from pathlib import Path

from maxland.parameter_handler import TrialParameterHandler
from maxland.userinput import UserInput

USERSETTINGS = os.path.join(Path(os.path.dirname(__file__)).parent.absolute(), "usersettings_example_conf_task.py")


class TestUserInputConfidentialityTask(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("usersettings", USERSETTINGS)
        self.usersettings_example_import = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.usersettings_example_import)
        self.parameter_handler = TrialParameterHandler(self.usersettings_example_import, "", "")

    def tearDown(self):
        self.parameter_handler = None

    def test_draw_userinput_window(self):
        window = UserInput(self.parameter_handler)
        window.draw_window_before()
        window.on_close()
