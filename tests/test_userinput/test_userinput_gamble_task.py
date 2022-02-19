import importlib.util
import os
import time
import unittest
from pathlib import Path

from maxland.parameter_handler import TrialParameterHandler
from maxland.userinput import UserInput

USERSETTINGS = os.path.join(Path(os.path.dirname(__file__)).parent.absolute(), "usersettings_example_gamble_task.py")
NEW_GAMBLE_SIDE = "right"


class TestUserInputGambleTask(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("usersettings", USERSETTINGS)
        self.usersettings_example_import = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.usersettings_example_import)
        self.parameter_handler = TrialParameterHandler(self.usersettings_example_import, "", "")

    def tearDown(self):
        self.parameter_handler = None

    def click_on_widget(self, widget, x, y, button=1):
        widget.focus_force()
        widget.event_generate(f"<ButtonPress-{button}>", x=x, y=y)
        widget.update_idletasks()

    def test_draw_userinput_window(self):
        window = UserInput(self.parameter_handler)
        window.draw_window_before()
        window.root.update_idletasks()
        window.on_close()

    def test_on_configm(self):
        window = UserInput(self.parameter_handler)
        window.draw_window_before()
        widget = window.root
        widget.update_idletasks()
        window.on_confirm()

        self.assertTrue(self.parameter_handler.run_session)

    def test_on_cancel(self):
        window = UserInput(self.parameter_handler)
        window.draw_window_before()
        widget = window.root
        widget.update_idletasks()
        window.on_cancel()

        self.assertFalse(self.parameter_handler.run_session)

    def test_change_gamble_side(self):
        window = UserInput(self.parameter_handler)
        window.draw_window_before()
        widget = window.root
        widget.update_idletasks()

        window.var_gamble_side.set("left")

        window.on_confirm()

        self.assertFalse(self.parameter_handler.run_session)


# test change gamble side

# test change block 1,2,3 (block test class)
## time range
## probability gamble
## probability save

# test reward gamble reward save
# test stimulus
# window background
# stim radius
# stim color
# stim end pos left,right
# wheel streshold left,right

# time
# start time
# stopp time
# not stop punish
# stim pres
# open loop
# open loop fail
# stim freeze
# reward
# trial end
