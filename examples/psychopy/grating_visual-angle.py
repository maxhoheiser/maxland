'''
script 1: creates black and white grating stimulus

1. Fisrt it creates a window whwre to draw the figure 
2. Second create two grating figures: grating square and a circular (with smooth borders)

Important information
If specifying your own texture using an image or numpy array you should ensure 
that the image has square power-of-two dimesnions (e.g. 256 x 256). 
If not then PsychoPy will upsample your stimulus to the next larger power of two


For the ‘raisedCos’ mask, pass a dict: {‘fringeWidth’:0.2}, 0.2 it is the default value
where ‘fringeWidth’ is a parameter (float, 0-1), 
determining the proportion of the patch that will be blurred by the raised cosine edge.

Low spatial frequency, bars get wider
'''
from psychopy import visual,event,monitors,core

# Monitor parameters
MON_DISTANCE = 16  # Distance between subject's eyes and monitor
MON_WIDTH = 30  # Width of your monitor in cm
MON_SIZE = [1024, 1280]  # Pixel-dimensions of your monitor
SAVE_FOLDER = 'templateData'  # Log is saved to this folder. The folder is created if it does not exist.


# Stimulus parameters
grating_SF = 0.25  # 4 cycles per degree visual angle
grating_SIZE = 45  # in degrees visual angle
grating_ori = 45


#1. creates window in which the grating will be placed (background)
my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_SIZE)

win = visual.Window(
    monitor= my_monitor,
    size= MON_SIZE, # Put the value from the display. size of the window in pixels
    color=[0.169,0.169, 0.169], #Color of background as [r,g,b].Each take values between -1.0 and 1.0.
    units="pix",#"deg",
    fullscr=False
)


#2. creates grating in window
grating = visual.GratingStim(
    win=win,
    contrast = 1, # unchanged contrast (from 1 to -1)
    units="deg",
    #pos = (0.0, 0.0), #in the middle of the screen. It is convertes internally in a numpy array
    size=grating_SIZE,
    #sf = 5.0 / 200.0, # set the spatial frequency 5 cycles/ 150 pixels. 
    sf = grating_SF, 
    tex = 'sin', # texture used
    ori = grating_ori,
    mask='raisedCos'
)


#this creates a never-ending loop
trialClock = core.Clock()
t = 0

while t < 10: 
    t = trialClock.getTime()
    grating.setPhase(1.5, '+')  # temporal phase. Increment (+) the phase by 0.015 of a cycle
    grating.setPhase(1.5*t)
    grating.draw()
    win.flip() 
    #win.update() it produce the same that win.flip()
    #win.getMovieFrame(buffer='front') # values,back, none


#filename = str(globals()['grating_ori'])+ str(globals()['grating_SF']) + '.mp4'
#win.saveMovieFrames(fileName = filename, clearFrames = 'True')

#win.saveMovieFrames(fileName = 'drif90_025.mp4')

win.close()