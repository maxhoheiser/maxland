from PIL import Image
import pygame
import threading


class Stimulus():
    def __init__(self, settings, rotary_encoder):
        self.run_open_loop = True
        self.display_stim_event = threading.Event()
        self.move_stim_event = threading.Event()
        self.still_show_event = threading.Event()
        self.exit_trial_event = threading.Event()
        self.GAIN = settings.GAIN
        if self.GAIN < 0:
            self.GAIN = 0.01
        self.FPS = settings.FPS
        self.SCREEN_WIDTH = settings.SCREEN_WIDTH
        self.SCREEN_HEIGHT = settings.SCREEN_HEIGHT
        self.STIMULUS = settings.STIMULUS
        self.surf = pygame.image.load(self.STIMULUS)
        self.screen_dim = [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        self.fpsClock=pygame.time.Clock()
        self.rotary_encoder = rotary_encoder
        self.TRIAL_NUM = 0
        for block in settings.BLOCKS:
            self.TRIAL_NUM += block[TRIAL_NUM_BLOCK]

    def present_stimulus(self):
        self.display_stim_event.set()

    def start_open_loop(self):
        self.move_stim_event.set()

    def stop_open_loop(self):
        self.run_open_loop = False

    def end_present_stimulus(self):
        self.still_show_event.set()

    def end_trial(self):
        self.display_stim_event.clear()
        self.move_stim_event.clear()
        self.still_show_event.clear()
        self.run_open_loop = True

    def stim_center(self):
        stim_dim = (Image.open(self.STIMULUS)).size
        rect = self.surf.get_rect()
        x = ( self.screen_dim[0]/2 - ( stim_dim[0]/2) )
        y = ( self.screen_dim[1]/2 - ( stim_dim[0]/2) )
        return([x, y])

    # ==== helper ===== remove later =================================

    def fps_clock(self):
        font = pygame.font.SysFont("Arial", 180)
        fr = str(int(self.fpsClock.get_fps()))
        frt = font.render(fr, 1, pygame.Color("coral"))
        return frt


    # ==== helper ===== remove later =================================

    def run_game(self):
        # pygame config
        pygame.init()

        #===========================
        # Set up the drawing window
        pygame.display.init()
        screen = pygame.display.set_mode(self.screen_dim, pygame.FULLSCREEN)
        screen.fill((0, 0, 0))

        for trial in range(self.TRIAL_NUM):
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

            #=========================
            # py game loop
            # loop is running while open loop active
            last_position = 0
            self.move_stim_event.wait()
            self.rotary_encoder.enable_stream()
            while self.run_open_loop:
                self.fpsClock.tick(self.FPS)
                screen.blit(self.fps_clock(), (2600,0))
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
                    last_position = current_position
                    # move to the left
                    if change_position > 0:
                        position[0] -= int(change_position*self.GAIN)
                    # move to the right
                    else:
                        position[0] -= int(change_position*self.GAIN)
                print(position)
                pygame.display.update()
            self.rotary_encoder.disable_stream()
            #show stimulus after closed loop period is over until reward gieven
            self.still_show_event.wait()
            screen.fill((0, 0, 0))
            pygame.display.flip()
            self.end_trial()

    pygame.quit()
