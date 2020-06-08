from PIL import Image
import pygame
import threading
import os


class Stimulus():
    def __init__(self, settings, rotary_encoder):
        self.run_open_loop = True
        self.display_stim_event = threading.Event()
        self.move_stim_event = threading.Event()
        self.still_show_event = threading.Event()
        # set gain
        self.GAIN =  [abs(y/x) for x in settings.ALL_THRESHOLDS[0:1] for y in settings.STIM_END_POS ]
        self.FPS = settings.FPS
        self.SCREEN_WIDTH = settings.SCREEN_WIDTH
        self.SCREEN_HEIGHT = settings.SCREEN_HEIGHT
        self.STIMULUS = settings.STIMULUS
        self.surf = pygame.image.load(self.STIMULUS)
        self.screen_dim = [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        self.fpsClock=pygame.time.Clock()
        self.rotary_encoder = rotary_encoder

    def present_stimulus(self):
        self.display_stim_event.set()
        print("present stimulus")

    def start_open_loop(self):
        self.move_stim_event.set()
        print("start open loop")

    def stop_open_loop(self):
        self.run_open_loop = False
        print("stop open loop")

    def end_present_stimulus(self):
        self.still_show_event.set()
        print("end present stimulus")

    def end_trial(self):
        self.display_stim_event.clear()
        self.move_stim_event.clear()
        self.still_show_event.clear()
        self.run_open_loop = True
        print("end trial")

    def stim_center(self):
        stim_dim = (Image.open(self.STIMULUS)).size
        rect = self.surf.get_rect()
        x = ( self.screen_dim[0]/2 - ( stim_dim[0]/2) )
        y = ( self.screen_dim[1]/2 - ( stim_dim[0]/2) )
        return([x, y])

    def run_game(self):
        # pygame config
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        pygame.init()
        #===========================
        # Set up the drawing window
        pygame.display.init()
        screen = pygame.display.set_mode(self.screen_dim,  pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
        screen.fill((0, 0, 0))
        pygame.display.flip()
        # Create player
        position = self.stim_center()
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
        self.rotary_encoder.enable_stream()
        while self.run_open_loop:
            # Fill the background with white
            screen.fill((0, 0, 0))
            screen.blit(self.surf, position)
            #-------------------------------------------------------------------------
            # on soft code of state 2
            #-------------------------------------------------------------------------
            # read rotary encoder stream
            current_position = self.rotary_encoder.read_position()
            if current_position == None:
                continue
            else:
                change_position = last_position - int(current_position)
                last_position = int(current_position)
                # move to the left
                if change_position > 0:
                    position[0] -= int(change_position*self.GAIN)
                # move to the right
                else:
                    position[0] -= int(change_position*self.GAIN)
            pygame.display.update()
        self.rotary_encoder.disable_stream()
        #show stimulus after closed loop period is over until reward gieven
        self.still_show_event.wait()
        screen.fill((0, 0, 0))
        pygame.display.flip()
        self.end_trial()
        pygame.display.quit()
        pygame.quit()
