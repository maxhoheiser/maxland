# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:12:55 2020

@author: User
"""
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from stimulus import Stimulus
from rotaryencoder import BpodRotaryEncoder
import numpy as np
import matplotlib.pyplot as plt

import settings

import threading
import time

rotary_encoder = BpodRotaryEncoder("COM4", settings.ALL_THRESHOLDS, settings.WHEEL_DIAMETER)
rotary_encoder.configure()

#==============================================
# manual

# rotary_encoder=RotaryEncoderModule('COM4')

# ALL_THRESHOLDS = [-10, 10]
# ENABLE_THRESHOLDS = [True, True, False, False, False, False, False, False]

# rotary_encoder.set_zero_position()  # Not necessarily needed
# #rotary_encoder.set_thresholds(ALL_THRESHOLDS)
# #rotary_encoder.enable_thresholds(ENABLE_THRESHOLDS)
# #rotary_encoder.enable_evt_transmission()
# rotary_encoder.enable_stream()
# rotary_encoder.set_zero_position()


# wrap_pt = 180
# array = np.array([np.uint8(wrap_pt)])
# rotary_encoder.arcom.write_array([ord('W')] + array )
# rotary_encoder.arcom.read_uint8() == 1
last_pos = 0
position_list = [0]
rotary_encoder.set_position_zero()
rotary_encoder.enable_stream()

while True:
    string = []
    # data = rotary_encoder.read_stream()
    # pos_data.append(data)
    # # if len(data)!=0:
    # #     pos_data.append(data)
    string.append(last_pos)
    current_pos = rotary_encoder.read_position()
    if current_pos == 0:
        continue
    else:
        position = current_pos
        print(position)
        position_list.append(position)
        # string.append(current_pos)
        # position = int(last_pos - current_pos)
        # string.append(position)
        # print(position)
        # #position_list.append(position)
        # last_pos = current_pos
        # position_list.append(string)


plt.plot( [x for x in range(len(position_list))], position_list, marker='', color='olive', linewidth=2)

rotary_encoder.close()



gain = 3
gain = lambda gain: 1 if gain <= 1 else gain