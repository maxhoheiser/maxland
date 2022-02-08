import threading
import os,sys,inspect
import json
import random
import time


# import pybpod modules
from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpodgui_api.models.session import Session

trials = 10

# create settings object
settings_obj = object
settings_obj.RESET_ROTARY_ENCODER = 1
settings_obj.thresholds = [-90,90,-1,1]
settings_obj.WHEEL_DIAMETER = 6.3
settings_obj.RESET_ROTARY_ENCODER = 1
settings_obj.THRESH_LEFT = "RotaryEncoder1_4"
settings_obj.THRESH_RIGHT = "RotaryEncoder1_3"
settings_obj.THRESH_RIGHT = "RotaryEncoder1_3"
settings_obj.STIMULUS_LEFT = "RotaryEncoder1_2"
settings_obj.STIMULUS_RIGHT = "RotaryEncoder1_1"
settings_obj.THRESH_RIGHT = "RotaryEncoder1_3"

# import custom modules
from ../modules/rotaryencoder import BpodRotaryEncoder
from ../modules/helperfunctions import find_rotary_com_port, tryer

# Main test for Mpod state machine test 
bpod=Bpod()

# state machine configs
for trial in range(trials):

    com_port = find_rotary_com_port()
    #com_port = '/dev/cu.usbmodem65305701' #TODO:
    rotary_encoder_module = BpodRotaryEncoder(com_port, settings_obj, bpod)
    rotary_encoder_module.load_message()
    rotary_encoder_module.configure()

    sma = StateMachine(bpod)
    # start state to define block of trial
    sma.add_state(
        state_name="start",
        state_timer=0,
        state_change_conditions={"Tup": "reset_rotary_encoder_wheel_stopping_check"},
        output_actions=[]
    )

    # reset rotary encoder bevore checking for wheel not stoping
    sma.add_state(
        state_name="reset_rotary_encoder_wheel_stopping_check",
        state_timer=0,
        state_change_conditions={"Tup": "open_loop"},
        output_actions=[("Serial1", settings_obj.RESET_ROTARY_ENCODER)], # activate white light while waiting
    )

    # open loop detection
    sma.add_state(
        state_name="open_loop",
        state_timer=5,
        state_change_conditions={
            "Tup": "stop_open_loop_fail",
            settings_obj.STIMULUS_LEFT: "stop_open_loop_left",
            settings_obj.STIMULUS_RIGHT: "stop_open_loop_right",
            },
        output_actions=[], # softcode to start open loop
    )

    # stop open loop fail
    sma.add_state(
        state_name="stop_open_loop_fail",
        state_timer=0,
        state_change_conditions={"Tup": "end"},
        output_actions=[] # stop open loop in py game
    )
    # reward left
    sma.add_state(
        state_name="stop_open_loop_left",
        state_timer=0,
        state_change_conditions={"Tup": "end"},
        output_actions=[] # stop open loop in py game
    )
    # reward right
    sma.add_state(
        state_name="stop_open_loop_right",
        state_timer=0,
        state_change_conditions={"Tup": "end"},
        output_actions=[] # stop open loop in py game
    )

    # end state
    sma.add_state(
        state_name="END",
        state_timer=0,
        state_change_conditions={"Tup":"exit"},
        output_actions=[],
    )

    # send & run state machine
    bpod.send_state_machine(sma)
    if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
        break
    print("Current trial info: {0}".format(bpod.session.current_trial))

    

tryer(rotary_encoder_module.close())()
