
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
import time

ro = RotaryEncoderModule('COM6')
ro.enable_stream()


t_end = time.time() + 20
data_pref = [[0,0,0]]
while time.time() < t_end:
    
    data = ro.read_stream()
    if len(data)==0:
        continue
    else:
        print(data)
        pos_change = data[0][2]-data_pref[0][2]
        print(pos_change)
        data_pref = data
        
        
        

ro.close()