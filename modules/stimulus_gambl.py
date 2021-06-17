from PIL import Image
import pygame
import threading
import os
import time


class Stimulus():
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
        
