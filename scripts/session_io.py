# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import shutil

import pandas as pd

from pybpodapi.com.messaging.session_info import SessionInfo
from pybpodapi.session import Session
from pybpodgui_api.com.messaging.parser import BpodMessageParser
from pybpodgui_api.models.session.session_base import SessionBase
from sca.formats import csv

from pybpodapi.utils import date_parser

logger = logging.getLogger(__name__)


class SessionIO(SessionBase):
    """

    """

    def __init__(self, setup):
        super(SessionIO, self).__init__(setup)

        # initial name. Used to track if the name was updated
        self.initial_name = None

    ##########################################################################
    ####### FUNCTIONS ########################################################
    ##########################################################################

    def collect_data(self, data):
        data.update({'name': self.name})
        data.update({'uuid4': self.uuid4})
        data.update({'started': str(self.started.strftime('%Y%m%d-%H%M%S')) if self.started else None})
        data.update({'ended': str(self.ended.strftime('%Y%m%d-%H%M%S')) if self.ended else None})
        data.update({'setup': str(self.setup.uuid4)})
        data.update({'task': str(self.task.uuid4 if self.task else None)})
        data.update({'board': str(self.setup.board.uuid4 if self.setup.board else None)})
        data.update({'serial_port': self.setup.board.serial_port})

        data.update({'subjects': []})
        for subject in self.subjects:
            data['subjects'].append(subject)

        data.update({'variables': []})
        for var in self.variables:
            data['variables'].append(var)

        return data

    def save(self):
        """

        :param parent_path:
        :return:
        """
        if not self.name:
            logger.warning("Skipping session without name")
        else:
            if self.initial_name is not None:
                initial_path = os.path.join(self.setup.path, 'sessions', self.initial_name)

                if initial_path != self.path:
                    shutil.move(initial_path, self.path)
                    current_filepath = os.path.join(self.path, self.initial_name+'.csv')
                    future_filepath = os.path.join(self.path, self.name+'.csv')
                    shutil.move(current_filepath, future_filepath)

            self.initial_name = self.name

    def load(self, path):
        """

        :param session_path:
        :param data:
        :return:
        """
        self.name = os.path.basename(path)
        # only set the filepath if it exists
        filepath = os.path.join(self.path, self.name+'.csv')

        if not os.path.exists(filepath):
            return

        try:
            self.filepath = filepath
            csvreader = self.load_info()
            self.uuid4 = csvreader.uuid4
        except FileNotFoundError:
            logger.warning('File not found: '+filepath)
            self.filepath = None

    def load_contents(self, init_func=None, update_func=None, end_func=None):
        """
        Parses session history file, line by line and populates the history message on memory.
        """
        if not self.filepath:
            return

        nrows = csv.reader.count_metadata_rows(self.filepath)
        #print(f"\n\n{self.filepath}\n\n")
        self.data = pd.read_csv(self.filepath,
                                delimiter=csv.CSV_DELIMITER,
                                quotechar=csv.CSV_QUOTECHAR,
                                quoting=csv.CSV_QUOTING,
                                lineterminator=csv.CSV_LINETERMINATOR,
                                skiprows=nrows,
                                memory_map=True
                                )
        

        res = self.data.query("MSG=='{0}'".format(Session.INFO_SESSION_ENDED))
        for index, row in res.iterrows():
            self.ended = date_parser.parse(row['+INFO'])

        res = self.data.query("TYPE in ['VAL', 'TRIAL'] or MSG=='SESSION-ENDED'")
        variables = []
        for index, row in res.iterrows():
            if row['TYPE'] == 'TRIAL':
                variables.append(['New trial', None])
            elif row['MSG'] == 'SESSION-ENDED':
                variables.append(['Session ended', None])
            else:
                variables.append([row['MSG'], row['+INFO']])
        #self.variables = variables

    def load_info(self):
        if not self.filepath:
            return

        with open(self.filepath) as filestream:
            csvreader = csv.reader(filestream)
            self.subjects = []

            count = 0
            for row in csvreader:
                msg = BpodMessageParser.fromlist(row)

                if msg:
                    if isinstance(msg, SessionInfo):
                        if msg.infoname == Session.INFO_SESSION_NAME:
                            self.task_name = msg.infovalue

                        elif msg.infoname == Session.INFO_CREATOR_NAME:
                            self.creator = msg.infovalue

                        elif msg.infoname == Session.INFO_SESSION_STARTED:
                            self.started = date_parser.parse(msg.infovalue)

                        elif msg.infoname == Session.INFO_SESSION_ENDED:
                            self.ended = date_parser.parse(msg.infovalue)

                        elif msg.infoname == Session.INFO_SERIAL_PORT:
                            self.board_serial_port = msg.infovalue

                        elif msg.infoname == Session.INFO_BOARD_NAME:
                            self.board_name = msg.infovalue

                        elif msg.infoname == Session.INFO_SETUP_NAME:
                            self.setup_name = msg.infovalue

                        elif msg.infoname == Session.INFO_SUBJECT_NAME:
                            self.subjects += [msg.infovalue]
                            name, uuid4 = eval(msg.infovalue)
                            subj = self.project.find_subject_by_id(uuid4)
                            if subj is not None:
                                subj += self
                    else:
                        count += 1

                if count > 50:
                    break

            return csvreader
