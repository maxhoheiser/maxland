# Simple player in pygame
import time
import pygame
from player_class import Player


from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
import time



GAIN = 3


# rotary encoder config
ro = RotaryEncoderModule('COM6')
ro.enable_stream()


t_end = time.time() + 20
data_pref = [[0,0,0]]


# pygame config
pygame.init()

FPS=100
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
SCREEN_WIDTH = 5760
SCREEN_HEIGHT = 1200
screen_dim = [SCREEN_WIDTH, SCREEN_HEIGHT]

screen = pygame.display.set_mode(screen_dim)
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)



# Create player
player = Player("stimulus.jpg", screen_dim, GAIN)
position = player.stim_center()

# present inital stimulus
screen.blit(player.surf, position)

#-----------------------------------------------------------------------------
# on soft code of state 4
#-----------------------------------------------------------------------------
pygame.display.flip()
for mode in pygame.display.list_modes():
        print(mode)
        
#==============================================================================
# py game loop
#==============================================================================
running = True
t_end = time.time() + 20

#-------------------------------------------------------------------------
# loop is running while open loop active
#-------------------------------------------------------------------------
while running and (time.time() < t_end):

    # Did the user click the window close button or ESC?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False


    # Fill the background with white
    screen.fill((0, 0, 0))

    #==============================================================
    DISPLAYSURF.blit(player.surf, position)
 

  
    # read rotary encoder stream
    #-------------------------------------------------------------------------
    # on soft code of state 15
    #-------------------------------------------------------------------------
    data = ro.read_stream()
    if len(data)==0:
        continue
    else:
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
        if position[0] > (SCREEN_WIDTH-player.stim_dim[0]):
            position[0] = (SCREEN_WIDTH-player.stim_dim[0])
        if position[0] < -( ( SCREEN_WIDTH/2 ) - 3/2*player.stim_dim[0] ) :
            position[0] = -( ( SCREEN_WIDTH/2) - 3/2*player.stim_dim[0] )

    pygame.display.update()

#freez stim in postition
position = player.stim_center()
screen.blit(player.surf, position)

# Done! Time to quit.
#fpsClock.tick(FPS)

ro.close()
pygame.quit()
        