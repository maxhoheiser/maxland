from math import tan as tan
from threading import Event
from typing import Dict

from psychopy import core, monitors, visual

from maxland.parameter_handler import TrialParameterHandler
from maxland.rotaryencoder import BpodRotaryEncoder


class Stimulus:
    """
    Create the stimulus via pygame and pyglet with psychopy
    Args:
        settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler
        rotary_encoder (RotaryEncoder object): object handeling rotary encoder module
    """

    def __init__(self, settings: TrialParameterHandler, rotary_encoder: BpodRotaryEncoder):
        self.settings = settings
        self.FPS = settings.fps
        self.monitor_width = settings.monitor_width
        self.monitor_distance = settings.monitor_distance
        self.screen_size = (
            settings.screen_width,
            settings.screen_height,
        )
        self.rotary_encoder = rotary_encoder

        self.gain_left = self.get_gain(settings.rotaryencoder_thresholds[0], settings.rotaryencoder_stimulus_end_position[0])
        self.gain_right = self.get_gain(settings.rotaryencoder_thresholds[1], settings.rotaryencoder_stimulus_end_position[1])
        self.gain = self.gain_left

        self.monitor = monitors.Monitor("testMonitor", width=self.monitor_width, distance=self.monitor_distance)
        self.monitor.setSizePix(self.screen_size)

        self.win = visual.Window(
            size=(self.screen_size),
            fullscr=True,
            screen=1,
            monitor=self.monitor,
            units="pix",
            winType="pyglet",
            allowGUI=False,
            allowStencil=False,
            color=self.settings.background_color,
            colorSpace="rgb",
            blendMode="avg",
            useFBO=True,
        )
        self.win.winHandle.maximize()
        self.win.flip()

        expInfo = {}
        expInfo["frameRate"] = self.win.getActualFrameRate()

        self.stimulus_radius = settings.stimulus_radius
        self.stimulus_color = settings.stimulus_color

        self.run_open_loop = True

    # helper functions
    def get_gratings_size_in_pixels(self, grating_size):
        stim_half_width = self.monitor_distance * tan(grating_size / 2)
        return (stim_half_width / self.monitor_width) * self.screen_size[0]

    def get_gain(self, threshold, stim_end_pos):
        gain = abs(stim_end_pos / threshold)
        return round(gain, 2)

    def ceil(self, num):
        if num > 30:
            return 30
        else:
            return num

    def on_close(self):
        self.win.close()
        core.quit()

    def stop_open_loop(self):
        self.run_open_loop = False

    # stimulus functions
    def get_stimulus(self):
        circle = visual.Circle(
            win=self.win,
            name="circle",
            radius=self.stimulus_radius,
            units="pix",
            edges=128,
            fillColor=self.stimulus_color,
            pos=(0, 0),
        )
        return circle

    # psychpy loop
    EventFlags = Dict[str, Event]

    def run_game(self, event_flags: EventFlags):
        event_display_stimulus = event_flags["event_display_stimulus"]
        event_start_open_loop = event_flags["event_start_open_loop"]
        event_still_show_stimulus = event_flags["event_still_show_stimulus"]
        # get right grating
        stimulus = self.get_stimulus()
        stimulus.draw()
        # on soft code of state 1
        # present initial stimulus
        event_display_stimulus.wait()
        self.win.flip()
        # on soft code of state 2
        event_start_open_loop.wait()
        # open loop
        print("open loop")
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        while self.run_open_loop:
            # get rotary encoder change position
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain
                pos = stream[-1][2]
                stimulus.pos += (change, 0)
            stimulus.draw()
            self.win.flip()
        # on soft code of state 3 freeze movement
        event_still_show_stimulus.wait()
        print("end")
        self.win.flip()
        # cleanup for next loop
        self.run_open_loop = True
        event_display_stimulus.clear()
        event_start_open_loop.clear()
        event_still_show_stimulus.clear()
