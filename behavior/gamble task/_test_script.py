cd "C:\Users\User\Google Drive\3.1 Code Repository\Maxland\tasks\behavior-gambl_task"
import os
import json


# Test TrialsParameterHAndler Object ==========================================================
from parameter import TrialParameterHandler
import usersettings

import importlib
importlib.reload(usersettings)

# create usersettings object
settings_obj = TrialParameterHandler(usersettings, os.getcwd())
settings_obj.update_userinput_file()



# Test Tkinter Window =========================================================================


from userinput import UserInput
input_obj = UserInput(settings_obj)

window = UserInput(settings_obj)
window.draw_window()
window.show_window()

settings_obj = window.settings
settings_obj.update_userinput_file()
     

# Test Probability Calculator Object ==========================================================
from probability import ProbabilityConstuctor
probability_obj = ProbabilityConstuctor(settings_obj)
probability_list = probability_obj.probability_list

# update settings object
settings_obj.probability_list = probability_obj.probability_list
settings_obj.trial_num = probability_obj.trial_num
settings_obj.update_userinput_file()

# test dump settings_obj as json
with open(os.path.join(os.getcwd(),'session_settings.py'), 'w') as f:
    f.write(settings_obj.toJSON())


# Test Stimulus ==============================================================================
from pybpodapi.bpod import Bpod
bpod = Bpod('COM7')

from rotaryencoder import BpodRotaryEncoder
rotary_encoder_module = BpodRotaryEncoder('COM3', settings_obj)
rotary_encoder_module.load_message(bpod)
rotary_encoder_module.configure()

from stimulus import Stimulus
stimulus_game = Stimulus(settings_obj, rotary_encoder_module)


import time
import threading

for trial in range(5):
    threading.Thread(target=stimulus_game.run_game, daemon=True).start()
    time.sleep(1)
    stimulus_game.present_stimulus()
    time.sleep(10)
    stimulus_game.start_open_loop()
    time.sleep(1)
    stimulus_game.stop_open_loop()
    time.sleep(1)
    stimulus_game.end_present_stimulus()
    time.sleep(1)
    
rotary_encoder_module.close()
bpod.close()



#==========================================================================================
from screeninfo import get_monitors
for m in get_monitors():
    print(str(m))

import pygame
# parameters
screen_dim = (6144,1536)
stim = "C:\\test_projekt\\test_projekt\\tasks\\behavior_1_test\\stimulus.png"
surf = pygame.image.load(stim)

def stim_center():
    from PIL import Image
    """calculate the x,y coordinates for the stimulus so it is based centered on the middle screen
    """        
    stim_dim = (Image.open(stim)).size
    rect = surf.get_rect()
    x = ( screen_dim[0]/2 - ( stim_dim[0]/2) )
    y = ( screen_dim[1]/2 - ( stim_dim[0]/2) )
    return([x, y])

position = stim_center()


# pygame    
os.environ['SDL_VIDEO_WINDOW_POS'] = "3840,0"#"2195,0"
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode(screen_dim,  pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
screen.fill((0, 0, 0))
pygame.display.flip()
print(f"\n\nscreen dim: {screen_dim}\nstim center:{position}\n\n")
# create inital stimulus
screen.blit(surf, position)
pygame.display.flip()
pygame.display.quit()
pygame.quit()
