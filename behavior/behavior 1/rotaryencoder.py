"""
Rotary Encoder Config
"""

class BpodRotaryEncoder():
    def __init__(self, bpod, com_port, settings):
    # rotary encoder settings
    self.com_port = com_port
    self.settigns = settings
    # softcode handler

    def load_message(self, bpod):
        "load reset messag to rotary encoder so bpod can reset rotary encoder position"
        rotary_encoder = [x for x in bpod.modules if x.name == "RotaryEncoder1"][0]
        bpod.load_serial_message(rotary_encoder, self.settings.RESET_ROTARY_ENCODER, [ord('Z'), ord('E')])
        #bpod.load_serial_message(rotary_encoder, 2, [ord("#"), 2])

    def config_rotary_encoder(self):
        "loads rotary enoder module with thresholds"
        self.rotary_encoder=RotaryEncoderModule(self.com_port)

        self.rotary_encoder.set_thresholds(self.settings.ALL_THRESHOLDS)
        self.rotary_encoder.enable_thresholds(self.settings.ENABLE_THRESHOLDS)
        self.rotary_encoder.enable_evt_transmission()
        return rotary_encoder
