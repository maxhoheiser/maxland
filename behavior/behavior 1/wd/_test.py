# -*- coding: utf-8 -*-
"""
Created on Fri May 29 18:43:37 2020

@author: User
"""

from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
import time
import numpy as np

ro = RotaryEncoderModule('COM4')
ro.enable_stream()

wrap_pt = 0
array = np.array([np.uint8(wrap_pt)])
ro.arcom.write_array([ord('W')] + array )
ro.arcom.read_uint8() == 1

t_end = time.time() + 20
while time.time() < t_end:
    
    data = ro.read_stream()
    if len(data)==0:
        continue
    else:
        print(data)

position = []        
# while time.time() < t_end:
    
#     data = ro.current_position()
#     if data==0:
#         continue
#     else:
#         position.append(data)
        
        

ro.close()