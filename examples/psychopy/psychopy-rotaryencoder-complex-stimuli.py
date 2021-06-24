# sinple psychopy example of different stimuli
# using pybpod roatry encoder as input


from psychopy import visual, core, event, monitors, info #import some libraries from PsychoPy
from psychopy.hardware import keyboard
import numpy as np
import time

from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule

# Setup Bpod Rotary Encoder Input =======================================
rotary_encoder = RotaryEncoderModule('/dev/cu.usbmodem65305701')
rotary_encoder.enable_stream()

def set_wrap_point(ro,wrap_point):
    """set the point at which the position is automatically set back to 0 => one half rotation

    Args:
        wrap_point (int): one half rotation wehre set to zero again

    Returns:
        [type]: [description]
    """        
    array = np.array([np.uint8(wrap_point)])
    ro.arcom.write_array([ord('W')] + array )
    return ro.arcom.read_uint8() == 1

set_wrap_point(rotary_encoder,0)



# Monitor parameters ====================================================
MON_DISTANCE = 16  # Distance between subject's eyes and monitor
MON_WIDTH = 20  # Width of your monitor in cm
MON_SIZE = (2048,1536)  #[1024, 1280]  # Pixel-dimensions of your monitor
SAVE_FOLDER = 'templateData'  # Log is saved to this folder. The folder is created if it does not exist.

# create monitor
monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
monitor.setSizePix(MON_SIZE)

#create a window
win = visual.Window(
    size=(2048, 1536), 
    fullscr=True, 
    screen=1, 
    monitor=monitor,
    winType='pyglet', allowGUI=False, allowStencil=False,
    color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
win.winHandle.maximize() # fix black bar bottom

# get frame rate of monitor
expInfo = {}
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess


# Grating Stimuli ========================================================
# Stimulus parameters
grating_SF = 0.25  # 4 cycles per degree visual angle
grating_SIZE = 45  # depending on canfaz measure type - no in screen hight
grating_ori = 0   # in degree

grating_left = visual.GratingStim(
    win=win,
    tex = 'sin', # texture used
    pos = (-500,0),
    units='pix',
    size=500,
    sf = 0.02, 
    ori = 90,
    phase= (0.0,0.0),
    contrast = 1, # unchanged contrast (from 1 to -1)
    #units="deg",
    #pos = (0.0, 0.0), #in the middle of the screen. It is convertes internally in a numpy array
    #sf = 5.0 / 200.0, # set the spatial frequency 5 cycles/ 150 pixels. 
    #mask='raisedCos',
    mask = 'raisedCos'
)
grating_left.draw()

grating_right = visual.GratingStim(
    win=win,
    tex = 'sin', # texture used
    pos = (500,0),
    units='pix',
    size=500,
    sf = 0.005, 
    ori = 0,
    phase= (0.0,0.0),
    contrast = 1, # unchanged contrast (from 1 to -1)
    #units="deg",
    #pos = (0.0, 0.0), #in the middle of the screen. It is convertes internally in a numpy array
    #sf = 5.0 / 200.0, # set the spatial frequency 5 cycles/ 150 pixels. 
    #mask='raisedCos',
    #color = (0,0,0),
    mask = 'raisedCos',
)
grating_right.draw()


# Moving Stimulus =======================================================
circle = visual.Circle(
    win=win,
    name='cicle',
    radius=100,
    units='pix',
    edges=128,
    #units='pix',
    fillColor=[0,255,0],
    pos=(0,0),
    )
circle.draw()

# flip initial design
win.flip()


# Main Loop =========================================================================================

timeout = time.time() + 10   # 10 sec  from now


pos_x = 0
GAIN=1
stream_data = []
pos_x_data = []
pos = 0
change = 0

while True: 
    # dram moving gratings
    grating_left.setPhase(0.05, '+')#advance phase by 0.05 of a cycle
    grating_right.setPhase(0.01, '+')
    grating_left.draw()
    grating_right.draw()

    # get rotary encoder change position
    stream = rotary_encoder.read_stream()
    if len(stream)>0:
        change = pos - stream[-1][2]
        pos = stream[-1][2]
        #move stimulus with mouse
        circle.pos+=(change*GAIN,0)    
        stream_data.append(stream[-1][2])   
        pos_x_data.append(pos_x)
    circle.draw()
    

    win.flip()
    #event.clearEvents()
    if time.time() > timeout:
        break



#cleanup
win.clear()
win.close()
core.quit()



data = np.zeros([len(stream_data),2])
data[:,0]=stream_data
data[:,1]=pos_x_data