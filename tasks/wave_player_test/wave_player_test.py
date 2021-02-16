from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine

import math, wave, array, struct, numpy as np
from pybpodgui_plugin_waveplayer.module_api import WavePlayerModule


# create bpod object all necessary settings are imported from GUI
# bpod = Bpod()


# configure wave
sampleRate = 1000  # of samples per second 1kHz
wave = np.ones(1000) * 5

# load wave
waveplayer = WavePlayerModule("COM5")

waveplayer.set_sampling_period(sampleRate)
waveplayer.set_output_range(5)
waveplayer.set_loop_mode([False, False, False, False, False, False, False, False])
waveplayer.debug()

(waveplayer.load_waveform(0, wave))


waveplayer.play(1, 0)
waveplayer.stop()


waveplayer.disconnect()


from pybpodapi.com.arcom import ArCOM, ArduinoTypes

arcom = ArCOM().open("COM5", 115200)
arcom.write_array(ArduinoTypes.get_uint8_array([ord("P"), 1, 0]))


# generate wav file containing sine waves
# FB36 - 20120617
import math, wave, array, struct, numpy as np
from pybpodgui_plugin_waveplayer.module_api import WavePlayerModule

amplitude = 3.0
duration = 3  # seconds
freq = 1000  # of cycles per second (Hz) (frequency of the sine waves)
volume = 100  # percent
sampleRate = 96000  # of samples per second (standard)
numChan = 1  # of channels (1: mono, 2: stereo)
dataSize = 2  # 2 bytes because of using signed short integers => bit depth = 16


samples = np.arange(0, duration, 1 / sampleRate)
wave = amplitude * np.sin(2 * math.pi * freq * samples)


"""
data = array.array('h') # signed short integer (-32768 to 32767) data
numSamplesPerCyc = int(sampleRate / freq)
numSamples = sampleRate * duration
for i in range(numSamples):
    
    sample = 32767 * float(volume) / 100
    sample *= math.sin(math.pi * 2 * (i % numSamplesPerCyc) / numSamplesPerCyc)
    data.append(int(sample))
"""

m = WavePlayerModule("/dev/ttyACM0")

print(m.set_sampling_period(sampleRate))
m.set_output_range(m.RANGE_VOLTS_MINUS5_5)
m.set_loop_mode([False, False, False, False])
m.debug()

print(m.load_waveform(0, wave))

print(m.play(1, 0))


"""
# trial loop

trials = 10



# main loop for 10 trials
for trial in range(trials):


    # create state machine object
    sma = StateMachine(bpod)


    # initial state, all states follow the same notation
    sma.add_state(
        # sate nemae can be freely chosen but must be unique
        state_name="start_state",
        # time how long the state is active can be 0 or seconds or fractions of seconds
        # if 0 state will only change if state change condition is met
        state_timer=2,
        # state change condition for switching to respective next state
        # hast to be a dictionary with keys from allowed conditions and values
        state_change_conditions={"Tup": "next_state"},
        # output actions can be none or list of touples with allowed names and values
        output_actions=[("BNC1", 1), ("BNC2", 1)],
    )

    # blink state
    sma.add_state(
        state_name="next_state",
        state_timer=2,
        state_change_conditions={"Tup": "end_state"},
        output_actions=[("BNC1", 0), ("BNC2", 0)],
    )

    # start testing for recifing signals
    sma.add_state(
        state_name="end_state",
        state_timer=0,
        # last state always next state to exit
        # state change condition must follow allowed names
        state_change_conditions={"Tup": "exit"},
        output_actions=[("BNC1", 1)],
    )

    # Send state machine description to Bpod device
    # as soone as the state machine object is transmitted the states are run
    bpod.send_state_machine(sma)

    # wait until state machine has finished
    if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
        break

    # print some infos about the trial
    print("Current trial info: {0}".format(bpod.session.current_trial))

bpod.close()

"""