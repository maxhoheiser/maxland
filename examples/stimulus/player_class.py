from PIL import Image
import pygame


#==========================================================================
# define gamer class
#==========================================================================
class Player(pygame.sprite.Sprite):
    """
    calculates the center position for the given picture stimulus
    -------
    Returns
    -------
    object with stim picture
    """


    def __init__(self, image, screen_dim, gain ):
        super(Player, self).__init__()
        self.surf = pygame.image.load(image)
        self.image = image
        self.screen_dim = screen_dim
        self.file = Image.open(self.image)
        self.stim_dim = self.file.size
        self.rect = self.surf.get_rect()
        self.STIM_OFFSET_Y = 0
        self.STIM_OFFSET_X = 0
        self.GAIN = gain

    # return x,y coordinates for stim postition
    def stim_center(self):
        self.x = ( self.screen_dim[0]/2 - ( self.stim_dim[0]/2 + self.STIM_OFFSET_X ) )
        self.y = ( self.screen_dim[1]/2 - ( self.stim_dim[0]/2 + self.STIM_OFFSET_Y ) )
        return([self.x, self.y])
        #ToDo Max: add offset for stimulus in y direction
    
    
    # # updates stim postion based on user input
    # def update(self, pos_change):
        
    #     if data[0][2]<0:
    #         position[0] -= (pos_change*GAIN)

    #     if data[0][2]>0:
    #         position[0] += (pos_change*GAIN)
        
    #     #keep stimulus on screen
    #     if self.rect.left < 0:
    #         self.rect.left = 0
    #     if self.rect.right > SCREEN_WIDTH:
    #         self.rect.right = SCREEN_WIDTH
    #     if self.rect.top <= 0:
    #         self.rect.top = 0
    #     if self.rect.bottom >= SCREEN_HEIGHT:
    #         self.rect.bottom = SCREEN_HEIGHT
     
    # #move left or right
    # def move_left(self, pos_change):
    #     self.pos_change = pos_change
    #     self.update(pos_change)
    #     return
    # def move_right(self, pos_change):