import numpy as np
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule

"""
Rotary Encoder Config
"""

class BpodRotaryEncoder():
    def __init__(self, com_port, all_thresholds, wheel_diameter):
        # rotary encoder settings
        self.com_port = com_port
        self.WRAP_POINT = 0
        # configure wheel
        self.wheel_circumference = wheel_diameter * np.pi
        self.mm_deg = self.wheel_circumference / 360
        self.factor = 1 / (self.mm_deg)
        self.all_thresholds = [x * self.factor for x in all_thresholds]
        self.enable_thresholds = [
            (True if x != 0 else False) for x in self.all_thresholds
        ]
        while len(self.enable_thresholds) < 8:
            self.enable_thresholds.append(False)
        self.events = [
            "RotaryEncoder1_{}".format(x)
            for x in list(range(1, len(all_thresholds) + 1))
        ]

    def get_events(self):
        return self.events

    def load_message(self, bpod):
        "load reset messag to rotary encoder so bpod can reset rotary encoder position"
        rotary_encoder = [x for x in bpod.modules if x.name == "RotaryEncoder1"][0]
        bpod.load_serial_message(rotary_encoder, self.settings.RESET_ROTARY_ENCODER, [ord('Z'), ord('E')])

    def configure(self):
        "loads rotary enoder module with thresholds"
        self.rotary_encoder=RotaryEncoderModule(self.com_port)
        self.rotary_encoder.set_thresholds(self.all_thresholds)
        self.rotary_encoder.enable_thresholds(self.enable_thresholds)
        self.rotary_encoder.enable_evt_transmission()
        self.rotary_encoder.enable_stream()
        self.set_wrap_point(self.WRAP_POINT)
        return self.rotary_encoder

    def close(self):
        self.rotary_encoder.close()

    def read_stream(self):
        return self.rotary_encoder.read_stream()

    def current_position(self):
        return self.rotary_encoder.current_position()

    def set_wrap_point(self,wrap_point):
        array = np.array([np.uint8(wrap_point)])
        self.rotary_encoder.arcom.write_array([ord('W')] + array )
        return self.rotary_encoder.arcom.read_uint8() == 1
