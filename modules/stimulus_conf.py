from psychopy import visual, core, monitors #import some libraries from PsychoPy
import time
import threading
import os
import sys

class Stimulus():
    def __init__(self, settings, rotary_encoder, correct_stim_side):
        """[summary]

        Args:
            settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler
            rotary_encoder (RotaryEncoder object): object handeling rotary encoder module
        """         
        self.settings = settings    
        self.trials = settings.trial_number
        self.run_open_loop = True
        self.display_stim_event = threading.Event()
        self.move_stim_event = threading.Event()
        self.still_show_event = threading.Event()
        # set gain
        self.gain =  [abs(y/x) for x in settings.thresholds[0:1] for y in settings.stim_end_pos]
        # gain to the left first - position
        self.gain_left = self.gain[0]
        # gain to the right second + position
        self.gain_right = self.gain[1]
        self.FPS = settings.FPS
        self.SCREEN_WIDTH = settings.SCREEN_WIDTH
        self.SCREEN_HEIGHT = settings.SCREEN_HEIGHT
        self.SCREEN_SIZE = (settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT)
        # stimulus    
        self.rotary_encoder = rotary_encoder
        self.correct_stim_side = correct_stim_side
        # variables
        self.closed_loop=True
        self.open_loop=True

        # TODO: nice solution
        GAIN=1 #TODO: gain from usersettings
        pos = 0
        change = 0

        """main psychopy funkction and loops"""        
        # monitor configuration
        self.monitor = monitors.Monitor('testMonitor', width=self.SCREEN_WIDTH, distance=self.SCREEN_HEIGHT)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
        self.monitor.setSizePix(self.SCREEN_SIZE)
        # create window
        #create a window
        self.win = visual.Window(
            size=(self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 
            fullscr=True, 
            screen=1, 
            monitor=self.monitor,
            winType='pyglet', allowGUI=False, allowStencil=False,
            color=[-1,-1,-1], colorSpace='rgb',
            blendMode='avg', useFBO=True, 
            units='height')
        self.win.winHandle.maximize() # fix black bar bottom
        self.win.flip()
        # get frame rate of monitor
        expInfo = {}
        expInfo['frameRate'] = self.win.getActualFrameRate()
        if expInfo['frameRate'] != None:
            frameDur = 1.0 / round(expInfo['frameRate'])
        else:
            frameDur = 1.0 / 60.0  # could not measure, so guess
        
        # flags
        self.display_stim_event = False


    # flags =========================================================================
    # flag softcode 1
    def present_stimulus(self):
        """flag bevore stimulus appears on screen, set from softcode in bpood state"""        
        #self.display_stim_event.set()
        self.display_stim_event = True
        print("present stimulus")

    # flag softcode 2
    def start_open_loop(self):
        """flag bevore open loop where wheel moves stimulus is started, set from softcode in bpod state"""        
        #self.move_stim_event.set()
        self.closed_loop = False
        print("start open loop")

    # flag softcode 3
    def stop_open_loop(self):
        """flag bevore open loop - while loop is stopped, time sleep so latent wheel movement which already triggered threshold
        can also move stimulus to final posititon
        """        
        self.run_open_loop = False
        print("stop open loop")

    # flag softcode 4
    def end_present_stimulus(self):
        """flag, which keeps stimulus frozen on end postition"""        
        self.still_show_event.set()
        print("end present stimulus")


    # helper functions ===============================================================
    def keep_on_scrren(self, position_x):
        """keep the stimulus postition in user defined boundaries

        Args:
            position_x (int): current stimulus screen positition in pixel

        Returns:
            int: updated stimulus position
        """        
        return max(min(self.stim_end_pos_right, position_x), self.stim_end_pos_left)
        

    # stimulus functions =============================================================
    def gen_grating(self, grating_sf, grating_or, pos):
        grating = visual.GratingStim(
            win=self.win,
            tex = 'sin', # texture used
            pos = (pos,0),
            units='pix',
            size=500,
            sf = grating_sf, 
            ori = grating_or,
            phase= (0.0,0.0),
            contrast = 1, # unchanged contrast (from 1 to -1)
            #units="deg",
            #pos = (0.0, 0.0), #in the middle of the screen. It is convertes internally in a numpy array
            #sf = 5.0 / 200.0, # set the spatial frequency 5 cycles/ 150 pixels. 
            #mask='raisedCos',
            mask = 'raisedCos'
        )
        return grating

    def gen_stim(self):
        circle = visual.Circle(
            win=self.win,
            name='cicle',
            radius=100, #self.settings.stimulus_rad,
            units='pix',
            edges=128,
            #units='pix',
            fillColor= (0,255,0), #self.settings.stimulus_col,
            pos=(0,0),
            )
        return circle

    # Main psychpy loop ==============================================================
    def run_game(self):
        # get right grating
        if self.correct_stim_side["right"]:
            right_sf = self.settings.stimulus_correct["grating_sf"]
            right_or = self.settings.stimulus_correct["grating_ori"]
            left_sf = self.settings.stimulus_wrong["grating_sf"]
            left_or = self.settings.stimulus_wrong["grating_ori"]
        elif self.correct_stim_side["left"]:
            left_sf = self.settings.stimulus_correct["grating_sf"]
            left_or = self.settings.stimulus_correct["grating_ori"]
            right_sf = self.settings.stimulus_wrong["grating_sf"]
            right_or = self.settings.stimulus_wrong["grating_ori"]
        # generate gratings and stimuli
        grating_left = self.gen_grating(left_sf,left_or,-900)#left_sf,left_or,self.settings.stim_end_pos[0] ,win)
        grating_right = self.gen_grating(right_sf,right_or,900) #right_sf,right_or,self.settings.stim_end_pos[1] ,win)
        stim = self.gen_stim()
        #-----------------------------------------------------------------------------
        # on soft code of state 1
        #-----------------------------------------------------------------------------
        # present initial stimulus
        #while self.display_stim_event:
        #    pass
        print("closed loop")
        sys.stdout.flush()
        while self.closed_loop: 
            # dram moving gratings
            grating_left.setPhase(0.02, '+')#advance phase by 0.05 of a cycle
            grating_right.setPhase(0.02, '+')
            grating_left.draw()
            grating_right.draw()
            stim.draw()
            self.win.flip()
        #-------------------------------------------------------------------------
        # on soft code of state 2
        #-------------------------------------------------------------------------
        # reset rotary encoder
        self.rotary_encoder.rotary_encoder.set_zero_position()
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        print("open loop")
        sys.stdout.flush()
        while True: #self.open_loop:
            # dram moving gratings
            grating_left.setPhase(0.02, '+')#advance phase by 0.05 of a cycle
            grating_right.setPhase(0.02, '+')
            grating_left.draw()
            grating_right.draw()
            # get rotary encoder change position
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            if len(stream)>0:
                change = pos - stream[-1][2]
                pos = stream[-1][2]
                #move stimulus with mouse
                stim.pos+=(change*GAIN,0)    
            stim.draw()
            self.win.flip()
            sys.stdout.flush()
        #-------------------------------------------------------------------------
        # on soft code of state 3 freez movement
        #-------------------------------------------------------------------------
        self.still_show_event.wait()
        self.win.flip()
        self.win.clear()
        # cleanup
        self.open_loop = True
        self.closed_loop = True
        # reset flags
        self.display_stim_event.clear()
        self.still_show_event.clear()


