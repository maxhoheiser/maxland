from psychopy import visual, core, monitors, tools  # import some libraries from PsychoPy
from math import tan as tan
import random
import time


class Stimulus():
    def __init__(self, settings, rotary_encoder, correct_stim_side):
        """[summary]

        Args:
            settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler
            rotary_encoder (RotaryEncoder object): object handeling rotary encoder module
        """
        self.settings = settings
        self.trials = settings.trial_number

        # set gain
        self.FPS = settings.FPS
        self.mon_width = settings.MON_WIDTH
        self.mon_dist = settings.MON_DIST
        self.screen_size = (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)  # (1024,1280)#
        # stimulus
        self.rotary_encoder = rotary_encoder
        self.correct_stim_side = correct_stim_side
        #self.gain = self.get_gain()
        self.gain_left, self.gain_right = [round(abs(y/x), 2) for x in settings.thresholds[0:1] for y in settings.stim_end_pos]
        self.gain = self.gain_left #TODO:
        # monitor configuration
        # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
        self.monitor = monitors.Monitor('testMonitor', width=self.mon_width, distance=self.mon_dist)
        self.monitor.setSizePix(self.screen_size)
        # create window
        # create a window
        self.win = visual.Window(
            size=(self.screen_size),
            fullscr=True,
            screen=1,
            monitor=self.monitor,
            units="pix",
            winType='pyglet', allowGUI=False, allowStencil=False,
            color=self.settings.bg_color, colorSpace='rgb',
            blendMode='avg', useFBO=True,
        )
        self.win.winHandle.maximize()  # fix black bar bottom
        self.win.flip()
        # get frame rate of monitor
        expInfo = {}
        expInfo['frameRate'] = self.win.getActualFrameRate()
        if expInfo['frameRate'] != None:
            frameDur = 1.0 / round(expInfo['frameRate'])
        else:
            frameDur = 1.0 / 60.0  # could not measure, so guess

        self.run_closed_loop = True
        self.run_open_loop = True

    # helper functions ===============================================================
    def keep_on_scrren(self, position_x):
        """keep the stimulus postition in user defined boundaries

        Args:
            position_x (int): current stimulus screen positition in pixel

        Returns:
            int: updated stimulus position
        """
        return max(min(self.stim_end_pos_right, position_x), self.stim_end_pos_left)

    def get_grating_size(self, deg):
        """calculate gratin size in pixel based on visual angle
        """
        return tools.monitorunittools.deg2pix(deg,self.monitor)
    
    def get_grating_sf(self, sf):
        """calculate spatial frequency given in visual angle in pixel
        """
        return sf #tools.monitorunittools.pix2deg(sf,self.monitor)

    def get_gain(self):
        clicks = 1024/365 * abs(self.settings.thresholds[0])  # each full rotation = 1024 clicks
        gain = abs(self.settings.stim_end_pos[0]) / clicks
        return round(gain, 2)

    def ceil(self, num):
        if num > 10:
            return 10
        else:
            return num

    def close(self):
        self.win.close()
        core.quit()

    def stop_closed_loop(self):
        self.run_closed_loop = False

    def stop_open_loop(self):
        self.run_open_loop = False

    # stimulus functions =============================================================
    def gen_grating(self, grating_sf, grating_or, grating_size, pos):
        grating = visual.GratingStim(
            win=self.win,
            tex='sin',  # texture used
            pos=(pos, 0),
            units="pix",  # "deg",#'deg', # size in degrees for correct stim size
            size=grating_size,
            sf=grating_sf,
            ori=grating_or,
            contrast=1,  # unchanged contrast (from 1 to -1)
            mask='raisedCos'
        )
        return grating

    def gen_stim(self):
        circle = visual.Circle(
            win=self.win,
            name='cicle',
            radius=self.get_grating_size(self.settings.stimulus_rad)/2, # convet from vis angle to pixel and fomr diameter to radius
            units='pix',
            edges=128,
            fillColor=self.settings.stimulus_col,
            pos=(0, 0),
        )
        return circle

    # Main psychpy loop ==============================================================
    # Stimulus Type 3 (main) = fixed gratings + moving circle
    def run_game_3(self, display_stim_event, still_show_event, bpod, sma):
        display_stim_event.clear()
        still_show_event.clear()
        self.run_closed_loop = True
        self.run_open_loop = True
        # get right grating
        if self.correct_stim_side["right"]:
            right_sf = self.get_grating_sf(self.settings.stimulus_correct["grating_sf"])
            right_or = self.settings.stimulus_correct["grating_ori"]
            right_size = self.get_grating_size(self.settings.stimulus_correct["grating_size"])
            right_ps = self.settings.stimulus_correct["grating_speed"]
            left_sf = self.get_grating_sf(self.settings.stimulus_wrong["grating_sf"])
            left_or = self.settings.stimulus_wrong["grating_ori"]
            left_size = self.get_grating_size(self.settings.stimulus_wrong["grating_size"])
            left_ps = self.settings.stimulus_correct["grating_speed"]
        elif self.correct_stim_side["left"]:
            left_sf = self.get_grating_sf(self.settings.stimulus_correct["grating_sf"])
            left_or = self.settings.stimulus_correct["grating_ori"]
            left_size = self.get_grating_size(self.settings.stimulus_correct["grating_size"])
            left_ps = self.settings.stimulus_correct["grating_speed"]
            right_sf = self.get_grating_sf(self.settings.stimulus_wrong["grating_sf"])
            right_or = self.settings.stimulus_wrong["grating_ori"]
            right_size = self.get_grating_size(self.settings.stimulus_wrong["grating_size"])
            right_ps = self.settings.stimulus_correct["grating_speed"]
        # generate gratings and stimuli
        grating_left = self.gen_grating(left_sf, left_or, left_size, self.settings.stim_end_pos[0])
        grating_right = self.gen_grating(right_sf, right_or, right_size, self.settings.stim_end_pos[1])
        stim = self.gen_stim()
        # -----------------------------------------------------------------------------
        # on soft code of state 1
        # -----------------------------------------------------------------------------
        # present initial stimulus
        display_stim_event.wait()
        while self.run_closed_loop:  # self.run_closed_loop:
            # dram moving gratings
            grating_left.setPhase(left_ps, '+')  # advance phase by 0.05 of a cycle
            grating_right.setPhase(right_ps, '+')
            grating_left.draw()
            grating_right.draw()
            stim.draw()
            self.win.flip()
        # -------------------------------------------------------------------------
        # on soft code of state 2
        # -------------------------------------------------------------------------
        # reset rotary encoder
        # open loop
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()
        #stim.draw
        #self.win.flip()
        time.sleep(0.01)
        while self.run_open_loop:
            # dram moving gratings
            # get rotary encoder change position
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            grating_left.setPhase(left_ps, '+')  # advance phase by 0.05 of a cycle
            grating_right.setPhase(right_ps, '+')
            grating_left.draw()
            grating_right.draw()
            if len(stream) > 0:
                change  = (pos - stream[-1][2])*self.gain  # self.ceil((pos - stream[-1][2])*self.gain) # if ceil -> if very fast rotation still threshold, but stimulus not therer
                pos = stream[-1][2]
                # move stimulus with mouse
                stim.pos += (change, 0)
            stim.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()
        # -------------------------------------------------------------------------
        # on soft code of state 3 freez movement
        # -------------------------------------------------------------------------
        still_show_event.wait()
        self.win.flip()
        # cleanup for next loop
        self.run_closed_loop = True
        self.run_open_loop = True
        display_stim_event.clear()
        still_show_event.clear()

    # Stimulus Type 2 = moving gratings ===============================================

    def run_game_2(self, display_stim_event, still_show_event, bpod, sma):
        # get right grating
        if self.correct_stim_side["left"]:  # switch side because stim is moved to center not ball moved to stim
            right_sf = self.get_grating_sf(self.settings.stimulus_correct["grating_sf"])
            right_or = self.settings.stimulus_correct["grating_ori"]
            right_size = self.get_grating_size(self.settings.stimulus_correct["grating_size"])
            right_ps = self.settings.stimulus_correct["grating_speed"]
            left_sf = self.get_grating_sf(self.settings.stimulus_wrong["grating_sf"])
            left_or = self.settings.stimulus_wrong["grating_ori"]
            left_size = self.get_grating_size(self.settings.stimulus_wrong["grating_size"])
            left_ps = self.settings.stimulus_correct["grating_speed"]
        elif self.correct_stim_side["right"]:  # switch side because stim is moved to center not ball moved to stim
            left_sf = self.get_grating_sf(self.settings.stimulus_correct["grating_sf"])
            left_or = self.settings.stimulus_correct["grating_ori"]
            left_size = self.get_grating_size(self.settings.stimulus_correct["grating_size"])
            left_ps = self.settings.stimulus_correct["grating_speed"]
            right_sf = self.get_grating_sf(self.settings.stimulus_wrong["grating_sf"])
            right_or = self.settings.stimulus_wrong["grating_ori"]
            right_size = self.get_grating_size(self.settings.stimulus_wrong["grating_size"])
            right_ps = self.settings.stimulus_correct["grating_speed"]
        # generate gratings and stimuli
        grating_left = self.gen_grating(left_sf, left_or, left_size, self.settings.stim_end_pos[0])
        grating_right = self.gen_grating(right_sf, right_or, right_size, self.settings.stim_end_pos[1])
        # -----------------------------------------------------------------------------
        # on soft code of state 1
        # -----------------------------------------------------------------------------
        # present initial stimulus
        display_stim_event.wait()
        while self.run_closed_loop:  # self.run_closed_loop:
            # dram moving gratings
            grating_left.setPhase(left_ps, '+')  # advance phase by 0.05 of a cycle
            grating_right.setPhase(right_ps, '+')
            grating_left.draw()
            grating_right.draw()
            self.win.flip()
        # -------------------------------------------------------------------------
        # on soft code of state 2
        # -------------------------------------------------------------------------
        # reset rotary encoder
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        self.rotary_encoder.rotary_encoder.set_zero_position()
        while self.run_open_loop:
            # get rotary encoder change position
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            # dram moving gratings
            grating_left.setPhase(left_ps, '+')  # advance phase by 0.05 of a cycle
            grating_right.setPhase(right_ps, '+')
            if len(stream) > 0:
                change = (pos - stream[-1][2])*self.gain  # self.ceil((pos - stream[-1][2])*self.gain) # if ceil -> if very fast rotation still threshold, but stimulus not therer
                pos = stream[-1][2]
                # move stimulus with mouse
                grating_left.pos += (change, 0)
                grating_right.pos += (change, 0)
            grating_left.draw()
            grating_right.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()
        # -------------------------------------------------------------------------
        # on soft code of state 3 freez movement
        # -------------------------------------------------------------------------
        still_show_event.wait()
        self.win.flip()
        # cleanup for next loop
        self.run_closed_loop = True
        self.run_open_loop = True
        display_stim_event.clear()
        still_show_event.clear()

    # Stimulus Type 1 = single moving grating ==========================================
    def run_game_1(self, display_stim_event, still_show_event, bpod, sma):
        # get random stimulus always set the right stimulus as correct
        if self.correct_stim_side["right"]:
            stimulus = self.settings.stimulus_correct
        elif self.correct_stim_side["left"]:
            stimulus = self.settings.stimulus_wrong
        stim_sf = self.get_grating_sf(stimulus["grating_sf"])
        stim_or = stimulus["grating_ori"]
        stim_size = self.get_grating_size(stimulus["grating_size"])
        stim_ps = stimulus["grating_speed"]
        # generate gratings and stimuli
        grating = self.gen_grating(stim_sf, stim_or, stim_size, 0)  # self.settings.stim_end_pos[0])
        # -----------------------------------------------------------------------------
        # on soft code of state 1
        # -----------------------------------------------------------------------------
        # present initial stimulus
        display_stim_event.wait()
        while self.run_closed_loop:  # self.run_closed_loop:
            # dram moving gratings
            grating.setPhase(stim_ps, '+')  # advance phase by 0.05 of a cycle
            grating.draw()
            self.win.flip()
        # -------------------------------------------------------------------------
        # on soft code of state 2
        # -------------------------------------------------------------------------
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
            grating.setPhase(stim_ps, '+')  # advance phase by 0.05 of a cycle
            grating.draw()
            if len(stream) > 0:
                change = (pos - stream[-1][2])*self.gain  # self.ceil((pos - stream[-1][2])*self.gain) # if ceil -> if very fast rotation still threshold, but stimulus not therer
                pos = stream[-1][2]
                # move stimulus with mouse
                grating.pos += (change, 0)
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()
        # -------------------------------------------------------------------------
        # on soft code of state 3 freez movement
        # -------------------------------------------------------------------------
        still_show_event.wait()
        self.win.flip()
        # cleanup for next loop
        self.run_closed_loop = True
        self.run_open_loop = True
        display_stim_event.clear()
        still_show_event.clear()

    # HABITUATION ######################################################################

    # Habituation  Type 3 online center stim psychopy Loop =============================

    def run_game_habituation_3_simple(self, display_stim_event, still_show_event, bpod, sma):
        # get right grating
        stim = self.gen_stim()
        stim.draw()
        # -----------------------------------------------------------------------------
        # on soft code of state 1
        # -----------------------------------------------------------------------------
        # present initial stimulus
        display_stim_event.wait()
        self.win.flip()
        # -------------------------------------------------------------------------
        # on soft code of state 2
        # -------------------------------------------------------------------------
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
                change = (pos - stream[-1][2])*self.gain  # self.ceil((pos - stream[-1][2])*self.gain) # if ceil -> if very fast rotation still threshold, but stimulus not therer
                pos = stream[-1][2]
                # move stimulus with mouse
                stim.pos += (change, 0)
            stim.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()
        # -------------------------------------------------------------------------
        # on soft code of state 3 freez movement
        # -------------------------------------------------------------------------
        still_show_event.wait()
        self.win.flip()
        # cleanup for next loop
        self.run_closed_loop = True
        self.run_open_loop = True
        display_stim_event.clear()
        still_show_event.clear()

    # Habituation Typ 3 only single correct grating ====================================
    def run_game_habituation_3_complex(self, display_stim_event, still_show_event, bpod, sma):
        # get right grating
        grating_sf = self.get_grating_sf(self.settings.stimulus_correct["grating_sf"])
        grating_or = self.settings.stimulus_correct["grating_ori"]
        grating_size = self.get_grating_size(self.settings.stimulus_correct["grating_size"])
        grating_ps = self.settings.stimulus_correct["grating_speed"]

        if self.correct_stim_side["right"]:
            grating = self.gen_grating(grating_sf, grating_or, grating_size, self.settings.stim_end_pos[1])
        elif self.correct_stim_side["left"]:
            grating = self.gen_grating(grating_sf, grating_or, grating_size, self.settings.stim_end_pos[0])
        # generate gratings and stimuli
        stim = self.gen_stim()
        # -----------------------------------------------------------------------------
        # on soft code of state 1
        # -----------------------------------------------------------------------------
        # present initial stimulus
        display_stim_event.wait()
        while self.run_closed_loop:  # self.run_closed_loop:
            # dram moving gratings
            grating.setPhase(grating_ps, '+')  # advance phase by 0.05 of a cycle
            grating.draw()
            # stim.draw()
            self.win.flip()
        # -------------------------------------------------------------------------
        # on soft code of state 2
        # -------------------------------------------------------------------------
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
            grating.setPhase(grating_ps, '+')  # advance phase by 0.05 of a cycle
            grating.draw()
            if len(stream) > 0:
                change = (pos - stream[-1][2])*self.gain  # self.ceil((pos - stream[-1][2])*self.gain) # if ceil -> if very fast rotation still threshold, but stimulus not therer
                pos = stream[-1][2]
                # move stimulus with mouse
                stim.pos += (change, 0)
            stim.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()
        # -------------------------------------------------------------------------
        # on soft code of state 3 freez movement
        # -------------------------------------------------------------------------
        still_show_event.wait()
        self.win.flip()
        # cleanup for next loop
        self.run_closed_loop = True
        self.run_open_loop = True
        display_stim_event.clear()
        still_show_event.clear()

    # Habituation Typ 2 complex =======================================================
    def run_game_habituation_2_complex(self, display_stim_event, still_show_event, bpod, sma):
        # get right grating
        grating_sf = self.get_grating_sf(self.settings.stimulus_correct["grating_sf"])
        grating_or = self.settings.stimulus_correct["grating_ori"]
        grating_size = self.get_grating_size(self.settings.stimulus_correct["grating_size"])
        grating_ps = self.settings.stimulus_correct["grating_speed"]

        if self.correct_stim_side["right"]:
            grating = self.gen_grating(grating_sf, grating_or, grating_size, self.settings.stim_end_pos[0])
        elif self.correct_stim_side["left"]:
            grating = self.gen_grating(grating_sf, grating_or, grating_size, self.settings.stim_end_pos[1])
        # -----------------------------------------------------------------------------
        # on soft code of state 1
        # -----------------------------------------------------------------------------
        # present initial stimulus
        display_stim_event.wait()
        while self.run_closed_loop:  # self.run_closed_loop:
            # dram moving gratings
            grating.setPhase(grating_ps, '+')  # advance phase by 0.05 of a cycle
            grating.draw()
            self.win.flip()
        # -------------------------------------------------------------------------
        # on soft code of state 2
        # -------------------------------------------------------------------------
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
            grating.setPhase(grating_ps, '+')  # advance phase by 0.05 of a cycle
            if len(stream) > 0:
                change = (pos - stream[-1][2])*self.gain  # self.ceil((pos - stream[-1][2])*self.gain) # if ceil -> if very fast rotation still threshold, but stimulus not therer
                pos = stream[-1][2]
                # move stimulus with mouse
                grating.pos += (change, 0)
            grating.draw()
            self.win.flip()
        self.rotary_encoder.rotary_encoder.disable_stream()
        # -------------------------------------------------------------------------
        # on soft code of state 3 freez movement
        # -------------------------------------------------------------------------
        still_show_event.wait()
        self.win.flip()
        # cleanup for next loop
        self.run_closed_loop = True
        self.run_open_loop = True
        display_stim_event.clear()
        still_show_event.clear()
