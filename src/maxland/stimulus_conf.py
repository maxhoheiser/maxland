import random
import time
from threading import Event
from typing import Dict

from psychopy import core, monitors, tools, visual

from maxland.parameter_handler import TrialParameterHandler
from maxland.rotaryencoder import BpodRotaryEncoder


class Stimulus:
    """
    Create the stimulus via pygame and pyglet with psychopy
    Args:
        settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler
        rotary_encoder (RotaryEncoder object): object handeling rotary encoder module
    """

    def __init__(self, settings: TrialParameterHandler, rotary_encoder: BpodRotaryEncoder, correct_stimulus_side: str):
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
        self.correct_stimulus_side = correct_stimulus_side

        self.gain_left = self.get_gain(settings.rotaryencoder_thresholds[0], settings.rotaryencoder_stimulus_end_position[0])
        self.gain_right = self.get_gain(settings.rotaryencoder_thresholds[1], settings.rotaryencoder_stimulus_end_position[1])
        self.gain = self.gain_left

        self.monitor = monitors.Monitor("testMonitor", width=self.monitor_width, distance=self.monitor_distance)
        self.monitor.setSizePix(self.screen_size)

        self.win = visual.Window(
            size=(self.screen_size),
            fullscr=False,
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

    def get_gain(self, threshold, rotaryencoder_stimulus_end_position):
        gain = abs(rotaryencoder_stimulus_end_position / threshold)
        return round(gain, 2)

    def ceil(self, num):
        if num > 10:
            return 10
        else:
            return num

    def on_close(self):
        self.win.close()
        core.quit()

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

    # Main psychpy loop
    EventFlags = Dict[str, Event]

    # Stimulus Type 3 (main) = fixed gratings + moving circle ==========================
    def run_game_3(self, event_flags: EventFlags):
        event_display_stimulus = event_flags["event_display_stimulus"]
        event_still_show_stimulus = event_flags["event_still_show_stimulus"]

        event_display_stimulus.clear()
        event_still_show_stimulus.clear()
        self.reset_loop_flags()

        if self.correct_stimulus_side == "right":
            right_sf = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_sf"])
            right_or = self.settings.stimulus_correct_side["grating_ori"]
            right_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
            right_ps = self.settings.stimulus_correct_side["grating_speed"]
            left_sf = self.get_grating_frequency(self.settings.stimulus_wrong_side["grating_sf"])
            left_or = self.settings.stimulus_wrong_side["grating_ori"]
            left_size = self.get_grating_size(self.settings.stimulus_wrong_side["grating_size"])
            left_ps = self.settings.stimulus_correct_side["grating_speed"]

        if self.correct_stimulus_side == "left":
            left_sf = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_sf"])
            left_or = self.settings.stimulus_correct_side["grating_ori"]
            left_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
            left_ps = self.settings.stimulus_correct_side["grating_speed"]
            right_sf = self.get_grating_frequency(self.settings.stimulus_wrong_side["grating_sf"])
            right_or = self.settings.stimulus_wrong_side["grating_ori"]
            right_size = self.get_grating_size(self.settings.stimulus_wrong_side["grating_size"])
            right_ps = self.settings.stimulus_correct_side["grating_speed"]

        grating_left = self.gen_grating(left_sf, left_or, left_size, self.settings.rotaryencoder_stimulus_end_position[0])
        grating_right = self.gen_grating(right_sf, right_or, right_size, self.settings.rotaryencoder_stimulus_end_position[1])
        stim = self.gen_stimulus()

        # on soft code of state 1 ----------------------
        event_display_stimulus.wait()
        while self.run_closed_loop_before:
            print(self.run_closed_loop_before)
            grating_left.setPhase(left_ps, "+")
            grating_right.setPhase(right_ps, "+")
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
            grating_left.setPhase(left_ps, "+")  # advance phase by 0.05 of a cycle
            grating_right.setPhase(right_ps, "+")
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

        # on soft code of state 3 freez movement ---------
        event_still_show_stimulus.wait()
        self.win.flip()

        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()
        event_still_show_stimulus.clear()

    # Stimulus Type 2 = moving gratings ================================================
    def run_game_2(self, event_flags: EventFlags):
        event_display_stimulus = event_flags["event_display_stimulus"]
        event_still_show_stimulus = event_flags["event_still_show_stimulus"]

        event_display_stimulus.clear()
        event_still_show_stimulus.clear()
        self.reset_loop_flags()

        if self.correct_stimulus_side == "left":  # switch side because stim is moved to center not ball moved to stim
            right_sf = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_sf"])
            right_or = self.settings.stimulus_correct_side["grating_ori"]
            right_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
            right_ps = self.settings.stimulus_correct_side["grating_speed"]
            left_sf = self.get_grating_frequency(self.settings.stimulus_wrong_side["grating_sf"])
            left_or = self.settings.stimulus_wrong_side["grating_ori"]
            left_size = self.get_grating_size(self.settings.stimulus_wrong_side["grating_size"])
            left_ps = self.settings.stimulus_correct_side["grating_speed"]

        if self.correct_stimulus_side == "right":  # switch side because stim is moved to center not ball moved to stim
            left_sf = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_sf"])
            left_or = self.settings.stimulus_correct_side["grating_ori"]
            left_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
            left_ps = self.settings.stimulus_correct_side["grating_speed"]
            right_sf = self.get_grating_frequency(self.settings.stimulus_wrong_side["grating_sf"])
            right_or = self.settings.stimulus_wrong_side["grating_ori"]
            right_size = self.get_grating_size(self.settings.stimulus_wrong_side["grating_size"])
            right_ps = self.settings.stimulus_correct_side["grating_speed"]

        grating_left = self.gen_grating(left_sf, left_or, left_size, self.settings.rotaryencoder_stimulus_end_position[0])
        grating_right = self.gen_grating(right_sf, right_or, right_size, self.settings.rotaryencoder_stimulus_end_position[1])

        # on soft code of state 1 ----------------------
        event_display_stimulus.wait()
        while self.run_closed_loop_before:
            grating_left.setPhase(left_ps, "+")
            grating_right.setPhase(right_ps, "+")
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
            grating_left.setPhase(left_ps, "+")  # advance phase by 0.05 of a cycle
            grating_right.setPhase(right_ps, "+")
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
        event_still_show_stimulus.wait()
        self.win.flip()

        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()

    # Stimulus Type 1 = single moving grating ==========================================
    def run_game_1(self, event_display_stimulus, event_still_show_stimulus):
        # get random stimulus always set the right stimulus as correct
        if self.correct_stimulus_side == "right":
            stimulus = self.settings.stimulus_correct_side
        elif self.correct_stimulus_side == "left":
            stimulus = self.settings.stimulus_wrong_side
        stim_sf = self.get_grating_frequency(stimulus["grating_sf"])
        stim_or = stimulus["grating_ori"]
        stim_size = self.get_grating_size(stimulus["grating_size"])
        stim_ps = stimulus["grating_speed"]
        # generate gratings and stimuli
        grating = self.gen_grating(stim_sf, stim_or, stim_size, 0)  # self.settings.rotaryencoder_stimulus_end_position[0])
        # on soft code of state 1
        # present initial stimulus
        event_display_stimulus.wait()
        while self.run_closed_loop_before:  # self.run_closed_loop_before:
            # dram moving gratings
            grating.setPhase(stim_ps, "+")  # advance phase by 0.05 of a cycle
            grating.draw()
            self.win.flip()
        # on soft code of state 2
        # reset rotary encoder
        # open loop
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()
        while self.run_open_loop:
            # get rotary encoder change position
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            # dram moving gratings
            grating.setPhase(stim_ps, "+")  # advance phase by 0.05 of a cycle
            grating.draw()
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain  # self.ceil((pos - stream[-1][2])*self.gain)
                # if ceil -> if very fast rotation still threshold, but stimulus not there
                pos = stream[-1][2]
                # move stimulus with mouse
                grating.pos += (change, 0)
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()
        # on soft code of state 3 freez movement
        event_still_show_stimulus.wait()
        self.win.flip()
        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()
        event_still_show_stimulus.clear()

    # Habituation  Type 3 online center stim psychopy Loop =============================
    def run_game_habituation_3_simple(self, event_display_stimulus, event_still_show_stimulus):
        # get right grating
        stim = self.gen_stimulus()
        stim.draw()
        # on soft code of state 1
        # present initial stimulus
        event_display_stimulus.wait()
        self.win.flip()
        # on soft code of state 2
        # reset rotary encoder
        # open loop
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()
        while self.run_open_loop:
            # get rotary encoder change position
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain  # self.ceil((pos - stream[-1][2])*self.gain)
                # if ceil -> if very fast rotation still threshold, but stimulus not there
                pos = stream[-1][2]
                # move stimulus with mouse
                stim.pos += (change, 0)
            stim.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()
        # on soft code of state 3 freez movement
        event_still_show_stimulus.wait()
        self.win.flip()
        self.reset_loop_flags()
        event_display_stimulus.clear()
        event_still_show_stimulus.clear()

    # Habituation Typ 3 only single correct grating ====================================
    def run_game_habituation_3_complex(self, event_display_stimulus, event_still_show_stimulus):
        # get right grating
        grating_sf = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_sf"])
        grating_or = self.settings.stimulus_correct_side["grating_ori"]
        grating_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
        grating_ps = self.settings.stimulus_correct_side["grating_speed"]

        if self.correct_stimulus_side == "right":
            grating = self.gen_grating(grating_sf, grating_or, grating_size, self.settings.rotaryencoder_stimulus_end_position[1])
        elif self.correct_stimulus_side == "left":
            grating = self.gen_grating(grating_sf, grating_or, grating_size, self.settings.rotaryencoder_stimulus_end_position[0])
        # generate gratings and stimuli
        stim = self.gen_stimulus()
        stim.draw()  # TODO: bugfix but now always all three stims are shown immediately
        # on soft code of state 1
        # present initial stimulus
        event_display_stimulus.wait()
        while self.run_closed_loop_before:  # self.run_closed_loop_before:
            # dram moving gratings
            grating.setPhase(grating_ps, "+")  # advance phase by 0.05 of a cycle
            grating.draw()
            # stim.draw()
            self.win.flip()
        # on soft code of state 2
        # reset rotary encoder
        # open loop
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()
        while self.run_open_loop:
            # get rotary encoder change position
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            # dram moving gratings
            grating.setPhase(grating_ps, "+")  # advance phase by 0.05 of a cycle
            grating.draw()
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain  # self.ceil((pos - stream[-1][2])*self.gain)
                # if ceil -> if very fast rotation still threshold, but stimulus not there
                pos = stream[-1][2]
                # move stimulus with mouse
                stim.pos += (change, 0)
            stim.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()
        # on soft code of state 3 freez movement
        event_still_show_stimulus.wait()
        self.win.flip()
        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()
        event_still_show_stimulus.clear()

    # Habituation Typ 2 complex ========================================================
    def run_game_habituation_2_complex(self, event_display_stimulus, event_still_show_stimulus):
        # randomly get left or right grating
        random_grating = bool(random.getrandbits(1))
        if random_grating:
            # get correct grating
            grating_sf = self.get_grating_frequency(self.settings.stimulus_correct_side["grating_sf"])
            grating_or = self.settings.stimulus_correct_side["grating_ori"]
            grating_size = self.get_grating_size(self.settings.stimulus_correct_side["grating_size"])
            grating_ps = self.settings.stimulus_correct_side["grating_speed"]
        else:
            # get wrong grating
            grating_sf = self.get_grating_frequency(self.settings.stimulus_wrong_side["grating_sf"])
            grating_or = self.settings.stimulus_wrong_side["grating_ori"]
            grating_size = self.get_grating_size(self.settings.stimulus_wrong_side["grating_size"])
            grating_ps = self.settings.stimulus_wrong_side["grating_speed"]

        if self.correct_stimulus_side == "right":
            grating = self.gen_grating(grating_sf, grating_or, grating_size, self.settings.rotaryencoder_stimulus_end_position[0])
        elif self.correct_stimulus_side == "left":
            grating = self.gen_grating(grating_sf, grating_or, grating_size, self.settings.rotaryencoder_stimulus_end_position[1])
        # on soft code of state 1
        # present initial stimulus
        event_display_stimulus.wait()
        while self.run_closed_loop_before:  # self.run_closed_loop_before:
            # dram moving gratings
            grating.setPhase(grating_ps, "+")  # advance phase by 0.05 of a cycle
            grating.draw()
            self.win.flip()
        # on soft code of state 2
        # reset rotary encoder
        # open loop
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()
        while self.run_open_loop:
            # get rotary encoder change position
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            # dram moving gratings
            grating.setPhase(grating_ps, "+")  # advance phase by 0.05 of a cycle
            if len(stream) > 0:
                change = (pos - stream[-1][2]) * self.gain  # self.ceil((pos - stream[-1][2])*self.gain)
                # if ceil -> if very fast rotation still threshold, but stimulus not there
                pos = stream[-1][2]
                # move stimulus with mouse
                grating.pos += (change, 0)
            grating.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()
        # on soft code of state 3 freez movement
        # event_still_show_stimulus.wait()
        self.win.flip()
        # cleanup for next loop
        self.reset_loop_flags()
        event_display_stimulus.clear()
        event_still_show_stimulus.clear()
