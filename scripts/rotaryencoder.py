import numpy as np
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule



class BpodRotaryEncoder():
    def __init__(self, com_port, settings):
        """helper class to deal with rotary encoder module, set thresholds, set and reset position aswell as read prosition

        Args:
            com_port (str): com port (usb) where rotary encoder module is connected to
            settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler      
        """        
        # rotary encoder settings
        self.com_port = com_port
        self.rotary_encoder=RotaryEncoderModule(self.com_port)
        self.RESET_ROTARY_ENCODER = settings.RESET_ROTARY_ENCODER
        self.WRAP_POINT = 0
        # set thresholds
        self.all_thresholds = settings.thresholds
        self.enable_thresholds = [
            (True if x != 0 else False) for x in self.all_thresholds
        ]
        while len(self.enable_thresholds) < 8:
            self.enable_thresholds.append(False)
        self.events = [
            "RotaryEncoder1_{}".format(x)
            for x in list(range(1, len(self.all_thresholds) + 1))
        ]

    def get_events(self):
        return self.events

    def load_message(self, bpod):
        """load reset messag to rotary encoder so bpod can reset rotary encoder position

        Args:
            bpod (Bpod object): 
        """        
        rotary_encoder = [x for x in bpod.modules if x.name == "RotaryEncoder1"][0]
        bpod.load_serial_message(rotary_encoder, self.RESET_ROTARY_ENCODER, [ord('Z'), ord('E')])

    def configure(self):
        """loads rotary enoder module with thresholds
        """        
        self.rotary_encoder.set_thresholds(self.all_thresholds)
        self.rotary_encoder.enable_thresholds(self.enable_thresholds)
        self.rotary_encoder.enable_evt_transmission()
        self.set_wrap_point(self.WRAP_POINT)

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
        # else:
        #     return None

    def set_position_zero(self):
        self.rotray_encoder.set_zero_position()

    def set_wrap_point(self,wrap_point):
        """set the point at which the position is automatically set back to 0 => one half rotation

        Args:
            wrap_point (int): one half rotation wehre set to zero again

        Returns:
            [type]: [description]
        """        
        array = np.array([np.uint8(wrap_point)])
        self.rotary_encoder.arcom.write_array([ord('W')] + array )
        return self.rotary_encoder.arcom.read_uint8() == 1
