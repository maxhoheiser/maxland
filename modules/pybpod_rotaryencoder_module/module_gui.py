import pyforms
import serial
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlCheckBox, ControlNumber, ControlButton, ControlCombo
from pyforms.controls import ControlMatplotlib
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from sca.formats import csv
from datetime import datetime as datetime_now
from confapp import conf

from AnyQt import QtGui
from AnyQt.QtCore import QTimer
from AnyQt.QtWidgets import QFileDialog


class RotaryEncoderModuleGUI(RotaryEncoderModule, BaseWidget):

    TITLE = 'Rotary encoder module'

    def __init__(self, parent_win=None):
        BaseWidget.__init__(self, self.TITLE, parent_win=parent_win)
        RotaryEncoderModule.__init__(self)

        self._port = ControlCombo('Serial port', changed_event=self.__combo_serial_ports_changed_evt)
        self._refresh_serial_ports = ControlButton('',
                                                   icon=QtGui.QIcon(conf.REFRESH_SMALL_ICON),
                                                   default=self.__refresh_serial_ports_btn_pressed,
                                                   helptext="Press here to refresh the list of available devices.")

        self._connect_btn   = ControlButton('Connect', checkable=True)

        self._filename 		= ControlText('Stream Filename', '')
        self._saveas_btn    = ControlButton('Save As...')

        self._events 		= ControlCheckBox('Enable events')
        self._output_stream	= ControlCheckBox('Output stream')
        self._stream 		= ControlCheckBox('Stream data')
        self._stream_file   = ControlCheckBox('Stream to file')
        self._zero_btn 		= ControlButton('Reset position')
        self._start_reading = ControlButton('Start Reading')
        self._reset_threshs = ControlButton('Reset thresholds')
        self._thresh_lower 	= ControlNumber('Lower threshold (deg)', 0, minimum=-360, maximum=360)
        self._thresh_upper 	= ControlNumber('Upper threshold (deg)', 0, minimum=-360, maximum=360)
        self._graph 		= ControlMatplotlib('Value')
        self._clear_btn 	= ControlButton('Clear')

        self.set_margin(10)

        self.formset = [
            ('_port', '_refresh_serial_ports', '_connect_btn'),
            ('_filename', '_saveas_btn'),
            ('_events', '_output_stream', '_stream', '_stream_file', '_zero_btn'),
            '_start_reading',
            ('_thresh_lower', '_thresh_upper', '_reset_threshs'),
            '=',
            '_graph',
            '_clear_btn'
        ]

        self._stream.enabled = False
        self._stream_file.enabled = False
        self._events.enabled = False
        self._output_stream.enabled = False
        self._zero_btn.enabled = False
        self._reset_threshs.enabled = False
        self._thresh_lower.enabled = False
        self._thresh_upper.enabled = False
        self._start_reading.enabled = False

        self._connect_btn.value = self.__toggle_connection_evt
        self._saveas_btn.value = self.__prompt_savig_evt
        self._stream_file.changed_event = self.__stream_file_changed_evt
        self._events.changed_event = self.__events_changed_evt
        self._output_stream.changed_event = self.__output_stream_changed_evt
        self._thresh_upper.changed_event = self.__thresh_evt
        self._thresh_lower.changed_event = self.__thresh_evt
        self._reset_threshs.value = self.__reset_thresholds_evt
        self._zero_btn.value = self.__zero_btn_evt
        self._start_reading.value = self.__start_reading_evt
        self._graph.on_draw = self.__on_draw_evt
        self._clear_btn.value = self.__clear_btn_evt
        self._filename.changed_event = self.__filename_changed_evt

        self.history_x = []
        self.history_y = []

        self._timer = QTimer()
        self._timer.timeout.connect(self.__update_readings)

        self._fill_serial_ports()

    def _fill_serial_ports(self):
        self._port.add_item('', '')
        for n, port in enumerate(sorted(serial.tools.list_ports.comports()), 1):
            self._port.add_item("{device}".format(device=port.device), str(port.device))

    def __filename_changed_evt(self):
        if not self._filename.value:
            self._stream_file.value = False
            self._stream_file.enabled = False

    def __prompt_savig_evt(self):
        '''
        Opens a window for user to select where to save the csv file
        '''
        self._filename.value, _ = QFileDialog.getSaveFileName()
        if self._filename.value:
            self._stream_file.enabled = True
        else:
            self._stream_file.value = False
            self._stream_file.enabled = False

    def __stream_file_changed_evt(self):
        '''
        User wants to store rotary encoder measurements in a CSV file. Create it
        '''
        if self._stream_file.value is True:
            self._csvfile = open(self._filename.value, 'w')
            self._csvwriter = csv.writer(
                self._csvfile,
                def_text='This file has all the rotary encoder data recorded during a PyBpod session.',
                columns_headers=['PC_TIME', 'DATA_TYPE','EVT_TIME', 'VALUE'])  # Check if we need something else after

    def __start_reading_evt(self):
        '''
        Toggle timer
        '''
        if self._timer.isActive():
            self.disable_stream()
            self._start_reading.label = 'Start Reading'
            self._timer.stop()
        else:
            self.enable_stream()
            self.history_x = []
            self.history_y = []
            self._start_reading.label = 'Stop Reading'
            self._timer.start(30)

    def __clear_btn_evt(self):
        '''
        Clear recorded data
        '''
        self.history_x = []
        self.history_y = []
        self._graph.draw()

    def __on_draw_evt(self, figure):
        '''
        The actual draw function. Pick just the last 200 measurements in order to avoid app freezing
        '''
        axes = figure.add_subplot(111)
        axes.clear()
        totallen = len(self.history_x)
        if totallen > 200:
            x = self.history_x[totallen - 201:]
            y = self.history_y[totallen - 201:]
            axes.plot(x,y)
            if len(x)>=2:
                x_range = [x[0],x[-1]]
                axes.plot(x_range, [self._thresh_upper.value, self._thresh_upper.value], linestyle='dotted', color='red')
                axes.plot(x_range, [self._thresh_lower.value, self._thresh_lower.value], linestyle='dotted', color='blue')
        else:
            axes.plot(self.history_x, self.history_y)
            if len(self.history_x) >= 2:
                x_range = [self.history_x[0], self.history_x[-1]]
                axes.plot(x_range, [self._thresh_upper.value, self._thresh_upper.value], linestyle='dotted', color='red')
                axes.plot(x_range, [self._thresh_lower.value, self._thresh_lower.value], linestyle='dotted', color='blue')

        self._graph.repaint()

    def __update_graph(self, readings):
        '''
        Add new data to the reading history and update the graph
        '''
        for data in readings:
            if data[0] == 'P':
                self.history_x.append(data[1])
                self.history_y.append(data[2])
        self._graph.draw()

    def __update_readings(self):
        '''
        Get new measurements and channel them to the graph or the file being written
        '''
        data = self.read_stream()

        if self._stream.value:
            self.__update_graph(data)
        if self._stream_file.value:
            self.__write_to_file(data)

    def __write_to_file(self, readings):
        '''
        Write new readings to the file
        '''
        now = datetime_now.now()
        for data in readings:
            self._csvwriter.writerow([now.strftime('%Y%m%d%H%M%S')]+data)

    def __zero_btn_evt(self):
        self.set_zero_position()

    def __reset_thresholds_evt(self):
        self._thresh_lower.value = 0
        self._thresh_upper.value = 0

    def __thresh_evt(self):
        thresholds = [int(self._thresh_lower.value), int(self._thresh_upper.value)]	
        self.set_thresholds(thresholds)

    def __events_changed_evt(self):
        if self._stream.value:
            self.enable_evt_transmission()
        else:
            self.disable_evt_transmission()

    def __output_stream_changed_evt(self):
        if self._stream.value:
            self.enable_module_outputstream()
        else:
            self.disable_module_outputstream()

    def __toggle_connection_evt(self):
        if not self._connect_btn.checked:
            if hasattr(self, 'arcom'):
                self.disable_stream()
                self._timer.stop()
                self.close()
            self._connect_btn.label = 'Connect'
            self._stream.enabled = False
            self._events.enabled = False
            self._output_stream.enabled = False
            self._zero_btn.enabled = False
            self._reset_threshs.enabled = False
            self._thresh_lower.enabled = False
            self._thresh_upper.enabled = False
            self._start_reading.enabled = False
            self._stream_file.enabled = False

            self._port.enabled = True
            self._refresh_serial_ports.enabled = True
        else:
            try:
                self.open(self._port.value)

                self._connect_btn.label = 'Disconnect'
                self._stream.enabled = True
                self._events.enabled = True
                self._output_stream.enabled = True
                self._zero_btn.enabled = True
                self._reset_threshs.enabled = True
                self._thresh_lower.enabled = True
                self._thresh_upper.enabled = True
                self._start_reading.enabled = True

                self._port.enabled = False
                self._refresh_serial_ports.enabled = False

                if self._filename.value:
                    self._stream_file.enabled = True
                else:
                    self._stream_file.value = False
                    self._stream_file.enabled = False
            except Exception as err:
                self.critical(str(err),  "Error")
                self._connect_btn.checked = False

    def __combo_serial_ports_changed_evt(self):
        self._connect_btn.enabled = True

    def __refresh_serial_ports_btn_pressed(self):
        tmp = self._port.value
        self._port.clear()
        self._fill_serial_ports()
        self._port.value = tmp


if __name__ == '__main__':
    pyforms.start_app(RotaryEncoderModuleGUI, geometry=(0, 0, 600, 500))
