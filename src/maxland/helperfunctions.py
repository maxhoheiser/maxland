import os
import sys
from contextlib import contextmanager
from typing import Union

from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine

from maxland.stimulus_conf import Stimulus as StimulusConfidentiality
from maxland.stimulus_gamble import Stimulus as StimulusGamble
from maxland.types_usersettings import TaskName


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def try_run_function(function_to_run):
    def wrapper():
        try:
            function_to_run
            return function_to_run
        except Exception as e:
            print(f"{function_to_run} failed with error: {e}")
            pass

    return wrapper


def post_session_cleanup(
    stimulus_game: Union[StimulusGamble, StimulusConfidentiality],
    bpod: Bpod,
    sma: StateMachine,
    event_flags,
    task_name: TaskName,
):
    if not bpod.run_state_machine(sma):
        event_flags["event_display_stimulus"].set()
        if task_name == TaskName.GAMBLE:
            event_flags["event_still_show_stimulus"].set()
            event_flags["event_start_open_loop"].set()
        try_run_function(stimulus_game.win.close())()
        print("\nCLOSED\n")


def find_rotaryencoder_com_port():
    with suppress_stdout():
        for port in range(20):
            com_port = f"COM{port}"
            try:
                ro = RotaryEncoderModule(com_port)
                ro.close()
                return com_port
            except Exception:
                pass


def find_bpod_com_port():
    with suppress_stdout():
        for port in range(20):
            com_port = f"COM{port}"
            try:
                bpod = Bpod(com_port)
                bpod.close()
                return com_port
            except Exception:
                pass
