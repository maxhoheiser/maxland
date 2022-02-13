from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule


def try_run_function(function_to_run):
    def wrapper():
        try:
            function_to_run
            return function_to_run
        except:
            pass

    return wrapper


def post_session_cleanup(
    bpod,
    sma,
    display_stim_event,
    still_show_event,
    stimulus_game,
    rotary_encoder_module,
):
    if not bpod.run_state_machine(sma):
        still_show_event.set()
        display_stim_event.set()
        try_run_function(stimulus_game.win.close())()
        try_run_function(stimulus_game.close())()
        try_run_function(rotary_encoder_module.close())()
        print("\nCLOSED\n")


def find_rotaryencoder_com_port():
    for port in range(20):
        com_port = f"COM{port}"
        try:
            ro = RotaryEncoderModule(com_port)
            ro.close()
        except:
            pass
        else:
            return com_port
