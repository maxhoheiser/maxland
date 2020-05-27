from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
import numpy as np
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from pybpodapi.com.arcom import ArCOM, ArduinoTypes

bpod=Bpod()
trials = 10

#==============================================================================
# rotary encoder config
#==============================================================================
rotary_encoder = [x for x in bpod.modules if x.name == "RotaryEncoder1"][0]
reset_re = 1
bpod.load_serial_message(rotary_encoder, 1, [ord('Z'), ord('E')])

#====================================
# configure encoder
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

#==============================================================================
# state machine configs
#==============================================================================
#reset = rotary_encoder.set_zero_position()

#====================================
# states
#====================================
for trial in range(trials):
    # send ttl to bnc1
    sma = StateMachine(bpod)

# sart state blink green two times
    sma.add_state(
        state_name="start1",
        state_timer=1,
        state_change_conditions={"Tup": "start2"},
        output_actions=[("Serial1", 1)],
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
        state_change_conditions={"Tup": "detect"},
        output_actions=[],
    )

# detect rotary encoder movement left -> blink red light
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

#==============================================================================
# blink red
    sma.add_state(
        state_name="blink_red_1x",
        state_timer=1,
        state_change_conditions={"Tup": "reset_rotary_encoder"},
        output_actions=[("BNC2", 1)],
    )

#==============================================================================
# reset rotary encoder to positin 0
    sma.add_state(
        state_name="reset_rotary_encoder",
        state_timer=0,
        state_change_conditions={"Tup": "exit"},
        output_actions=[("Serial1", 1)],
    )
    bpod.send_state_machine(sma)

    # Run state machine
    if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
        break
    print("test ob das geprintet wird\n")
    print("Current trial info: {0}".format(bpod.session.current_trial))

bpod.close()
if __name__ == "__main__":
    print("main")

#=============================================================================
bpod.close()
