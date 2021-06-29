# helper functions for pybpod
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule


def tryer(fn):
    def wrapper():
        try:
            fn
        except:
            pass
    return wrapper

def closer_fn(stimulus_game, bpod, sma, display_stim_event, still_show_event, rotary_encoder_module):
    if not bpod.run_state_machine(sma):
        still_show_event.set()
        display_stim_event.set()
        tryer(stimulus_game.win.close())()
        tryer(stimulus_game.close())()
        tryer(rotary_encoder_module.close())()
        print("\nCLOSED\n")

def find_rotary_com_port():
    for port in range(10):
        com_port = f"COM{port}"
        try:
            ro = RotaryEncoderModule(com_port)
            ro.close()
        except:
            pass
        else:
            return com_port