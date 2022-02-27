import importlib.util
import os
import sys
import unittest
from pathlib import Path

# from pybpodapi.bpod import Bpod

# from unittest.mock import patch


# from maxland.helperfunctions import find_bpod_com_port, find_rotaryencoder_com_port

USERSETTINGS_EXAMPLE = os.path.join(
    Path(os.path.dirname(__file__)).parent.absolute().parent.absolute(), "usersettings_example_gamble_task.py"
)

GAMBLE_TASK_TRAINING = os.path.join(
    Path(os.path.dirname(__file__)).parent.absolute().parent.absolute().parent.absolute(),
    "tasks",
    "gamble_task",
    "gamble_task_training",
    "gamble_task_training.py",
)

# hardware in the loop tests
class TestGambleTaskTraining(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("usersettings", USERSETTINGS_EXAMPLE)
        self.usersettings = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.usersettings)

        sys.modules["usersettings"] = self.usersettings

        # bpod_com_port = find_bpod_com_port()
        # self.bpod = Bpod(bpod_com_port)

    def tearDown(self):
        self.usersettings_example_import = None
        self.bpod.close()
        self.bpod = None

    # patch bpod
    # add
    # @patch("Bpod()")
    def test_load_gamble_task_training(self):
        # Bpod.main.mockside_effect = self.bpod()
        spec = importlib.util.spec_from_file_location("gamble_task_training", GAMBLE_TASK_TRAINING)
        gamble_task_training = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gamble_task_training)

        gamble_task_training.bpod = self.bpod

        gamble_task_training.main()
