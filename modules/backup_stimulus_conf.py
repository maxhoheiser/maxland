from psychopy import visual, core, monitors #import some libraries from PsychoPy
import time
import threading
import os
import sys


run_open_loop = True
display_stim_event = threading.Event()
move_stim_event = threading.Event()
still_show_event = threading.Event()
# set gain
gain =  [abs(y/x) for x in settings_obj.thresholds[0:1] for y in settings_obj.stim_end_pos]
# gain to the left first - position
gain_left = gain[0]
# gain to the right second + position
gain_right = gain[1]
FPS = settings_obj.FPS
SCREEN_WIDTH = settings_obj.SCREEN_WIDTH
SCREEN_HEIGHT = settings_obj.SCREEN_HEIGHT
SCREEN_SIZE = (settings_obj.SCREEN_WIDTH,settings_obj.SCREEN_HEIGHT)
# stimulus    
rotary_encoder = rotary_encoder
correct_stim_side = correct_stim_side
# variables
closed_loop=True
open_loop=True

# TODO: nice solution
GAIN=1 #TODO: gain from usersettings_obj
pos = 0
change = 0

"""main psychopy funkction and loops"""        
# monitor configuration
monitor = monitors.Monitor('testMonitor', width=SCREEN_WIDTH, distance=SCREEN_HEIGHT)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
monitor.setSizePix(SCREEN_SIZE)
# create window
#create a window
win = visual.Window(
    size=(SCREEN_WIDTH, SCREEN_HEIGHT), 
    fullscr=True, 
    screen=1, 
    monitor=monitor,
    winType='pyglet', allowGUI=False, allowStencil=False,
    color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
win.winHandle.maximize() # fix black bar bottom
win.flip()
# get frame rate of monitor
expInfo = {}
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# flags
display_stim_event = False


# flags =========================================================================
# flag softcode 1
def present_stimulus(display_stim_event):
    """flag bevore stimulus appears on screen, set from softcode in bpood state"""        
    #display_stim_event.set()
    display_stim_event = True
    print("present stimulus")

# flag softcode 2
def start_open_loop(closed_loop):
    """flag bevore open loop where wheel moves stimulus is started, set from softcode in bpod state"""        
    #move_stim_event.set()
    closed_loop = False
    print("start open loop")

# flag softcode 3
def stop_open_loop(run_open_loop):
    """flag bevore open loop - while loop is stopped, time sleep so latent wheel movement which already triggered threshold
    can also move stimulus to final posititon
    """        
    run_open_loop = False
    print("stop open loop")

# flag softcode 4
def end_present_stimulus(still_show_event):
    """flag, which keeps stimulus frozen on end postition"""        
    still_show_event.set()
    print("end present stimulus")


# helper functions ===============================================================
def keep_on_scrren(position_x):
    """keep the stimulus postition in user defined boundaries

    Args:
        position_x (int): current stimulus screen positition in pixel

    Returns:
        int: updated stimulus position
    """        
    return max(min(stim_end_pos_right, position_x), stim_end_pos_left)
    

# stimulus functions =============================================================
def gen_grating(grating_sf, grating_or, pos, win, settings_obj):
    grating = visual.GratingStim(
        win=win,
        tex = 'sin', # texture used
        pos = (pos,0),
        units='pix',
        size=500,
        sf = grating_sf, 
        ori = grating_or,
        phase= (0.0,0.0),
        contrast = 1, # unchanged contrast (from 1 to -1)
        #units="deg",
        #pos = (0.0, 0.0), #in the middle of the screen. It is convertes internally in a numpy array
        #sf = 5.0 / 200.0, # set the spatial frequency 5 cycles/ 150 pixels. 
        #mask='raisedCos',
        mask = 'raisedCos'
    )
    return grating

def gen_stim(win,settings_obj):
    circle = visual.Circle(
        win=win,
        name='cicle',
        radius=100, #settings_obj.stimulus_rad,
        units='pix',
        edges=128,
        #units='pix',
        fillColor= (0,255,0), #settings_obj.stimulus_col,
        pos=(0,0),
        )
    return circle

# Main psychpy loop ==============================================================
def run_game(settings_obj,win, rotary_encoder):
    # get right grating
    if correct_stim_side["right"]:
        right_sf = settings_obj.stimulus_correct["grating_sf"]
        right_or = settings_obj.stimulus_correct["grating_ori"]
        left_sf = settings_obj.stimulus_wrong["grating_sf"]
        left_or = settings_obj.stimulus_wrong["grating_ori"]
    elif correct_stim_side["left"]:
        left_sf = settings_obj.stimulus_correct["grating_sf"]
        left_or = settings_obj.stimulus_correct["grating_ori"]
        right_sf = settings_obj.stimulus_wrong["grating_sf"]
        right_or = settings_obj.stimulus_wrong["grating_ori"]
    # generate gratings and stimuli
    grating_left = gen_grating(left_sf,left_or,-900)#left_sf,left_or,settings_obj.stim_end_pos[0] ,win)
    grating_right = gen_grating(right_sf,right_or,900) #right_sf,right_or,settings_obj.stim_end_pos[1] ,win)
    stim = gen_stim()
    #-----------------------------------------------------------------------------
    # on soft code of state 1
    #-----------------------------------------------------------------------------
    # present initial stimulus
    #while display_stim_event:
    #    pass
    print("closed loop")
    sys.stdout.flush()
    while closed_loop: 
        # dram moving gratings
        grating_left.setPhase(0.02, '+')#advance phase by 0.05 of a cycle
        grating_right.setPhase(0.02, '+')
        grating_left.draw()
        grating_right.draw()
        stim.draw()
        win.flip()
    #-------------------------------------------------------------------------
    # on soft code of state 2
    #-------------------------------------------------------------------------
    # reset rotary encoder
    rotary_encoder.rotary_encoder.set_zero_position()
    rotary_encoder.rotary_encoder.enable_stream()
    # open loop
    print("open loop")
    sys.stdout.flush()
    while True: #open_loop:
        # dram moving gratings
        grating_left.setPhase(0.02, '+')#advance phase by 0.05 of a cycle
        grating_right.setPhase(0.02, '+')
        grating_left.draw()
        grating_right.draw()
        # get rotary encoder change position
        stream = rotary_encoder.rotary_encoder.read_stream()
        if len(stream)>0:
            change = pos - stream[-1][2]
            pos = stream[-1][2]
            #move stimulus with mouse
            stim.pos+=(change*GAIN,0)    
        stim.draw()
        win.flip()
        sys.stdout.flush()
    #-------------------------------------------------------------------------
    # on soft code of state 3 freez movement
    #-------------------------------------------------------------------------
    still_show_event.wait()
    win.flip()
    win.clear()
    # cleanup
    open_loop = True
    closed_loop = True
    # reset flags
    display_stim_event.clear()
    still_show_event.clear()



