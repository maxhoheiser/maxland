import importlib.util
import os
import unittest
from pathlib import Path

from pybpodapi.bpod import Bpod

from maxland.helperfunctions import find_bpod_com_port, find_rotaryencoder_com_port
from maxland.parameter_handler import TrialParameterHandler
from maxland.rotaryencoder import BpodRotaryEncoder

USERSETTINGS_EXAMPLE = os.path.join(Path(os.path.dirname(__file__)).parent.absolute(), "usersettings_example_gamble_task.py")

# hardware in the loop tests
class TestBpodRotaryEncoderModule(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("usersettings_example", USERSETTINGS_EXAMPLE)
        self.usersettings_example_import = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.usersettings_example_import)
        self.usersettings_object = TrialParameterHandler(self.usersettings_example_import, "", "")
        bpod_com_port = find_bpod_com_port()
        self.bpod = Bpod(bpod_com_port)
        self.com_port = find_rotaryencoder_com_port()

    def tearDown(self):
        self.usersettings_example_import = None

    def test_com_port_found(self):
        self.assertIsNotNone(self.com_port)

    def test_connect_to_rotary_encoder(self):
        rotary_encoder = BpodRotaryEncoder(self.com_port, self.usersettings_object, self.bpod)
        self.assertIsNotNone(rotary_encoder)
