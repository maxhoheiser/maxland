import os
import threading
from pathlib import Path

import usersettings
from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpodgui_api.models.session import Session

from maxland.helperfunctions import (
    find_rotaryencoder_com_port,
    post_session_cleanup,
    try_run_function,
)
from maxland.parameter_handler import TrialParameterHandler
from maxland.probability_gamble import ProbabilityConstructor
from maxland.rotaryencoder import BpodRotaryEncoder
from maxland.stimulus_gamble import Stimulus
from maxland.userinput import UserInput

session_folder = os.getcwd()
settings_folder = Path(execution_folder_path=os.path.dirname(__file__))
settings_obj = TrialParameterHandler(usersettings, settings_folder, session_folder)

bpod = Bpod()

window = UserInput(settings_obj)
window.draw_window_before_gamble()
window.show_window()
window.update_settings()

# multithreading flags
display_stimulus_event = threading.Event()
start_open_loop_event = threading.Event()
freeze_stimulus_event = threading.Event()
display_stimulus_event.clear()
start_open_loop_event.clear()
freeze_stimulus_event.clear()


# run session
if settings_obj.run_session:
    settings_obj.update_userinput_file_gamble()
    # rotary encoder config
    com_port = find_rotaryencoder_com_port()
    rotary_encoder_module = BpodRotaryEncoder(com_port, settings_obj, bpod)
    rotary_encoder_module.set_bit_message()
    rotary_encoder_module.set_configuration()
    rotary_encoder_module.enable_stream()

    # softcode handler
    def softcode_handler(data):
        if data == settings_obj.soft_code_present_stimulus:
            display_stimulus_event.set()
            print("present stimulus")
        elif data == settings_obj.soft_code_start_open_loop:
            start_open_loop_event.set()
            print("start open loop")
        elif data == settings_obj.soft_code_stop_open_loop:
            stimulus_game.stop_open_loop()
            print("stop open loop")
        elif data == settings_obj.soft_code_end_present_stimulus:
            freeze_stimulus_event.set()
            print("end present stimulus")
        elif data == settings_obj.soft_code_wheel_not_stopping:
            print("wheel not stopping")

    bpod.softcode_handler_function = softcode_handler

    stimulus_game = Stimulus(settings_obj, rotary_encoder_module)

    probability_obj = ProbabilityConstructor(settings_obj)

    # create main state machine trial loops
    for trial in range(settings_obj.trial_num):
        probability_dict = settings_obj.probability_list[trial]
        sma = StateMachine(bpod)

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
                ("Serial1", settings_obj.bit_message_reset_rotary_encoder),
                ("BNC1", 0),
                ("BNC2", 1),
            ],  # activate white light while waiting
        )
        sma.add_state(
            state_name="wheel_stopping_check",
            state_timer=settings_obj.time_dict["time_wheel_stopping_check"],
            state_change_conditions={
                "Tup": "present_stim",
                settings_obj.rotary_encoder_threshhold_left: "wheel_stopping_check_failed_punish",
                settings_obj.rotary_encoder_threshhold_right: "wheel_stopping_check_failed_punish",
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
            state_name="present_stim",
            state_timer=settings_obj.time_dict["time_stim_pres"],
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
                ("Serial1", settings_obj.bit_message_reset_rotary_encoder),
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
                ("SoftCode", settings_obj.soft_code_stop_open_loop),
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

        # reward left
        sma.add_state(
            state_name="stop_open_loop_reward_left",
            state_timer=settings_obj.time_dict["time_stim_freez"],
            state_change_conditions={"Tup": "check_reward_left"},
            output_actions=[
                ("SoftCode", settings_obj.soft_code_stop_open_loop),
                ("BNC1", 0),
                ("BNC2", 1),
            ],  # stop open loop in py game
        )

        # check for gamble side:
        if probability_dict["gamble_left"]:
            if probability_dict["gamble_reward"]:
                print("Gamble_reward_left")
                # big reward
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

            else:
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

        if probability_dict["safe_reward"]:
            print("safereward_gambleleft")
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

        else:
            print("nosafereward_gamble_left")
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

        # reward right side: ======================================================================
        sma.add_state(
            state_name="stop_open_loop_reward_right",
            state_timer=settings_obj.time_dict["time_stim_freez"],
            state_change_conditions={"Tup": "check_reward_right"},
            output_actions=[
                ("SoftCode", settings_obj.soft_code_stop_open_loop),
                ("BNC1", 0),
                ("BNC2", 1),
            ],
        )

        # check for gamble side:
        if not probability_dict["gamble_left"]:
            if probability_dict["gamble_reward"]:
                print("Gamble_Reward_right")
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

            else:
                print("gamble_No_Reward_right")
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
            print("safe_reward_right")
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

        else:
            print("safe_No_reward_right")
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
            args=(
                stimulus_game,
                bpod,
                sma,
                display_stimulus_event,
                start_open_loop_event,
                freeze_stimulus_event,
            ),
        )
        closer.start()

        try:
            stimulus_game.run_game(display_stimulus_event, start_open_loop_event, freeze_stimulus_event, bpod, sma)
        except:
            continue

        closer.join()
        print("---------------------------------------------------\n")
        print(f"Current trial: {trial}")

    print("---------------------------------------------------\n")
    print("finished")

    session_name = bpod.session_name
    settings_obj.save_usersettings(session_name)

try_run_function(rotary_encoder_module.close())()