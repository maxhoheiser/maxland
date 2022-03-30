import os
import threading
from pathlib import Path
from typing import cast

import usersettings
from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine

from maxland.helperfunctions import (
    find_rotaryencoder_com_port,
    post_session_cleanup,
    try_run_function,
)
from maxland.parameter_handler import TrialParameterHandler
from maxland.probability_gamble import ProbabilityConstructor
from maxland.rotaryencoder import BpodRotaryEncoder
from maxland.stimulus_gamble import Stimulus
from maxland.types_usersettings import UsersettingsTypes
from maxland.userinput import UserInput

usersettings_obj = cast(UsersettingsTypes, usersettings)

session_folder = os.getcwd()
settings_folder = Path(execution_folder_path=os.path.dirname(__file__))
settings_obj = TrialParameterHandler(usersettings_obj, settings_folder, session_folder)

bpod = Bpod()

window = UserInput(settings_obj)
window.draw_window_before()
window.show_window()

# create threading flags
event_display_stimulus = threading.Event()
event_start_open_loop = threading.Event()
event_still_show_stimulus = threading.Event()
event_display_stimulus.clear()
event_start_open_loop.clear()
event_still_show_stimulus.clear()
event_flags = {
    "event_display_stimulus": event_display_stimulus,
    "event_start_open_loop": event_start_open_loop,
    "event_still_show_stimulus": event_still_show_stimulus,
}


# run session
if settings_obj.run_session:
    settings_obj.update_userinput_file_gamble()
    # rotary encoder config
    com_port = find_rotaryencoder_com_port()
    rotary_encoder_module = BpodRotaryEncoder(com_port, settings_obj, bpod)
    rotary_encoder_module.enable_stream()

    # softcode handler
    def softcode_handler(data):
        if data == settings_obj.soft_code_present_stimulus:
            event_display_stimulus.set()
        if data == settings_obj.soft_code_start_open_loop:
            event_start_open_loop.set()
        if data == settings_obj.soft_code_stop_open_loop:
            stimulus_game.stop_open_loop()
        if data == settings_obj.soft_code_end_present_stimulus:
            event_still_show_stimulus.set()
        if data == settings_obj.soft_code_wheel_not_stopping:
            print("wheel not stopping")

    bpod.softcode_handler_function = softcode_handler

    stimulus_game = Stimulus(settings_obj, rotary_encoder_module)

    probability_obj = ProbabilityConstructor(settings_obj)

    # create main state machine trial loops
    for trial in range(settings_obj.trial_number):
        probability_dict = settings_obj.probability_list[trial]
        sma = StateMachine(bpod)

        # start state to define block of trial
        sma.add_state(
            state_name="start",
            state_timer=settings_obj.time_dict["time_start"],
            state_change_conditions={"Tup": "sync_state_1"},
            output_actions=[
                ("SoftCode", settings_obj.soft_code_start_logging),
                ("BNC1", 1),
                ("BNC2", 1),
            ],
        )
        sma.add_state(
            state_name="sync_state_1",
            state_timer=0,
            state_change_conditions={"Tup": "reset_rotary_encoder_wheel_stopping_check"},
            output_actions=[("BNC1", 0), ("BNC2", 0)],
        )
        sma.add_state(
            state_name="reset_rotary_encoder_wheel_stopping_check",
            state_timer=0,
            state_change_conditions={"Tup": "wheel_stopping_check"},
            output_actions=[
                ("Serial1", settings_obj.serial_message_reset_rotary_encoder),
                ("BNC1", 0),
                ("BNC2", 1),
            ],  # activate white light while waiting
        )
        sma.add_state(
            state_name="wheel_stopping_check",
            state_timer=settings_obj.time_dict["time_wheel_stopping_check"],
            state_change_conditions={
                "Tup": "present_stimulus",
                settings_obj.rotary_encoder_threshold_left: "wheel_stopping_check_failed_punish",
                settings_obj.rotary_encoder_threshold_right: "wheel_stopping_check_failed_punish",
            },
            output_actions=[("BNC1", 0), ("BNC2", 0)],
        )
        sma.add_state(
            state_name="wheel_stopping_check_failed_punish",
            state_timer=settings_obj.time_dict["time_wheel_stopping_punish"],
            state_change_conditions={"Tup": "wheel_stopping_check_failed_reset"},
            output_actions=[("BNC1", 0), ("BNC2", 1)],
        )
        sma.add_state(
            state_name="wheel_stopping_check_failed_reset",
            state_timer=0,
            state_change_conditions={"Tup": "reset_rotary_encoder_wheel_stopping_check"},
            output_actions=[("BNC1", 0), ("BNC2", 0), ("SoftCode", 9)],
        )

        # continue if wheel stopped for time x
        sma.add_state(
            state_name="present_stimulus",
            state_timer=settings_obj.time_dict["time_present_stimulus"],
            state_change_conditions={"Tup": "sync_state_2"},
            output_actions=[
                ("SoftCode", settings_obj.soft_code_present_stimulus),
                ("BNC1", 0),
                ("BNC2", 1),
            ],
        )
        sma.add_state(
            state_name="sync_state_2",
            state_timer=0,
            state_change_conditions={"Tup": "reset_rotary_encoder_open_loop"},
            output_actions=[("BNC1", 0), ("BNC2", 0)],
        )

        sma.add_state(
            state_name="reset_rotary_encoder_open_loop",
            state_timer=0,
            state_change_conditions={"Tup": "open_loop"},
            output_actions=[
                ("Serial1", settings_obj.serial_message_reset_rotary_encoder),
                ("BNC1", 0),
                ("BNC2", 1),
            ],  # reset rotary encoder postition to 0
        )

        # open loop detection
        sma.add_state(
            state_name="open_loop",
            state_timer=settings_obj.time_dict["time_open_loop"],
            state_change_conditions={
                "Tup": "stop_open_loop_fail",
                settings_obj.stimulus_threshold_left: "stop_open_loop_reward_left",
                settings_obj.stimulus_threshold_right: "stop_open_loop_reward_right",
            },
            output_actions=[
                ("SoftCode", settings_obj.soft_code_start_open_loop),
                ("BNC1", 0),
                ("BNC2", 0),
            ],  # softcode to start open loop
        )

        # stop open loop fail
        sma.add_state(
            state_name="stop_open_loop_fail",
            state_timer=0,
            state_change_conditions={"Tup": "sync_state_3"},
            output_actions=[
                ("SoftCode", settings_obj.soft_code_stop_open_loop),
                ("BNC1", 0),
                ("BNC2", 1),
            ],  # stop open loop in py game
        )

        sma.add_state(
            state_name="sync_state_3",
            state_timer=0,
            state_change_conditions={"Tup": "open_loop_fail_punish"},
            output_actions=[("BNC1", 0), ("BNC2", 0)],
        )

        sma.add_state(
            state_name="open_loop_fail_punish",
            state_timer=settings_obj.time_dict["time_open_loop_fail_punish"],
            state_change_conditions={"Tup": "inter_trial"},
            output_actions=[
                ("SoftCode", settings_obj.soft_code_end_present_stimulus),
                ("BNC1", 0),
                ("BNC2", 1),  # must  be 0 1
            ],
        )

        # reward left ---------------------------------
        sma.add_state(
            state_name="stop_open_loop_reward_left",
            state_timer=settings_obj.time_dict["time_stimulus_freeze"],
            state_change_conditions={"Tup": "check_reward_left"},
            output_actions=[
                ("SoftCode", settings_obj.soft_code_stop_open_loop),
                ("BNC1", 0),
                ("BNC2", 1),
            ],  # stop open loop in py game
        )

        # check for gamble side:
        if probability_dict["gamble_left"]:
            print("gamble side: left")
            if probability_dict["gamble_reward"]:
                # big reward
                print("gamble reward left")
                sma.add_state(
                    state_name="check_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "big_reward_left"},
                    output_actions=[("BNC1", 0), ("BNC2", 0)],
                )
                sma.add_state(
                    state_name="big_reward_left",
                    state_timer=settings_obj.time_dict["time_big_reward_open"],
                    state_change_conditions={"Tup": "reward_left_waiting"},
                    output_actions=[
                        ("SoftCode", settings_obj.soft_code_end_present_stimulus),
                        ("Valve1", 255),
                        ("BNC1", 1),
                        ("BNC2", 0),
                    ],
                )
                sma.add_state(
                    state_name="reward_left_waiting",
                    state_timer=settings_obj.time_dict["time_big_reward_waiting"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[("BNC1", 0), ("BNC2", 1)],
                )

            if not probability_dict["gamble_reward"]:
                # no reward
                print("Gamble_No_Reward_left")
                sma.add_state(
                    state_name="check_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "no_reward_left"},
                    output_actions=[("BNC1", 0), ("BNC2", 0)],
                )
                sma.add_state(
                    state_name="no_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "reward_left_waiting"},
                    output_actions=[
                        ("SoftCode", settings_obj.soft_code_end_present_stimulus),
                        ("BNC1", 1),
                        ("BNC2", 0),
                    ],
                )
                sma.add_state(
                    state_name="reward_left_waiting",
                    state_timer=settings_obj.time_dict["time_reward"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[("BNC1", 0), ("BNC2", 1)],
                )
        if not probability_dict["gamble_left"]:
            print("safe side left")
            if probability_dict["safe_reward"]:
                print("safe reward left")
                # small reward
                sma.add_state(
                    state_name="check_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "small_reward_left"},
                    output_actions=[("BNC1", 0), ("BNC2", 0)],
                )
                sma.add_state(
                    state_name="small_reward_left",
                    state_timer=settings_obj.time_dict["time_small_reward_open"],
                    state_change_conditions={"Tup": "reward_left_waiting"},
                    output_actions=[
                        ("SoftCode", settings_obj.soft_code_end_present_stimulus),
                        ("Valve1", 255),
                        ("BNC1", 1),
                        ("BNC2", 0),
                    ],
                )
                sma.add_state(
                    state_name="reward_left_waiting",
                    state_timer=settings_obj.time_dict["time_small_reward_waiting"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[("BNC1", 0), ("BNC2", 1)],
                )

            if not probability_dict["safe_reward"]:
                print("safe no-reward left")
                # no reward
                sma.add_state(
                    state_name="check_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "no_reward_left"},
                    output_actions=[("BNC1", 0), ("BNC2", 0)],
                )
                sma.add_state(
                    state_name="no_reward_left",
                    state_timer=0,
                    state_change_conditions={"Tup": "reward_left_waiting"},
                    output_actions=[
                        ("SoftCode", settings_obj.soft_code_end_present_stimulus),
                        ("BNC1", 1),
                        ("BNC2", 0),
                    ],
                )
                sma.add_state(
                    state_name="reward_left_waiting",
                    state_timer=settings_obj.time_dict["time_reward"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[("BNC1", 0), ("BNC2", 1)],
                )

        # reward right side: -------------------------
        sma.add_state(
            state_name="stop_open_loop_reward_right",
            state_timer=settings_obj.time_dict["time_stimulus_freeze"],
            state_change_conditions={"Tup": "check_reward_right"},
            output_actions=[
                ("SoftCode", settings_obj.soft_code_stop_open_loop),
                ("BNC1", 0),
                ("BNC2", 1),
            ],
        )

        # check for gamble side:
        if not probability_dict["gamble_left"]:
            print("gamble side: right")
            if probability_dict["gamble_reward"]:
                print("gamble reward right")
                # big reward
                sma.add_state(
                    state_name="check_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "big_reward_right"},
                    output_actions=[("BNC1", 0), ("BNC2", 0)],
                )
                sma.add_state(
                    state_name="big_reward_right",
                    state_timer=settings_obj.time_dict["time_big_reward_open"],
                    state_change_conditions={"Tup": "reward_right_waiting"},
                    output_actions=[
                        ("SoftCode", settings_obj.soft_code_end_present_stimulus),
                        ("Valve1", 255),
                        ("BNC1", 1),
                        ("BNC2", 0),
                    ],
                )
                sma.add_state(
                    state_name="reward_right_waiting",
                    state_timer=settings_obj.time_dict["time_big_reward_waiting"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[("BNC1", 0), ("BNC2", 1)],
                )

            if not probability_dict["gamble_reward"]:
                print("gamble no-reward right")
                # no reward
                sma.add_state(
                    state_name="check_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "no_reward_right"},
                    output_actions=[("BNC1", 0), ("BNC2", 0)],
                )
                sma.add_state(
                    state_name="no_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "reward_right_waiting"},
                    output_actions=[
                        ("SoftCode", settings_obj.soft_code_end_present_stimulus),
                        ("BNC1", 1),
                        ("BNC2", 0),
                    ],
                )
                sma.add_state(
                    state_name="reward_right_waiting",
                    state_timer=settings_obj.time_dict["time_reward"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[("BNC1", 0), ("BNC2", 1)],
                )

        if probability_dict["safe_reward"]:
            print("safe side: right")
            if probability_dict["safe_reward"]:
                print("safe reward right")
                # small reward
                sma.add_state(
                    state_name="check_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "small_reward_right"},
                    output_actions=[("BNC1", 0), ("BNC2", 0)],
                )
                sma.add_state(
                    state_name="small_reward_right",
                    state_timer=settings_obj.time_dict["time_small_reward_open"],
                    state_change_conditions={"Tup": "reward_right_waiting"},
                    output_actions=[
                        ("SoftCode", settings_obj.soft_code_end_present_stimulus),
                        ("Valve1", 255),
                        ("BNC1", 1),
                        ("BNC2", 0),
                    ],
                )
                sma.add_state(
                    state_name="reward_right_waiting",
                    state_timer=settings_obj.time_dict["time_small_reward_waiting"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[("BNC1", 0), ("BNC2", 1)],
                )

            if not probability_dict["safe_reward"]:
                # no reward
                print("safe no-reward right")
                # no reward
                sma.add_state(
                    state_name="check_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "no_reward_right"},
                    output_actions=[("BNC1", 0), ("BNC2", 0)],
                )
                sma.add_state(
                    state_name="no_reward_right",
                    state_timer=0,
                    state_change_conditions={"Tup": "reward_right_waiting"},
                    output_actions=[
                        ("SoftCode", settings_obj.soft_code_end_present_stimulus),
                        ("BNC1", 1),
                        ("BNC2", 0),
                    ],
                )
                sma.add_state(
                    state_name="reward_right_waiting",
                    state_timer=settings_obj.time_dict["time_reward"],
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[("BNC1", 0), ("BNC2", 1)],
                )

        sma.add_state(
            state_name="inter_trial",
            state_timer=settings_obj.time_dict["time_inter_trial"],
            state_change_conditions={"Tup": "end_state_signal"},
            output_actions=[("BNC1", 0), ("BNC2", 0)],
        )

        # end state necessary for bnc1 and bnc2 = +1
        sma.add_state(
            state_name="end_state_signal",
            state_timer=0,
            state_change_conditions={"Tup": "end_state"},
            output_actions=[("BNC1", 1), ("BNC2", 1)],
        )
        sma.add_state(
            state_name="end_state",
            state_timer=0,
            state_change_conditions={"Tup": "exit"},
            output_actions=[
                ("SoftCode", settings_obj.soft_code_end_logging),
                ("BNC1", 0),
                ("BNC2", 0),
            ],
        )

        bpod.send_state_machine(sma)

        closer = threading.Thread(
            target=post_session_cleanup,
            args=(stimulus_game, bpod, sma, event_flags),
        )
        closer.start()

        try:
            stimulus_game.run_game(event_flags)
        except Exception as e:
            print(e)
            continue

        closer.join()
        print("---------------------------------------------------\n")
        print(f"Current trial: {trial}")

    print("---------------------------------------------------\n")
    print("finished")

    session_name = bpod.session_name
    settings_obj.save_usersettings(session_name)

try_run_function(rotary_encoder_module.close())()
