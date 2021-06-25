
from psychopy import visual, core, monitors #import some libraries from PsychoPy
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
        self.screen_size = (settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT) #(1024,1280)#
        # stimulus    
        self.rotary_encoder = rotary_encoder
        #self.gain = self.get_gain()
        self.gain_left,self.gain_right  =  [round(abs(y/x),2) for x in settings.thresholds[0:1] for y in settings.stim_end_pos]
        self.gain = self.gain_left
        # monitor configuration
        self.monitor = monitors.Monitor('testMonitor', width=self.mon_width, distance=self.mon_dist)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
        self.monitor.setSizePix(self.screen_size)
        # create window
        #create a window
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
        self.win.winHandle.maximize() # fix black bar bottom
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
        
    def get_gratings_size(self,grating_size):
        """calculate gratin size in pixel based on visual angle
        """
        x = self.mon_dist*tan(grating_size/2)#half width of stim in size 
        return (x/self.mon_width)*self.screen_size[0]

    def get_gain(self):
        clicks = 1024/365 * abs(self.settings.thresholds[0]) #each full rotation = 1024 clicks
        gain = abs(self.settings.stim_end_pos[0]) / clicks
        return round(gain,2)

    def ceil(self,num):
        if num > 20:
            return 20
        else:
            return num
    
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
            fillColor= self.settings.stimulus_col,
            pos=(0,0),
            )
        return circle

    # Main psychpy loop ==============================================================
    def run_game(self, display_stim_event, start_open_loop_event, still_show_event):
        # get right grating
        stim = self.gen_stim()
        stim.draw()
        #-----------------------------------------------------------------------------
        # on soft code of state 1
        #-----------------------------------------------------------------------------
        # present initial stimulus
        display_stim_event.wait()
        self.win.flip()
        #-------------------------------------------------------------------------
        # on soft code of state 2
        #-------------------------------------------------------------------------
        # reset rotary encoder
        self.rotary_encoder.rotary_encoder.set_zero_position()
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        print("open loop")
        pos=0
        start_open_loop_event.wait()
        while self.run_open_loop:
            # get rotary encoder change position
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            if len(stream)>0:
                change = (pos - stream[-1][2])*self.gain #self.ceil((pos - stream[-1][2])*self.gain) # if ceil -> if very fast rotation still threshold, but stimulus not therer
                pos = stream[-1][2]
                #move stimulus with mouse
                stim.pos+=(change,0)    

            stim.draw()
            self.win.flip()
        #-------------------------------------------------------------------------
        # on soft code of state 3 freez movement
        #-------------------------------------------------------------------------
        still_show_event.wait()
        print("end")
        self.win.flip()
        # cleanup for next loop
        self.run_closed_loop=True
        self.run_open_loop=True
        display_stim_event.clear()
        still_show_event.clear()


        ##################################################################################################################################




#from PIL import Image
#import pygame
#import threading
#import os
#import time

class oldStimulus():
    def __init__(self, settings, rotary_encoder):
        """[summary]

        Args:
            settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler
            rotary_encoder (RotaryEncoder object): object handeling rotary encoder module
        """         
        self.settings = settings    
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
        self.stim = settings.stim
        #self.stim = "C:\\test_projekt\\test_projekt\\tasks\\behavior_1_test\\stimulus.png"
        self.surf = pygame.image.load(self.stim)
        self.screen_dim = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.fpsClock=pygame.time.Clock()
        self.rotary_encoder = rotary_encoder
        self.stimulus_position = []
        self.stim_center = self.get_stim_center()
        self.stim_end_pos_left = settings.stim_end_pos[0]+self.stim_center[0]
        self.stim_end_pos_right = settings.stim_end_pos[1]+self.stim_center[0]

    # flags
    def present_stimulus(self):
        """flag bevore stimulus appears on screen, set from softcode in bpood state"""        
        self.display_stim_event.set()
        print("present stimulus")

    def start_open_loop(self):
        """flag bevore open loop where wheel moves stimulus is started, set from softcode in bpod state"""        
        self.move_stim_event.set()
        print("start open loop")

    def stop_open_loop(self):
        """flag bevore open loop - while loop is stopped, time sleep so latent wheel movement which already triggered threshold
        can also move stimulus to final posititon
        """        
        time.sleep(0.05)
        self.run_open_loop = False
        print("stop open loop")

    def end_present_stimulus(self):
        """flag, which keeps stimulus frozen on end postition"""        
        self.still_show_event.set()
        print("end present stimulus")

    def end_trial(self):
        """routine that resets all flags and variables for new trial"""        
        self.display_stim_event.clear()
        self.move_stim_event.clear()
        self.still_show_event.clear()
        self.run_open_loop = True
        print("end pygame")

    def get_stim_center(self):
        """calculate the x,y coordinates for the stimulus so it is based centered on the middle screen"""        
        stim_dim = (Image.open(self.stim)).size
        rect = self.surf.get_rect()
        x = ( self.screen_dim[0]/2 - ( stim_dim[0]/2) )
        y = ( self.screen_dim[1]/2 - ( stim_dim[0]/2) )
        return([x, y])

    def keep_on_scrren(self, position_x):
        """keep the stimulus postition in user defined boundaries

        Args:
            position_x (int): current stimulus screen positition in pixel

        Returns:
            int: updated stimulus position
        """        
        return max(min(self.stim_end_pos_right, position_x), self.stim_end_pos_left)

    def run_game(self):
        """main loop running the pygame controlling the stimulus and enableing interaction via the rotary encoder"""        
        # pygame config
        os.environ['SDL_VIDEO_WINDOW_POS'] = "3840,0"#"2195,0"
        pygame.init()
        print("init")
        #===========================
        # Set up the drawing window
        pygame.display.init()
        #screen = pygame.display.set_mode(self.screen_dim,  pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
        screen = pygame.display.set_mode((6144,1536),  pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
        screen.fill((0, 0, 0))
        pygame.display.flip()
        # Create player
        position = self.get_stim_center()
        # create inital stimulus
        screen.blit(self.surf, position)
        #-----------------------------------------------------------------------------
        # on soft code of state 1
        #-----------------------------------------------------------------------------
        # present initial stimulus
        self.display_stim_event.wait()
        pygame.display.flip()
        # py game loop
        last_position = 0
        self.move_stim_event.wait()
        self.rotary_encoder.rotary_encoder.set_zero_position()
        self.rotary_encoder.rotary_encoder.enable_stream()
        self.rotary_encoder.rotary_encoder.current_position()
        while self.run_open_loop:
            # Fill the background with white
            screen.fill((0, 0, 0))
            screen.blit(self.surf, position)
            #-------------------------------------------------------------------------
            # on soft code of state 2
            #-------------------------------------------------------------------------
            # read rotary encoder stream
            #current_position = self.rotary_encoder.read_position()
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            #if current_position == None:
            #   continue
            #else:
            #    change_position = last_position - int(current_position)
            #    last_position = int(current_position)
            #    # move to the left
            #    position[0] += int(change_position*self.gain_right)

            if len(stream)>0:
                change_position = last_position - stream[-1][2]
                #print(stream)
                last_position = stream[-1][2]
                # move to the left
                # if change_position > 20:
                #     change_postition = 20
                position[0] += int(change_position*self.gain_right)
                position[0] = self.keep_on_scrren(position[0])
                #print(position[0])

            pygame.display.update()
            self.stimulus_position.append( (time.time(),position) )
        
        self.rotary_encoder.rotary_encoder.disable_stream()
        #show stimulus after closed loop period is over until reward gieven
        self.still_show_event.wait()
        self.end_trial()
        print("quite")
        screen.fill((0, 0, 0))
        pygame.display.flip()
        print("reset")
        print(self.settings.time_dict["time_inter_trial"])
        pygame.display.quit()
        pygame.quit()
        
