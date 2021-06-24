# Simple player in pygame
import time
import pygame
from player_class import Player

from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule


#=============================================================================
GAIN = 3
THRESHOLD = 2000
FPS=100
SCREEN_WIDTH = 5760
SCREEN_HEIGHT = 1200
t_end = time.time() + 20
#============================================================================


# rotary encoder config
ro = RotaryEncoderModule('COM6')
ro.enable_stream()
data_pref = [[0,0,0]]

# pygame config
pygame.init()
fpsClock=pygame.time.Clock()
fpsClock.tick(FPS)

# define keys and user interaction
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    )

#==============================================================================
# Set up the drawing window
#==============================================================================
pygame.display.init()
screen_dim = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(screen_dim, pygame.FULLSCREEN)
#DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill((0, 0, 0))


# Create player
player = Player("stimulus.jpg", screen_dim, GAIN)
position = player.stim_center()
stim_threshold = position[0] + THRESHOLD
# create inital stimulus
screen.blit(player.surf, position)

#-----------------------------------------------------------------------------
# on soft code of state 4
#-----------------------------------------------------------------------------
# present initial stimulus
pygame.display.flip()

#==============================================================================
# py game loop
#==============================================================================
running = True


# loop is running while open loop active
while time.time() < t_end:

    # Fill the background with white
    screen.fill((0, 0, 0))

    #==============================================================
    screen.blit(player.surf, position)


    # read rotary encoder stream
    #-------------------------------------------------------------------------
    # on soft code of state 15
    #-------------------------------------------------------------------------
    data = ro.read_stream()
    if len(data)==0 and running:
        continue
    elif running:
        print(data)

        pos_change = abs(data[0][2])-abs(data_pref[0][2])
        #print(f"data-pref: {data_pref[0][2]}  data-now: {data[0][2]} n")
        data_pref = data

        #repositin based on changes
        if data[0][2]<0:
            #player.move_left(pos_change)
            position[0] -= (pos_change*GAIN)

        if data[0][2]>0:
            #player.move_right(pos_change)
            position[0] += (pos_change*GAIN)
        # keep on screen
        if abs(position[0]) >= stim_threshold:
            running = False
            t_end = time.time() + 2

    pygame.display.update()

fpsClock.tick(FPS)


# Done! Time to quit.

ro.close()
pygame.quit()
