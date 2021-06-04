# sinple psychopy example of different stimuli


from psychopy import visual, core, event, monitors #import some libraries from PsychoPy
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
"""
win = visual.Window(
    size=[2048,1536],
    #winType='pyglet',
    monitor="testMonitor", 
    #units='pixel',#'height',#'deg',
    screen=2,
    fullscr=True,
    color=[-1,-1,-1],
    colorSpace='rgb',
    )
"""

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


#win.winHandle.maximize()
#win.winHandle.activate()
#win.fullscr = True
#win.flip()




# Grating Stimuli ========================================================
#grating = visual.GratingStim(win=win, mask='circle', size=10, pos=[-4,0], sf=3)
#fixation = visual.GratingStim(win=win, size=0.2, pos=[0,0], sf=0, rgb=-1)

"""
# Moving Gratings =========================
#draw the stimuli and update the window
while True: #this creates a never-ending loop
    grating.setPhase(0.05, '+')#advance phase by 0.05 of a cycle
    grating.draw()
    fixation.draw()
    win.flip()

    if len(event.getKeys())>0:
        break
    event.clearEvents()
"""




# Cicle Stimuli =========================================================

circle = visual.Circle(
    win=win,
    name='cicle',
    radius=0.1,
    edges=128,
    #units='pix',
    fillColor=[0,0,255],
    pos=(0,0),
    )
circle.autoDraw = True
#win.flip()


polygon = visual.Rect(
    win=win, 
    name='polygon',
    width=(0.2, 0.2)[0], 
    height=(0.2, 0.2)[1],
    ori=0.0, 
    pos=(0, -0.5),
    lineWidth=1.0,     
    colorSpace='rgb',  
    lineColor='white', 
    fillColor='white',
    opacity=None, 
    depth=0.0, 
    interpolate=True
    )
#polygon.draw()
#polygon.setAutoDraw(False) # remove auto draw
polygon.autoDraw = True # will keep it always drawin if win is flipped
#win.flip()


## Text Stimmuli ========================================================

message_a = visual.TextStim(
    win=win, 
    text='A',
    color=[0,255,0],
    pos=(-0.7, -0.2),
    opacity=1.0,
    #height=1,
    )
message_a.size=5
message_a.autoDraw = True


message_b = visual.TextStim(
    win=win, 
    text='B',
    color=[255,0,0],
    pos=(0.7, -0.2),
    opacity=1.0,
    #height=1,
    )
message_b.size = 5
message_b.autoDraw = True  # Automatically draw every frame

win.flip()
#core.wait(5.0)



# Main Loop ===========================================================



circle_2 = visual.Circle(
    win=win,
    name='cicle',
    radius=0.01,
    edges=128,
    #units='pix',
    fillColor=[255,0,0],
    pos=(0,0),
    )
circle_2.autoDraw = True



while True:
    # update positions
    #circle.pos+=(np.random.rand(2)*2-1)/100
    circle.pos+=(0.01,0.01)
    polygon.pos+=(np.random.rand(2)*2-1)/100
    message_a.pos+=(np.random.rand(2)*2-1)/100
    message_b.pos+=(np.random.rand(2)*2-1)/100
    if len(event.getKeys())>0:
        break
    event.clearEvents()
    win.flip()

#cleanup
win.clear()
win.close()
core.quit()