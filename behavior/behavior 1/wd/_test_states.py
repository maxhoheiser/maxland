# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import settings
from probability import ProbabilityConstuctor



STIM_POSITIONS = [-35, 35]  # All possible positions (deg)
QUIESCENCE_THRESHOLDS = [-2, 2]  # degree
ALL_THRESHOLDS = STIM_POSITIONS + QUIESCENCE_THRESHOLDS


STIM_GAIN = 4.0


#movement_left = threshold_events_dict[sph.QUIESCENCE_THRESHOLDS[0]]
#movement_right = threshold_events_dict[sph.QUIESCENCE_THRESHOLDS[1]]

#=============================================================================
WHEEL_PERIM = 31 * 2 * np.pi  # = 194,778744523
mm_deg = WHEEL_PERIM / 360
factor = 1 / (mm_deg * STIM_GAIN)

SET_THRESHOLDS = [x * factor for x in ALL_THRESHOLDS]
ENABLE_THRESHOLDS = [
            (True if x != 0 else False) for x in SET_THRESHOLDS
        ]
while len(ENABLE_THRESHOLDS) < 8:
            ENABLE_THRESHOLDS.append(False)
            

ENCODER_EVENTS = [
            "RotaryEncoder1_{}".format(x)
            for x in list(range(1, len(ALL_THRESHOLDS) + 1))
        ]

THRESHOLD_EVENTS = dict(zip(ALL_THRESHOLDS, ENCODER_EVENTS))