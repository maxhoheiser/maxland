import importlib.util
import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from maxland.parameter_handler import TrialParameterHandler
from maxland.rotaryencoder import BpodRotaryEncoder

USERSETTINGS_EXAMPLE = os.path.join(Path(os.path.dirname(__file__)).parent.absolute(), "usersettings_example_gamble_task.py")
COM_PORT = "COM1"

# hardware in the loop tests
class TestBpodRotaryEncoderModule(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("usersettings_example", USERSETTINGS_EXAMPLE)
        self.usersettings_example_import = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.usersettings_example_import)
        self.usersettings_object = TrialParameterHandler(self.usersettings_example_import, "", "")
        self.bpod = MagicMock()
        self.bpod.modules.return_vale = [
            {"name": "OtherName", "other": "other"},
            {"name": "RotaryEncoder1", "other": "other"},
        ]
        self.bpod.load_serial_message.return_value = None

    def tearDown(self):
        self.usersettings_example_import = None

    def test_create_rotaryencodermodule(self):
        BpodRotaryEncoder(COM_PORT, self.usersettings_object, self.bpod)
