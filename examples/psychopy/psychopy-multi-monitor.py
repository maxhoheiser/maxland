# indetify the monitors
#create two monitors 
#display text on one or the other or both


from psychopy import visual,event,monitors,core


# Monitor parameters
MON_DISTANCE = 16  # Distance between subject's eyes and monitor
MON_WIDTH = 20  # Width of your monitor in cm
#MON_SIZE = (2560,1440)
MON_SIZE = [2048,1536] # Pixel-dimensions of your monitor

#1. creates window in which the grating will be placed (background)
monitor0 = monitors.Monitor('mon0', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
monitor0.setSizePix(MON_SIZE)


# create stimulus window
win0 = visual.Window(
    monitor=monitor0,
    screen = 2,
    size=MON_SIZE,
    color=[0.169,0.169, 0.169], #Color of background as [r,g,b].Each take values between -1.0 and 1.0.
    units="deg",
    fullscr=True
)

# create stimulus window
win1 = visual.Window(
    #monitor= my_monitor,
    monitor=monitor0,
    screen = 1,
    #size= MON_SIZE, # Put the value from the display. size of the window in pixels
    #color=[0.10,0.10, 0.10], #Color of background as [r,g,b].Each take values between -1.0 and 1.0.
    units="deg",
    fullscr=False
)

# create stimulus window
win2 = visual.Window(
    #monitor= my_monitor,
    monitor=monitor0,
    screen = 2,
    #size= MON_SIZE, # Put the value from the display. size of the window in pixels
    #color=[0.10,0.10, 0.10], #Color of background as [r,g,b].Each take values between -1.0 and 1.0.
    units="deg",
    fullscr=True
)

# create stimulus window
win3 = visual.Window(
    #monitor= my_monitor,
    monitor=monitor0,
    screen = 2,
    #size= MON_SIZE, # Put the value from the display. size of the window in pixels
    #color=[0.10,0.10, 0.10], #Color of background as [r,g,b].Each take values between -1.0 and 1.0.
    units="deg",
    fullscr=False
)


left_text = visual.TextStim(win0, text='Left', flipHoriz=True)
left_text.setAutoDraw(True)
right_text = visual.TextStim(win1, text='Right', flipHoriz=True)
right_text.setAutoDraw(True)


win0.close()
win1.close()
win1.close()