from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
import time
import numpy as np
from pybpodgui_plugin_waveplayer.module_api import WavePlayerModule
from pybpodapi.com.arcom import ArCOM, ArduinoTypes




# load wave
waveplayer = WavePlayerModule("COM6")

# configure wave
sampleRate = 1000  # of samples per second 1kHz
wave = np.ones(100000) * 5

waveplayer.set_sampling_period(sampleRate)
waveplayer.set_output_range(0)
#waveplayer.set_loop_mode([False, False, False, False, False, False, False, False])
waveplayer.set_loop_mode([False, False, False, False])
waveplayer.debug()

print(waveplayer.load_waveform(1, wave))

waveplayer.disconnect()


# create bpod object all necessary settings are imported from GUI
bpod = Bpod('COM5')
bpod.modules[0].name
bpod.modules[1].name
bpod.modules[1].


wave_player = [x for x in bpod.modules if x.name == "WavePlayer1"][0]
bpod.load_serial_message(wave_player, 1, [ord('P'), 15, 1])
wave_player.load_message([ord('P'), 15, 1],1)




"""
for _ in range(10):
    print(f"loop:{_}")
    waveplayer.play(1,1)
    waveplayer.play(2,1)
    waveplayer.play(3,1)
    waveplayer.play(4,1)

    time.sleep(5)
    waveplayer.stop()

waveplayer.disconnect()"""


#from pybpodapi.com.arcom import ArCOM, ArduinoTypes

#arcom = ArCOM().open("COM6", 115200)
#arcom.write_array(ArduinoTypes.get_uint8_array([ord("P"), 1, 0]))
#arcom.close()


# trial loop

trials = 10

#LoadSerialMessages('WavePlayer1', ['P', 15, 1])

# main loop for 10 trials
for trial in range(trials):

    # create state machine object
    sma = StateMachine(bpod)

    # initial state, all states follow the same notation
    sma.add_state(
        state_name="start_state",
        state_timer=2,
        state_change_conditions={"Tup": "next_state"},
        output_actions=[('Serial4', 1)],
    )

    # blink state
    sma.add_state(
        state_name="next_state",
        state_timer=2,
        state_change_conditions={"Tup": "end_state"},
        output_actions=[("BNC1", 1), ("BNC2", 1)],
    )

    # start testing for recifing signals
    sma.add_state(
        state_name="end_state",
        state_timer=2,
        state_change_conditions={"Tup": "exit"},
        output_actions=[('Serial4', 1)],
    )

    bpod.send_state_machine(sma)

    if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
        break

    # print some infos about the trial
    print("Current trial info: {0}".format(bpod.session.current_trial))

bpod.close()

"""