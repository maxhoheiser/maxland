# Simple player in pygame
import time
import pygame
from player_class import Player

pygame.init()
FPS=100
fpsClock=pygame.time.Clock()

#==============================================================================
# define keys and user interaction
#==============================================================================
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    )

#==============================================================================
# Set up the drawing window
#==============================================================================
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
screen_dim = [SCREEN_WIDTH, SCREEN_HEIGHT]

screen = pygame.display.set_mode(screen_dim)
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)



# Create player
player = Player("stimulus.png", screen_dim)
position = player.stim_center()

#==============================================================================
# py game loop
#==============================================================================
running = True
t_end = time.time() + 20
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


        
    #player.update(pressed_keys)

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT]:
        position[0] -= 2

    if keys_pressed[pygame.K_RIGHT]:
        position[0] += 2

    pygame.display.update()
    fpsClock.tick(FPS)



    # lip the display
    #pygame.display.flip()







# Done! Time to quit.
pygame.quit()
