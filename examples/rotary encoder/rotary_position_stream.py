
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
import time

ro = RotaryEncoderModule('COM6')
ro.enable_stream()
ro.set_zero_position()

pos_li = []
pos_change_li = []

t_end = time.time() + 20
data_pref = [[0, 0, 0]]

# test with read hole stream
while time.time() < t_end:
    data = ro.read_stream()
    if len(data) == 0:
        continue
    else:
        pos_li.append(data)
        pos_change = data[0][2]-data_pref[0][2]
        data_pref = data
        pos_change_li.append(pos_change)


"""
# test with read only current position
while time.time() < t_end:
    pos = ro.current_position()
    if len(data)==0:
        continue
    else:
        pos_li.append(pos)
        #pos_change = data[0][2]-data_pref[0][2]
        pos_pref = pos
        #pos_change_li.append(pos_change)
"""


ro.disable_stream()
ro.close()
