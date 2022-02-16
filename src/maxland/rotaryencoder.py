import numpy as np
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule

WRAP_POINT = 0


class BpodRotaryEncoder:
    """helper class to deal with rotary encoder module, set thresholds, set and reset position as well as read prosition
    Args:
        com_port (str): com port (usb) where rotary encoder module is connected to
        settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler
    """

    def __init__(self, com_port, settings, bpod):
        self.com_port = com_port
        self.rotary_encoder = RotaryEncoderModule(self.com_port)
        self.bpod = bpod
        self.reset = settings.reset_rotary_encoder
        self.wrap_point = WRAP_POINT
        self.all_thresholds = settings.thresholds
        self.enabled_thresholds = self.get_enabled_thresholds(self.all_thresholds)
        self.events = self.get_events(self.all_thresholds)
        self.set_bit_message()
        self.set_configuration()

    def get_enabled_thresholds(self, all_thresholds):
        enable_thresholds = [(True if x != 0 else False) for x in all_thresholds]
        while len(enable_thresholds) < 8:
            enable_thresholds.append(False)
        return enable_thresholds

    def get_events(self, thresholds):
        events = [f"RotaryEncoder1_{x}" for x in list(range(1, len(thresholds) + 1))]
        return events

    def set_bit_message(self):
        rotary_encoder = [x for x in self.bpod.modules if x.name == "RotaryEncoder1"][0]
        self.bpod.load_serial_message(rotary_encoder, self.reset, [ord("Z"), ord("E")])

    def set_configuration(self):
        """loads rotary encoder module with thresholds"""
        self.rotary_encoder.set_thresholds(self.all_thresholds)
        self.rotary_encoder.enable_thresholds(self.enabled_thresholds)
        self.rotary_encoder.enable_evt_transmission()
        self.set_wrap_point(self.wrap_point)

    def close(self):
        self.rotary_encoder.close()

    def enable_stream(self):
        self.rotary_encoder.enable_stream()

    def disable_stream(self):
        self.rotary_encoder.disable_stream()

    def read_stream(self):
        return self.rotary_encoder.read_stream()

    def read_position(self):
        position = self.rotary_encoder.read_stream()
        if len(position) != 0:
            return position[0][2]

    def enable_logging(self):
        self.rotary_encoder.enable_logging()

    def disable_logging(self):
        self.rotary_encoder.disable_logging()

    def get_logging(self):
        return self.rotary_encoder.get_logged_data()

    def set_zero_position(self):
        self.rotary_encoder.set_zero_position()

    def set_wrap_point(self, wrap_point):
        """
        set the point at which the position is automatically set back to 0 => one half rotation
        Args: wrap_point (int): one half rotation wehre set to zero again
        Returns: [type]: [description]
        """
        array = np.array([np.uint8(wrap_point)])
        self.rotary_encoder.arcom.write_array([ord("W")] + array)
        return self.rotary_encoder.arcom.read_uint8() == 1
