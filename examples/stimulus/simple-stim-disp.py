# Simple pygame program
import time
import pygame

pygame.init()

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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen_dim = [SCREEN_WIDTH, SCREEN_HEIGHT]

screen = pygame.display.set_mode(screen_dim)
#DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)



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
    # Create stimulus rectange
    STIM_WIDTH = 50
    STIM_HIGHT = 50
    stim = pygame.Surface((STIM_WIDTH, STIM_HIGHT))
    stim.fill((0, 0, 255))
    stim_rect = stim.get_rect()
    stim_center = (
        (SCREEN_WIDTH/2-STIM_WIDTH/2),
        (SCREEN_HEIGHT/2-STIM_HIGHT/2)
    )

    # Draw a solid blue circle in the center
    #pygame.draw.circle(screen, (0, 0, 255), (500, 500), 100)


    #==============================================================
    # load image to display
    stim_pic = pygame.image.load('stimulus.png')

    #==============================================================
    # Build the image & Flip the display
    screen.blit(stim_pic, stim_center)
    pygame.display.flip()







# Done! Time to quit.
pygame.quit()
