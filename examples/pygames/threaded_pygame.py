from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
import numpy as np
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from pybpodapi.com.arcom import ArCOM, ArduinoTypes

import time
import pygame
from player_class import Player
import threading

rotary_encoder = RotaryEncoderModule('COM6')
rotary_encoder.enable_stream()



# Simple player in pygame


#====================================================================================================================
#pygame
#====================================================================================================================
class py_game():

    def __init__(self):
        self.run_open_loop = True
        self.display_stim_event = threading.Event()
        self.move_stim_event = threading.Event()
        self.still_show_event = threading.Event()
        self.GAIN = 3
        self.THRESHOLD = 2000
        self.FPS=100
        self.SCREEN_WIDTH = 5760
        self.SCREEN_HEIGHT = 1200
        self.STIMULUS = r"C:\test\tasks\behavior 01\stimulus.jpg"


    def present_stimulus(self):
        self.display_stim_event.set()

    def start_open_loop(self):
        self.move_stim_event.set()

    def stop_open_loop(self):
        self.run_open_loop = False

    def end_present_stimulus(self):
        self.still_show_event.set()

    def exit(self):
        self.display_stim_event.clear()
        self.move_stim_event.clear()
        self.still_show_event.clear()
        self.run_open_loop = True

    def run_game(self):
        # pygame config
        pygame.init()
        fpsClock=pygame.time.Clock()
        fpsClock.tick(self.FPS)

        # define keys and user interaction
        from pygame.locals import (
            K_ESCAPE,
            KEYDOWN,
            QUIT,
            )

        #===========================
        # Set up the drawing window
        pygame.display.init()
        screen_dim = [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        screen = pygame.display.set_mode(screen_dim, pygame.FULLSCREEN)
        #DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill((0, 0, 0))

        # Create player
        player = Player(self.STIMULUS, screen_dim, self.GAIN)
        position = player.stim_center()
        stim_threshold = position[0] + self.THRESHOLD
        # create inital stimulus
        screen.blit(player.surf, position)

        #-----------------------------------------------------------------------------
        # on soft code of state 1
        #-----------------------------------------------------------------------------
        # present initial stimulus
        self.display_stim_event.wait()
        pygame.display.flip()

        #=========================
        # py game loop
        # loop is running while open loop active
        data_pref = [[0,0,0]]
        while self.run_open_loop:
            # Fill the background with white
            screen.fill((0, 0, 0))
            screen.blit(player.surf, position)

            #-------------------------------------------------------------------------
            # on soft code of state 2
            #-------------------------------------------------------------------------
            # read rotary encoder stream
            self.move_stim_event.wait()
            data = rotary_encoder.read_stream()
            running = True
            if len(data)==0:
                continue
            else:
                pos_change = abs(data[0][2])-abs(data_pref[0][2])
                #print(f"data-pref: {data_pref[0][2]}  data-now: {data[0][2]} n")
                data_pref = data

                #repositin based on changes
                if data[0][2]<0:
                    #player.move_left(pos_change)
                    position[0] -= (pos_change*self.GAIN)

                if data[0][2]>0:
                    #player.move_right(pos_change)
                    position[0] += (pos_change*self.GAIN)
                # # keep on screen
                # if abs(position[0]) >= stim_threshold:
                #     running = False

            pygame.display.update()

        #show stimulus after closed loop period is over until reward gieven
        self.still_show_event.wait()
        screen.fill((0, 0, 0))
        pygame.display.flip()

        fpsClock.tick(self.FPS)
        pygame.quit()
        print("end of game loop")



def waiter():
    stimulus_game = py_game()
    for trial in range(5):
        t1 = threading.Thread(target=stimulus_game.run_game)
        t1.start()
        print(f"start {trial}")
        time.sleep(2)
        print("start stimulus pres")
        stimulus_game.present_stimulus()
        time.sleep(2)
        print("start open loop")
        stimulus_game.start_open_loop()
        time.sleep(10)
        print("stop open loop")
        stimulus_game.stop_open_loop()
        time.sleep(2)
        print("remove stim")
        stimulus_game.end_present_stimulus()
        stimulus_game.exit()
        #t1.kill()
        t1.join()
        print("end of game loop")

t2 = threading.Thread(target=waiter)
t2.start()
t2.join()
print("end all")


rotary_encoder.close()
        

    