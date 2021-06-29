
from psychopy import visual, core, monitors  # import some libraries from PsychoPy
from math import tan as tan
import random


class Stimulus():
    def __init__(self, settings, rotary_encoder):
        """[summary]

        Args:
            settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler
            rotary_encoder (RotaryEncoder object): object handeling rotary encoder module
        """
        self.settings = settings

        # set gain
        self.FPS = settings.FPS
        self.mon_width = settings.MON_WIDTH
        self.mon_dist = settings.MON_DIST
        self.screen_size = (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)  # (1024,1280)#
        # stimulus
        self.rotary_encoder = rotary_encoder
        #self.gain = self.get_gain()
        self.gain_left, self.gain_right = [round(abs(y/x), 2) for x in settings.thresholds[0:1] for y in settings.stim_end_pos]
        self.gain = self.gain_left
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

    def get_gratings_size(self, grating_size):
        """calculate gratin size in pixel based on visual angle
        """
        x = self.mon_dist*tan(grating_size/2)  # half width of stim in size
        return (x/self.mon_width)*self.screen_size[0]

    """
    def get_gain(self):
        clicks = 1024/365 * abs(self.settings.thresholds[0]) #each full rotation = 1024 clicks
        gain = abs(self.settings.stim_end_pos[0]) / clicks
        return round(gain,2)
    """

    def ceil(self, num):
        if num > 30:
            return 30
        else:
            return num

    def close(self):
        self.win.close()
        core.quit()

    def stop_open_loop(self):
        self.run_open_loop = False

    # stimulus functions =============================================================
    def gen_stim(self):
        circle = visual.Circle(
            win=self.win,
            name='cicle',
            radius=self.settings.stimulus_rad,
            units='pix',
            edges=128,
            fillColor=self.settings.stimulus_col,
            pos=(0, 0),
        )
        return circle

    # Main psychpy loop ==============================================================
    def run_game(self, display_stim_event, start_open_loop_event, still_show_event, bpod, sma):
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
        start_open_loop_event.wait()
        # reset rotary encoder
        # self.rotary_encoder.rotary_encoder.set_zero_position()
        # self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        print("open loop")
        pos = 0
        stream = self.rotary_encoder.rotary_encoder.read_stream()
        # self.rotary_encoder.rotary_encoder.set_zero_position()
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
        # -------------------------------------------------------------------------
        # on soft code of state 3 freez movement
        # -------------------------------------------------------------------------
        still_show_event.wait()
        print("end")
        self.win.flip()
        # cleanup for next loop
        self.run_closed_loop = True
        self.run_open_loop = True
        display_stim_event.clear()
        start_open_loop_event.clear()
        still_show_event.clear()
