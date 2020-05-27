from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
import numpy as np
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from pybpodapi.com.arcom import ArCOM, ArduinoTypes

from PIL import Image
import time
import pygame
import threading

bpod=Bpod()
trials = 3

#==============================================================================
# rotary encoder config
#==============================================================================
rotary_encoder = [x for x in bpod.modules if x.name == "RotaryEncoder1"][0]
reset_re = 1
bpod.load_serial_message(rotary_encoder, 1, [ord('Z'), ord('E')])
#bpod.load_serial_message(rotary_encoder, 2, [ord("#"), 2])


#====================================
# configure encoder
rotary_encoder=RotaryEncoderModule('COM6')

ALL_THRESHOLDS = [-150, 150, -2, 2]
ENABLE_THRESHOLDS = [True, True, True, True, False, False, False, False]

rotary_encoder.set_zero_position()  # Not necessarily needed
rotary_encoder.set_thresholds(ALL_THRESHOLDS)
rotary_encoder.enable_thresholds(ENABLE_THRESHOLDS)
rotary_encoder.enable_evt_transmission()
rotary_encoder.set_zero_position()

#rotary_encoder.close()


movement_left="RotaryEncoder1_1"
movement_right="RotaryEncoder1_2"
incr_left="RotaryEncoder1_3"
incr_right="RotaryEncoder1_4"


#==============================================================================
# softcode handler
#==============================================================================
def softcode_handler(data):
    if data == 1:
        stimulus_game.present_stimulus()
        print("present stimulus")
    elif data == 2:
        stimulus_game.start_open_loop()
        print("start oppen loop")
    elif data == 3:
        stimulus_game.stop_open_loop()
        print("stop open loop")
    elif data == 4:
        stimulus_game.end_present_stimulus()
        print("end  presentation")

bpod.softcode_handler_function = softcode_handler


# Simple player in pygame


#====================================================================================================================
#pygame
#====================================================================================================================
class py_game():

    def __init__(self):
        self.run_open_loop = True
        self.display_stim_event = threading.Event()
        self.move_stim_event = threading.Event()
        self.still_show_event = threading.Event()
        self.GAIN = 3
        self.THRESHOLD = 2000
        self.FPS=100
        self.SCREEN_WIDTH = 5760
        self.SCREEN_HEIGHT = 1200
        self.screen_dim = [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        self.STIMULUS = r"C:\test\tasks\behavior 01\stimulus.jpg"
        self.surf = pygame.image.load(self.STIMULUS)

    def present_stimulus(self):
        self.display_stim_event.set()

    def start_open_loop(self):
        self.move_stim_event.set()
        #rotary_encoder=RotaryEncoderModule('COM6')
        #rotary_encoder.set_zero_position()
        #rotary_encoder.enable_stream()
        print(f"start_open_loop")

    def stop_open_loop(self):
        self.run_open_loop = False
        #rotary_encoder.disable_stream()
        #rotary_encoder.close()

    def end_present_stimulus(self):
        self.still_show_event.set()

    def exit_trial(self):
        self.display_stim_event.clear()
        self.move_stim_event.clear()
        self.still_show_event.clear()
        self.game = True
        self.run_open_loop = True

    # return x,y coordinates for stim postition
    def stim_center(self):
        stim_dim = (Image.open(self.STIMULUS)).size
        rect = self.surf.get_rect()
        x = ( self.screen_dim[0]/2 - ( stim_dim[0]/2) )
        y = ( self.screen_dim[1]/2 - ( stim_dim[0]/2) )
        return([x, y])


    def run_game(self):
        # pygame config
        pygame.init()
        fpsClock=pygame.time.Clock()
        fpsClock.tick(self.FPS)

        #===========================
        # Set up the drawing window
        pygame.display.init()
        screen = pygame.display.set_mode(self.screen_dim, pygame.FULLSCREEN)
        #DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill((0, 0, 0))

        # Create player
        position = self.stim_center()
        #position = [2580, 300]
        print(f"position initial {position}")
        # create inital stimulus
        screen.blit(self.surf, position)

        #-----------------------------------------------------------------------------
        # on soft code of state 1
        #-----------------------------------------------------------------------------
        # present initial stimulus
        self.display_stim_event.wait()
        pygame.display.flip()

        #=========================
        # py game loop
        # loop is running while open loop active
        #-------------------------------------------------------------------------
        # on soft code of state 2
        #-------------------------------------------------------------------------
        self.move_stim_event.wait()
        #rotary_data = rotary_encoder.read_stream()
        data_pref = [[0,0,0]]
        while self.run_open_loop:
            print(f"position {position}")
            # Fill the background with white
            screen.fill((0, 0, 0))
            screen.blit(self.surf, position)

            # read rotary encoder stream
            self.rotary_position = rotary_encoder.read_stream()
            print(f"position {self.rotary_position}")

            if len(self.rotary_position)==0:
                continue
            else:
                pos_change = abs(self.rotary_position[0][2])-abs(data_pref[0][2])
                #print(f"data-pref: {data_pref[0][2]}  data-now: {data[0][2]} n")
                data_pref = self.rotary_position

                #repositin based on changes
                if self.rotary_position[0][2]<0:
                    #player.move_left(pos_change)
                    position[0] -= (pos_change*self.GAIN)

                if self.rotary_position[0][2]>0:
                    #player.move_right(pos_change)
                    position[0] += (pos_change*self.GAIN)
                # # keep on screen
                # if abs(position[0]) >= stim_threshold:
                #     running = False

            pygame.display.update()
        pos_change = 0
        print(f"pos_change: {pos_change}")
        #position = [2580, 300]
        print(f"position end: {position}")
        #rotary_encoder.disable_stream()

        #show stimulus after closed loop period is over until reward gieven
        self.still_show_event.wait()
        screen.fill((0, 0, 0))
        pygame.display.flip()
        fpsClock.tick(self.FPS)
        pygame.quit()



#===============================================================================================================
# state machine configs
#===============================================================================================================
#reset = rotary_encoder.set_zero_position()
stimulus_game = py_game()

#====================================
# states -> thread 1
def trial():
    # construct pygame objec

    for trial in range(trials):
        #====================================
        # start pygmae threading
        t1 = threading.Thread(target=stimulus_game.run_game)
        t1.start()
        print(f"start {trial}")

        #====================================
        # define states
        sma = StateMachine(bpod)
        # sart state blink green two times
        sma.add_state(
            state_name="start1",
            state_timer=1,
            state_change_conditions={"Tup": "start2"},
            output_actions=[("BNC1", 1), ("BNC2", 1) #blink white + red
                            ],
        )
        sma.add_state(
            state_name="start2",
            state_timer=1,
            state_change_conditions={"Tup": "wheel_not_stopping"},
            output_actions=[("Serial1", 1)],
        ) # necessary to blink light

        #wheel not stoping check
        sma.add_state(
            state_name="wheel_not_stopping",
            state_timer=5,
            state_change_conditions={
                    "Tup":"present_stim",
                    incr_left:"reset_rotary_encoder_wheel_not_stopping",
                    incr_right:"reset_rotary_encoder_wheel_not_stopping",
                    },
            output_actions=[("BNC1", 1)], # activate white light while waiting
        )
        sma.add_state(
            state_name="reset_rotary_encoder_wheel_not_stopping",
            state_timer=0,
            state_change_conditions={"Tup":"start1"},
            output_actions=[("BNC2", 1)], # activate white light while waiting
        )

        # main loop
        sma.add_state(
            state_name="present_stim",
            state_timer=2,
            state_change_conditions={"Tup": "reset_rotary_encoder_open_loop"},
            output_actions=[("SoftCode", 1)],#after wait -> present initial stimulus
        ) # wait for 2 seconds with presented stimulus & wheel not mooving stimulus

        sma.add_state(
            state_name="reset_rotary_encoder_open_loop",
            state_timer=0.5,
            state_change_conditions={"Tup": "activate_open_loop"},
            output_actions=[("Serial1", 1)], # reset rotary encoder postition to 0
        )
        sma.add_state(
            state_name="activate_open_loop",
            state_timer=0.5,
            state_change_conditions={"Tup": "detect"},
            output_actions=[("SoftCode", 2)], # activate open loop
        )
        # open loop detection
        sma.add_state(
            state_name="detect",
            state_timer=0,
            state_change_conditions={
                movement_left: "stop_open_loop",
                movement_right: "stop_open_loop",
                },
            output_actions=[],
        )
        # blink red
        sma.add_state(
            state_name="stop_open_loop",
            state_timer=0,
            state_change_conditions={"Tup": "blink_red_1x"},
            output_actions=[("SoftCode", 3)] # stop open loop in py game
        )
        sma.add_state(
            state_name="blink_red_1x",
            state_timer=2,
            state_change_conditions={"Tup": "reset_rotary_encoder"},
            output_actions=[] # shine red ligh
        )
        # reset rotary encoder to positin 0
        sma.add_state(
            state_name="reset_rotary_encoder",
            state_timer=0,
            state_change_conditions={"Tup": "exit"},
            output_actions=[#("Serial1", 1),
                            ("SoftCode", 4) # remove stimulus presentation
                            ],
        )

        bpod.send_state_machine(sma)
        # Run state machine
        if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
            break
        # end py game & reset
        stimulus_game.exit_trial()
        t1.join()
        print(f"end trial {trial}")
        # end thread1



#==========================================================================================================

t2 = threading.Thread(target=trial)
t2.start()
t2.join()
print("t2 finished")


rotary_encoder.close()
bpod.close()
