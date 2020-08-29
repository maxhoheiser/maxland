from pybpodapi.bpod_modules.bpod_module import BpodModule


class RotaryEncoder(BpodModule):
    """
    .. note:: This API was based on the `Rotary Encoder board documentation <https://sites.google.com/site/bpoddocumentation/bpod-user-guide/serial-interfaces/rotaryencodermodule>`_.
    """

    COM_TOGGLEOUTPUTSTREAM      = ord('O')
    COM_STOP_STREAMANDLOGGING   = ord('X')
    COM_ENABLE_ALLTHRESHOLDS    = ord('E')
    COM_SETZEROPOS              = ord('Z')
    COM_START_LOGGING           = ord('L')
    COM_STOP_LOGGING            = ord('F')
    COM_TIMESTAMP_BYTE          = ord('#')


    @staticmethod
    def check_module_type(module_name):
        return module_name and module_name.startswith('RotaryEncoder')


    def create_resetpositions_trigger(self):
        """
        Create a trigger to reset the positions and the threshods
        :return: trigger_id
        """
        return self.load_message([ self.COM_SETZEROPOS, self.COM_ENABLE_ALLTHRESHOLDS])


    def activate_outputstream(self):
        """
        Activate module output stream.
        """
        self.write_char_array([self.COM_TOGGLEOUTPUTSTREAM,1])

    def deactivate_outputstream(self):
        """
        Deactivate module output stream.
        """
        self.write_char_array([self.COM_TOGGLEOUTPUTSTREAM,0])

    def stop_streaming_and_logging(self):
        """
        Stops streaming + logging.
        """
        self.write_char_array([self.COM_STOP_STREAMANDLOGGING])

    def enable_positions_threshold(self):
        """
        Enable all position thresholds.
        """
        self.write_char_array([self.COM_ENABLE_ALLTHRESHOLDS])

    def set_position_zero(self):
        """
        Set current rotary encoder position to zero. 
        """
        self.write_char_array([self.COM_SETZEROPOS])

    def starts_logging(self):
        """
        Start logging position+time data to the microSD card. 
        """
        self.write_char_array([self.COM_START_LOGGING])

    def stops_logging(self):
        """
        Finish logging position+time data to the microSD card. 
        """
        self.write_char_array([self.COM_STOP_LOGGING])

    def timestamp_byte(self, value):
        """
        value as to be a byte
        """
        self.write_char_array([self.COM_TIMESTAMP_BYTE, value])