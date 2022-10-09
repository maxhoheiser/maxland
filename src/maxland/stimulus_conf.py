import random
from threading import Event
from typing import Dict

from psychopy import monitors, tools, visual

from maxland.parameter_handler import TrialParameterHandler
from maxland.rotaryencoder import BpodRotaryEncoder


class Stimulus:
    """
    Create the stimulus via pygame and pyglet with psychopy
    Args:
        settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler
        rotary_encoder (RotaryEncoder object): object handeling rotary encoder module
    """

    def __init__(self, settings: TrialParameterHandler, rotary_encoder: BpodRotaryEncoder, stimulus_sides: Dict[str, bool]):
        self.settings = settings
        self.trials = settings.trial_number
        self.FPS = settings.fps
        self.monitor_width = settings.monitor_width
        self.monitor_distance = settings.monitor_distance
        self.screen_size = (
            settings.screen_width,
            settings.screen_height,
        )

        self.rotary_encoder = rotary_encoder
        self.stimulus_sides = stimulus_sides

        self.gain_left = self.get_gain(settings.rotaryencoder_thresholds[0], settings.stimulus_end_position[0])
        self.gain_right = self.get_gain(settings.rotaryencoder_thresholds[1], settings.stimulus_end_position[1])
        self.gain = self.gain_left

        self.monitor = monitors.Monitor("testMonitor", width=self.monitor_width, distance=self.monitor_distance)
        self.monitor.setSizePix(self.screen_size)

        self.win = visual.Window(
            size=(self.screen_size),
            fullscr=True,
            screen=2,
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

        self.run_closed_loop_before = True
        self.run_open_loop = True
        self.run_closed_loop_after = True

        self.fade_start = abs(self.settings.fade_start)
        self.fade_end = abs(self.settings.fade_end)
        self.fade_range = self.fade_end - self.fade_start

    # helper functions
    def get_grating_size(self, degree):
        return tools.monitorunittools.deg2pix(degree, self.monitor)

    def get_grating_frequency(self, frequency):
        return frequency

    def get_gain(self, threshold, stimulus_end_position):
        gain = abs(stimulus_end_position / threshold)
        return round(gain, 2)

    def ceil(self, num):
        if num > 10:
            return 10
        else:
            return num

    def on_close(self):
        self.win.close()
        # core.quit()

    def stop_closed_loop_before(self):
        self.run_closed_loop_before = False

    def stop_open_loop(self):
        self.run_open_loop = False

    def stop_closed_loop_after(self):
        self.run_closed_loop_after = False

    def reset_loop_flags(self):
        self.run_closed_loop_before = True
        self.run_open_loop = True
        self.run_closed_loop_after = True

    # stimulus functions
    def gen_grating(self, grating_frequency, grating_orientation, grating_size, position):
        grating = visual.GratingStim(
            win=self.win,
            tex="sin",  # texture used
            pos=(position, 0),
            units="pix",  # "deg",#'deg', # size in degrees for correct stim size
            size=grating_size,
            sf=grating_frequency,
            ori=grating_orientation,
            contrast=1,  # unchanged contrast (from 1 to -1)
            mask="raisedCos",
            opacity=1.0,  # ranging 1.0 (opaque) to 0.0 (transparent)
        )
        return grating

    def gen_stimulus(self):
        circle = visual.Circle(
            win=self.win,
            name="circle",
            radius=self.get_grating_size(self.stimulus_radius) / 2,  # convet from vis angle to pixel and fomr diameter to radius
            units="pix",
            edges=128,
            fillColor=self.stimulus_color,
            pos=(0, 0),
            opacity=1.0,
        )
        return circle

    def get_opacity(self, pos):
        opacity = (self.fade_end - abs(pos)) / self.fade_range
        return round(opacity, 1)

    def get_stim_end_position(self):
        pos_x = self.settings.stimulus_end_position[0]
        pos_y = 0
        return [pos_x, pos_y]

    # Main psychpy loop
    EventFlags = Dict[str, Event]

    # Stimulus Type 3 (main) = fixed gratings + moving circle ==========================
    def run_game_3(self, event_flags: EventFlags):
        event_display_stimulus = event_flags["event_display_stimulus"]

        event_display_stimulus.clear()
        self.reset_loop_flags()

        if self.stimulus_sides["right"]:
            right_frequency = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_frequency"])
            right_orientation = self.settings.stimulus_correct_side["grating_orientation"]
            right_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
            right_speed = self.settings.stimulus_correct_side["grating_speed"]
            left_frequency = self.get_grating_frequency(self.settings.stimulus_wrong_side["grating_frequency"])
            left_orientation = self.settings.stimulus_wrong_side["grating_orientation"]
            left_size = self.get_grating_size(self.settings.stimulus_wrong_side["grating_size"])
            left_speed = self.settings.stimulus_correct_side["grating_speed"]

        if self.stimulus_sides["left"]:
            left_frequency = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_frequency"])
            left_orientation = self.settings.stimulus_correct_side["grating_orientation"]
            left_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
            left_speed = self.settings.stimulus_correct_side["grating_speed"]
            right_frequency = self.get_grating_frequency(self.settings.stimulus_wrong_side["grating_frequency"])
            right_orientation = self.settings.stimulus_wrong_side["grating_orientation"]
            right_size = self.get_grating_size(self.settings.stimulus_wrong_side["grating_size"])
            right_speed = self.settings.stimulus_correct_side["grating_speed"]

        grating_left = self.gen_grating(left_frequency, left_orientation, left_size, self.settings.stimulus_end_position[0])
        grating_right = self.gen_grating(right_frequency, right_orientation, right_size, self.settings.stimulus_end_position[1])
        stim = self.gen_stimulus()

        # on soft code of state 1 ----------------------
        event_display_stimulus.wait()
        while self.run_closed_loop_before:
            grating_left.setPhase(left_speed, "+")
            grating_right.setPhase(right_speed, "+")
            grating_left.draw()
            grating_right.draw()
            stim.draw()
            self.win.flip()

        # on soft code of state 2 ----------------------
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()

        while self.run_open_loop:
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            grating_left.setPhase(left_speed, "+")  # advance phase by 0.05 of a cycle
            grating_right.setPhase(right_speed, "+")
            grating_left.draw()
            grating_right.draw()
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain
                # if very fast rotation still threshold, but stimulus not there
                pos = stream[-1][2]
                stim.pos += (change, 0)
            stim.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()

        # on soft code of state 3 freeze movement ---------
        stim.pos = self.get_stim_end_position()
        while self.run_closed_loop_after:
            grating_left.setPhase(left_speed, "+")
            grating_right.setPhase(right_speed, "+")
            grating_left.draw()
            grating_right.draw()
            stim.draw()
            self.win.flip()
        self.win.flip()

        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()

    # Stimulus Type 2 = moving gratings ================================================
    def run_game_2(self, event_flags: EventFlags):
        event_display_stimulus = event_flags["event_display_stimulus"]

        event_display_stimulus.clear()
        self.reset_loop_flags()

        if self.stimulus_sides["left"]:
            right_frequency = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_frequency"])
            right_orientation = self.settings.stimulus_correct_side["grating_orientation"]
            right_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
            right_speed = self.settings.stimulus_correct_side["grating_speed"]
            left_frequency = self.get_grating_frequency(self.settings.stimulus_wrong_side["grating_frequency"])
            left_orientation = self.settings.stimulus_wrong_side["grating_orientation"]
            left_size = self.get_grating_size(self.settings.stimulus_wrong_side["grating_size"])
            left_speed = self.settings.stimulus_correct_side["grating_speed"]

        if self.stimulus_sides["right"]:
            left_frequency = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_frequency"])
            left_orientation = self.settings.stimulus_correct_side["grating_orientation"]
            left_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
            left_speed = self.settings.stimulus_correct_side["grating_speed"]
            right_frequency = self.get_grating_frequency(self.settings.stimulus_wrong_side["grating_frequency"])
            right_orientation = self.settings.stimulus_wrong_side["grating_orientation"]
            right_size = self.get_grating_size(self.settings.stimulus_wrong_side["grating_size"])
            right_speed = self.settings.stimulus_correct_side["grating_speed"]

        grating_left = self.gen_grating(left_frequency, left_orientation, left_size, self.settings.stimulus_end_position[0])
        grating_right = self.gen_grating(right_frequency, right_orientation, right_size, self.settings.stimulus_end_position[1])

        # on soft code of state 1 ----------------------
        event_display_stimulus.wait()
        while self.run_closed_loop_before:
            grating_left.setPhase(left_speed, "+")
            grating_right.setPhase(right_speed, "+")
            grating_left.draw()
            grating_right.draw()
            self.win.flip()

        # on soft code of state 2 ----------------------
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()

        while self.run_open_loop:
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            grating_left.setPhase(left_speed, "+")  # advance phase by 0.05 of a cycle
            grating_right.setPhase(right_speed, "+")
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain
                # if ceil -> if very fast rotation still threshold, but stimulus not there
                pos = stream[-1][2]
                grating_left.pos += (change, 0)
                grating_right.pos += (change, 0)

                if grating_left.pos[0] < -self.fade_start:
                    grating_left.opacity = self.get_opacity(grating_left.pos[0])

                if grating_right.pos[0] > self.fade_start:
                    grating_right.opacity = self.get_opacity(grating_right.pos[0])

            grating_left.draw()
            grating_right.draw()
            self.win.flip()

        self.rotary_encoder.rotary_encoder.disable_stream()

        # on soft code of state 3 freez movement ---------
        while self.run_closed_loop_after:
            grating_left.setPhase(left_speed, "+")
            grating_right.setPhase(right_speed, "+")
            grating_left.draw()
            grating_right.draw()
            self.win.flip()
        self.win.flip()

        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()

    # Stimulus Type 1 = single moving grating ==========================================
    def run_game_1(self, event_flags: EventFlags):
        event_display_stimulus = event_flags["event_display_stimulus"]

        if self.stimulus_sides["right"]:
            stimulus = self.settings.stimulus_correct_side
        if self.stimulus_sides["left"]:
            stimulus = self.settings.stimulus_wrong_side
        stim_sf = self.get_grating_frequency(stimulus["grating_frequency"])
        stim_or = stimulus["grating_orientation"]
        stim_size = self.get_grating_size(stimulus["grating_size"])
        stim_ps = stimulus["grating_speed"]

        grating = self.gen_grating(stim_sf, stim_or, stim_size, 0)

        # on soft code of state 1 ----------------------
        event_display_stimulus.wait()
        while self.run_closed_loop_before:
            grating.setPhase(stim_ps, "+")
            grating.draw()
            self.win.flip()

        # on soft code of state 2 ----------------------
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()

        while self.run_open_loop:
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            grating.setPhase(stim_ps, "+")
            grating.draw()
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain
                # if ceil -> if very fast rotation still threshold, but stimulus not there
                pos = stream[-1][2]
                grating.pos += (change, 0)
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()

        # on soft code of state 3 freeze movement ---------
        grating.pos = self.get_stim_end_position()
        while self.run_closed_loop_after:
            grating.setPhase(stim_ps, "+")
            grating.draw()
            self.win.flip()
        self.win.flip()

        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()

    # Habituation  Type 3 online center stim psychopy Loop =============================
    def run_game_habituation_3_simple(self, event_flags: EventFlags):
        event_display_stimulus = event_flags["event_display_stimulus"]
        event_start_open_loop = event_flags["event_start_open_loop"]
        event_still_show_stimulus = event_flags["event_still_show_stimulus"]

        stim = self.gen_stimulus()
        stim.draw()

        # on soft code of state 1 ----------------------
        event_display_stimulus.wait()
        self.win.flip()

        # on soft code of state 2 ----------------------
        event_start_open_loop.wait()

        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()

        while self.run_open_loop:
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain
                # if ceil -> if very fast rotation still threshold, but stimulus not there
                pos = stream[-1][2]
                stim.pos += (change, 0)
            stim.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()

        # on soft code of state 3 freeze movement ---------
        stim.pos = self.get_stim_end_position()
        event_still_show_stimulus.wait()
        self.win.flip()

        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()
        event_start_open_loop.clear()
        event_still_show_stimulus.clear()

    # Habituation Typ 3 only single correct grating ====================================
    def run_game_habituation_3_complex(self, event_flags: EventFlags):
        event_display_stimulus = event_flags["event_display_stimulus"]

        grating_frequency = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_frequency"])
        grating_or = self.settings.stimulus_correct_side["grating_orientation"]
        grating_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
        grating_ps = self.settings.stimulus_correct_side["grating_speed"]

        if self.stimulus_sides["right"]:
            grating = self.gen_grating(grating_frequency, grating_or, grating_size, self.settings.stimulus_end_position[1])

        if self.stimulus_sides["left"]:
            grating = self.gen_grating(grating_frequency, grating_or, grating_size, self.settings.stimulus_end_position[0])

        stim = self.gen_stimulus()
        stim.draw()

        # on soft code of state 1 ----------------------
        event_display_stimulus.wait()
        self.win.flip()
        while self.run_closed_loop_before:
            grating.setPhase(grating_ps, "+")
            grating.draw()
            stim.draw()
            self.win.flip()

        # on soft code of state 2 ----------------------
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()

        while self.run_open_loop:
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            # dram moving gratings
            grating.setPhase(grating_ps, "+")
            grating.draw()
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain
                # if ceil -> if very fast rotation still threshold, but stimulus not there
                pos = stream[-1][2]
                stim.pos += (change, 0)
            stim.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()

        # on soft code of state 3 freeze movement ---------
        stim.pos = self.get_stim_end_position()
        while self.run_closed_loop_after:
            grating.setPhase(grating_ps, "+")
            grating.draw()
            stim.draw()
            self.win.flip()
        self.win.flip()

        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()

    # Habituation Typ 2 complex ========================================================
    def run_game_habituation_2(self, event_flags: EventFlags):
        event_display_stimulus = event_flags["event_display_stimulus"]

        random_grating = bool(random.getrandbits(1))

        if random_grating:
            grating_frequency = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_frequency"])
            grating_or = self.settings.stimulus_correct_side["grating_orientation"]
            grating_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
            grating_ps = self.settings.stimulus_correct_side["grating_speed"]
        else:
            grating_frequency = self.get_grating_frequency(self.settings.stimulus_wrong_side["grating_frequency"])
            grating_or = self.settings.stimulus_wrong_side["grating_orientation"]
            grating_size = self.get_grating_size(self.settings.stimulus_wrong_side["grating_size"])
            grating_ps = self.settings.stimulus_wrong_side["grating_speed"]

        if self.stimulus_sides["right"]:
            grating = self.gen_grating(grating_frequency, grating_or, grating_size, self.settings.stimulus_end_position[0])

        if self.stimulus_sides["left"]:
            grating = self.gen_grating(grating_frequency, grating_or, grating_size, self.settings.stimulus_end_position[1])

        # on soft code of state 1 ----------------------
        event_display_stimulus.wait()
        while self.run_closed_loop_before:
            grating.setPhase(grating_ps, "+")
            grating.draw()
            self.win.flip()

        # on soft code of state 2 ----------------------
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()

        while self.run_open_loop:
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            grating.setPhase(grating_ps, "+")
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain
                # if ceil -> if very fast rotation still threshold, but stimulus not there
                pos = stream[-1][2]
                grating.pos += (change, 0)
            grating.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()

        # on soft code of state 3 freeze movement ---------
        grating.pos = self.get_stim_end_position()
        while self.run_closed_loop_after:
            grating.setPhase(grating_ps, "+")
            grating.draw()
            self.win.flip()
        self.win.flip()

        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()
