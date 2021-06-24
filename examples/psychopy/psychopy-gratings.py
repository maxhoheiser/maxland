# sinple psychopy example of different stimuli


from psychopy import visual, core, event, monitors, info #import some libraries from PsychoPy
import numpy as np

# Monitor parameters
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
    screen=2, 
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


#win.winHandle.maximize()
#win.winHandle.activate()
#win.fullscr = True
#win.flip()




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
    color = (0,255,0),
    mask = 'raisedCos',
)
grating_right.draw()


win.flip()

#grating = visual.GratingStim(win=win, mask='circle', size=10, pos=[-4,0], sf=3)
#fixation = visual.GratingStim(win=win, size=0.2, pos=[0,0], sf=0, rgb=-1)


# Moving Gratings =========================
#draw the stimuli and update the window
while True: #this creates a never-ending loop
    grating_left.setPhase(0.05, '+')#advance phase by 0.05 of a cycle
    grating_right.setPhase(0.01, '+')
    grating_left.draw()
    grating_right.draw()
    #fixation.draw()
    win.flip()

    if len(event.getKeys())>0:
        break
    event.clearEvents()







# Main Loop ===========================================================




while True:
    # update positions
    #circle.pos+=(np.random.rand(2)*2-1)/100
    
    if len(event.getKeys())>0:
        break
    event.clearEvents()
    win.flip()

#cleanup
win.clear()
win.close()
core.quit()