# helper functions for pybpod


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