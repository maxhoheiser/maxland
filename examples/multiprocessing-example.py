# test multiprocessing


from psychopy import visual, core, monitors
import multiprocessing
from multiprocessing import Process, Event
import threading
import platform
import time
import os, sys


# Psychopy =======================================================================================================================================
# Monitor parameters ====================================================

class psy_test():
    def __init__(self):
        self.run = True

        MON_DISTANCE = 16  # Distance between subject's eyes and monitor
        MON_WIDTH = 20  # Width of your monitor in cm
        MON_SIZE = (2048,1536)  #[1024, 1280]  # Pixel-dimensions of your monitor
        SAVE_FOLDER = 'templateData'  # Log is saved to this folder. The folder is created if it does not exist.

        # create monitor
        self.monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
        self.monitor.setSizePix(MON_SIZE)

        #create a window
        self.win = visual.Window(
            size=(2048, 1536), 
            fullscr=True, 
            screen=1, 
            monitor=self.monitor,
            winType='pyglet', allowGUI=False, allowStencil=False,
            color=[-1,-1,-1], colorSpace='rgb',
            blendMode='avg', useFBO=True, 
            units='height')
        self.win.winHandle.maximize() # fix black bar bottom

        # get frame rate of monitor
        expInfo = {}
        expInfo['frameRate'] = self.win.getActualFrameRate()
        if expInfo['frameRate'] != None:
            frameDur = 1.0 / round(expInfo['frameRate'])
        else:
            frameDur = 1.0 / 60.0  # could not measure, so guess


        # Grating Stimuli ========================================================
        # Stimulus parameters
        grating_SF = 0.25  # 4 cycles per degree visual angle
        grating_SIZE = 45  # depending on canfaz measure type - no in screen hight
        grating_ori = 0   # in degree

        self.grating_left = visual.GratingStim(
            win=self.win,
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
        self.grating_left.draw()
        self.win.flip()


    def psychopy_loop(self):
        timeout = time.time()+10
        while self.run: 
            # dram moving gratings
            self.grating_left.setPhase(0.05, '+')#advance phase by 0.05 of a cycle
            self.grating_left.draw()
            self.win.flip()
            #sys.stdout.flush()
            #event.clearEvents()
            if time.time() > timeout:
                break
        


def info(title):
    print(title)
    #print('module name:', __name__)
    #print('parent process:', os.getppid())
    #print('process id:', os.getpid())

def test_loop():
    time.sleep(1)
    #sys.stdout = open(str(os.getpid()) + ".out", "a")
    #sys.stderr = open(str(os.getpid()) + "_error.out", "a")
    #info('function f')
    print(time.time())
    sys.stdout.flush()


# Main Loop ==============================================================================

# span subprocess
if platform.system() == "Darwin":
        multiprocessing.set_start_method('span')

psy = psy_test()
#psy.psychopy_loop()
pa = Process(target=test_loop)#psychopy_loop)
pa.start()

pa = Process(target=psy.psychopy_loop)#psychopy_loop)
pa.start()

#psy.psychopy_loop()

pa.join()

#psychopy_loop()






"""
game_trhead = threading.Thread(target=psychopy_loop, daemon=True)
#game_trhead.start()

timeout = time.time()+23
while True:
    print(time.time())
    if time.time() > timeout:
        break
"""

