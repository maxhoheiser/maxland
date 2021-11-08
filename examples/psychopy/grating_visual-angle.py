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
from psychopy import visual, event, monitors, core, tools
from math import tan

# Monitor parameters
MON_DISTANCE = 16  # Distance between subject's eyes and monitor
MON_WIDTH = 35.79  # Width of your monitor in cm
MON_SIZE = [6144,1536]#[1792, 1120]  # Pixel-dimensions of your monitor
SAVE_FOLDER = 'templateData'  # Log is saved to this folder. The folder is created if it does not exist.

# 1. creates window in which the grating will be placed (background)
my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_SIZE)

# Stimulus parameters
grating_SF = 0.25  # 4 cycles per degree visual angle
grating_SIZE = 60  # in degrees visual angle
grating_ori = 45



def get_size(angle):
    x_cm = 2 * MON_DISTANCE * tan(angle/2)
    x_pix = x_cm * MON_SIZE[0]/MON_WIDTH
    return x_pix

x_in_pix = get_size(grating_SIZE)

grating_SIZE_pix = tools.monitorunittools.deg2pix(grating_SIZE,my_monitor)
grating_SF_pix = tools.monitorunittools.pix2deg(grating_SF,my_monitor)


win = visual.Window(
    monitor=my_monitor,
    size=MON_SIZE,  # Put the value from the display. size of the window in pixels
    color=[-1, -1, -1],  # Color of background as [r,g,b].Each take values between -1.0 and 1.0.
    units="pix",  # "deg",
    fullscr=True,
    screen=1,
)


# 2. creates grating in window in degree
grating_deg = visual.GratingStim(
    win=win,
    contrast=1,  # unchanged contrast (from 1 to -1)
    units="deg",
    size=grating_SIZE,
    sf=grating_SF,
    tex='sin',  # texture used
    ori=grating_ori,
    mask='raisedCos',
    opacity=1.0,
    pos=(-30, 0)
)




# 2. creates grating in window in degree
grating_pix = visual.GratingStim(
    win=win,
    contrast=1,  # unchanged contrast (from 1 to -1)
    units="pix",
    size=grating_SIZE_pix,
    sf=grating_SF_pix,
    tex='sin',  # texture used
    ori=grating_ori,
    mask='raisedCos',
    opacity=1.0,
    pos=(30, 0)
)


# this creates a never-ending loop
trialClock = core.Clock()
t = 0

while t < 5:
    t = trialClock.getTime()
    grating_deg.setPhase(1.5, '+')  # temporal phase. Increment (+) the phase by 0.015 of a cycle
    grating_deg.setPhase(1.5*t)
    #grating_pix.setPhase(1.5, '+')  # temporal phase. Increment (+) the phase by 0.015 of a cycle
    #grating_pix.setPhase(1.5*t)
    grating_deg.opacity=0.2
    grating_deg.draw()
    #grating_pix.draw()
    win.flip()
    # win.update() it produce the same that win.flip()
    # win.getMovieFrame(buffer='front') # values,back, none


#filename = str(globals()['grating_ori'])+ str(globals()['grating_SF']) + '.mp4'
#win.saveMovieFrames(fileName = filename, clearFrames = 'True')

#win.saveMovieFrames(fileName = 'drif90_025.mp4')
win.close()

