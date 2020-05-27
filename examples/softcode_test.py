from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
import numpy as np
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from pybpodapi.com.arcom import ArCOM, ArduinoTypes
import time
import threading

bpod=Bpod()

trials = 10

#==============================================================================
# rotary encoder config
#==============================================================================
rotary_encoder = [x for x in bpod.modules if x.name == "RotaryEncoder1"][0]

reset_re = 1

bpod.load_serial_message(rotary_encoder, 1, [ord('Z'), ord('E')])
bpod.load_serial_message(rotary_encoder, 2, [ord("#"), 2])

#====================================
# onfigure encoder
#====================================
rotary_encoder=RotaryEncoderModule('COM6')

ALL_THRESHOLDS = [-10, 10]
ENABLE_THRESHOLDS = [True, True, False, False, False, False, False, False]

rotary_encoder.set_zero_position()  # Not necessarily needed
rotary_encoder.set_thresholds(ALL_THRESHOLDS)
rotary_encoder.enable_thresholds(ENABLE_THRESHOLDS)
rotary_encoder.enable_evt_transmission()
rotary_encoder.close()

movement_left="RotaryEncoder1_1"
movement_right="RotaryEncoder1_2"


#====================================
# softcode handler
#====================================
def softcode_handler(data):
    global sph
    if data == 0:
        print("soft code = 0")
    elif data == 1:
        message1.update(1)
        print("soft code = 1")
    elif data == 2:
        message1.update(0)
        print("soft code = 2")
bpod.softcode_handler_function = softcode_handler



#====================================
# loop to print rotary encoder position -> thred 0
#====================================
class postion_printer():
    def __init__(self, typ):
        self.typ = typ
        self.run = True
    def print_info(self):
        while self.run:
            if self.typ == 0:
                print(f"waiting")
            if self.typ == 1:
                print(f"KEYBOARD")
    def update(self, new_typ):
        self.typ = new_typ
    def stop(self):
        self.run = False

message1 = printer(0)


#====================================
# states -> thread 1
#====================================
def trial():
    for trial in range(trials):
        # send ttl to bnc1
        sma = StateMachine(bpod)
        # sart state blink green two times
        sma.add_state(
            state_name="start1",
            state_timer=1,
            state_change_conditions={"Tup": "start2"},
            output_actions=[("Serial1", 1), ("SoftCode", 2)],
        )
        sma.add_state(
            state_name="start2",
            state_timer=1,
            state_change_conditions={"Tup": "start3"},
            output_actions=[("BNC1", 1)],
        )
        sma.add_state(
            state_name="start3",
            state_timer=1,
            state_change_conditions={"Tup": "reset_rotary_encoder2"},
            output_actions=[],
        )
        # detect rotary encoder movement left -> blink red light
        sma.add_state(
            state_name="reset_rotary_encoder2",
            state_timer=0,
            state_change_conditions={"Tup": "detect"},
            output_actions=[("Serial1", 1)],
        )
        sma.add_state(
            state_name="detect",
            state_timer=30,
            state_change_conditions={
                movement_left: "blink_red_1x",
                movement_right: "blink_red_1x",
                "Tup": "start1"
                },
            output_actions=[("BNC1", 1)],
        )
        # blink red
        sma.add_state(
            state_name="blink_red_1x",
            state_timer=1,
            state_change_conditions={"Tup": "reset_rotary_encoder"},
            output_actions=[("BNC2", 1), ("Serial1",2 ), ("SoftCode", 1)],
        )
        # reset rotary encoder to positin 0
        sma.add_state(
            state_name="reset_rotary_encoder",
            state_timer=0,
            state_change_conditions={"Tup": "exit"},
            output_actions=[("Serial1", 1)],
        )

        bpod.send_state_machine(sma)
        # Run state machine
        bpod.run_state_machine(sma)
    message1.stop()

t1 = threading.Thread(target=message1.print_info)
t2 = threading.Thread(target=trial)

t1.start()
t2.start()

t1.join()
print("t1 finished")
t2.join()
print("t2 finished")

bpod.close()










#=============================================================================
