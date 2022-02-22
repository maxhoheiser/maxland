"""
Main config file for the confidentiality task training stage 2a - simple discrimination
This behavior config file makes use of three
Bpod classes the main Bpod and the StateMachine as well as the RotaryEncoder.

In addition it uses three custom classes:
    Stimulus: handeling the psychopy configuration and drawing of the stimulus on the screens
    ProbabilityConstructor: generating the necessary probabilites for each trial
    BpodRotaryEncoder: handeling the rotary encoder and reading the position
    TrialParameterHandler: generating the necessary parameters for each session from the user input and predefined parameters

"""
import os
import random
import threading
from typing import List

import usersettings
from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine

from maxland.helperfunctions import (
    find_rotaryencoder_com_port,
    post_session_cleanup,
    try_run_function,
)
from maxland.parameter_handler import TrialParameterHandler
from maxland.probability_conf import ProbabilityConstructor
from maxland.rotaryencoder import BpodRotaryEncoder
from maxland.stimulus_conf import Stimulus
from maxland.userinput import UserInput

session_folder = os.getcwd()
settings_folder = os.path.dirname(__file__)

settings_obj = TrialParameterHandler(usersettings, settings_folder, session_folder)

bpod = Bpod()

# create tkinter userinput dialoge window
window = UserInput(settings_obj)
window.draw_window_before(stage="habituation_complex")
window.show_window()

# create threading flags
event_display_stimulus = threading.Event()
event_still_show_stimulus = threading.Event()
event_display_stimulus.clear()
event_still_show_stimulus.clear()
event_flags = {
    "event_display_stimulus": event_display_stimulus,
    "event_still_show_stimulus": event_still_show_stimulus,
}

# run session
if settings_obj.run_session:
    settings_obj.update_userinput_file_conf()

    # configure rotary encoder
    com_port = find_rotaryencoder_com_port()
    rotary_encoder_module = BpodRotaryEncoder(com_port, settings_obj, bpod)
    rotary_encoder_module.set_bit_message()
    rotary_encoder_module.set_configuration()
    rotary_encoder_module.enable_stream()

    # softcode handler
    def softcode_handler(data):
        if data == settings_obj.soft_code_present_stimulus:
            event_display_stimulus.set()
        if data == settings_obj.soft_code_start_open_loop:
            stimulus_game.stop_closed_loop_before()
        if data == settings_obj.soft_code_stop_open_loop:
            stimulus_game.stop_open_loop()
        if data == settings_obj.soft_code_end_present_stimulus:
            stimulus_game.stop_closed_loop_after()
            event_still_show_stimulus.set()
        if data == settings_obj.soft_code_wheel_not_stopping:
            print("wheel not stopping")

    bpod.softcode_handler_function = softcode_handler

    probability_obj = ProbabilityConstructor(settings_obj)

    stimulus_game = Stimulus(settings_obj, rotary_encoder_module, probability_obj.stimulus_sides)

    # list of side for correct stimulus
    sides_li: List[int] = []
    times_punish_li: List[int] = []
    insist_mode_li: List[int] = []
    active_rule_li: List[int] = []

    # create main state machine trial loop ---------------------------------------------
    # state machine configs
    for trial in range(settings_obj.trial_number):
        probability_obj.get_random_side()

        # get random punish time
        punish_time = round(
            random.uniform(
                float(settings_obj.time_dict["time_range_no_reward_punish"][0]),
                float(settings_obj.time_dict["time_range_no_reward_punish"][1]),
            ),
            2,
        )
        times_punish_li.append(punish_time)

        sma = StateMachine(bpod)

        # start state to define block of trial
        sma.add_state(
            state_name="start",
            state_timer=settings_obj.time_dict["time_start"],
            state_change_conditions={"Tup": "reset_rotary_encoder_wheel_stopping_check"},
            output_actions=[("SoftCode", settings_obj.soft_code_start_logging)],
        )
        sma.add_state(
            state_name="reset_rotary_encoder_wheel_stopping_check",
            state_timer=0,
            state_change_conditions={"Tup": "wheel_stopping_check"},
            output_actions=[("Serial1", settings_obj.serial_message_reset_rotary_encoder)],
        )

        # wheel not stoping check
        sma.add_state(
            state_name="wheel_stopping_check",
            state_timer=settings_obj.time_dict["time_wheel_stopping_check"],
            state_change_conditions={
                "Tup": "present_stim",
                settings_obj.stimulus_threshold_left: "wheel_stopping_check_failed_punish",
                settings_obj.stimulus_threshold_right: "wheel_stopping_check_failed_punish",
            },
            output_actions=[],
        )
        sma.add_state(
            state_name="wheel_stopping_check_failed_punish",
            state_timer=settings_obj.time_dict["time_wheel_stopping_punish"],
            state_change_conditions={"Tup": "reset_rotary_encoder_wheel_stopping_check"},
            output_actions=[("SoftCode", settings_obj.soft_code_wheel_not_stopping)],
        )

        # Open Loop
        sma.add_state(
            state_name="present_stim",
            state_timer=settings_obj.time_dict["time_stim_pres"],
            state_change_conditions={"Tup": "reset_rotary_encoder_open_loop"},
            output_actions=[("SoftCode", settings_obj.soft_code_present_stimulus)],
        )
        sma.add_state(
            state_name="reset_rotary_encoder_open_loop",
            state_timer=0,
            state_change_conditions={"Tup": "open_loop"},
            output_actions=[("Serial1", settings_obj.serial_message_reset_rotary_encoder)],
        )
        sma.add_state(
            state_name="open_loop",
            state_timer=settings_obj.time_dict["time_open_loop"],
            state_change_conditions={
                "Tup": "stop_open_loop_fail",
                settings_obj.stimulus_threshold_left: "stop_open_loop_reward_left",
                settings_obj.stimulus_threshold_right: "stop_open_loop_reward_right",
            },
            output_actions=[("SoftCode", settings_obj.soft_code_start_open_loop)],
        )

        # stop open loop fail
        sma.add_state(
            state_name="stop_open_loop_fail",
            state_timer=0,
            state_change_conditions={"Tup": "open_loop_fail_punish"},
            output_actions=[("SoftCode", settings_obj.soft_code_stop_open_loop)],
        )
        sma.add_state(
            state_name="open_loop_fail_punish",
            state_timer=settings_obj.time_dict["time_open_loop_fail_punish"],
            state_change_conditions={"Tup": "inter_trial"},
            output_actions=[("SoftCode", settings_obj.soft_code_end_present_stimulus)],
        )

        # reward left -------------------------------
        sma.add_state(
            state_name="stop_open_loop_reward_left",
            state_timer=settings_obj.time_dict["time_stimulus_freeze"],
            state_change_conditions={"Tup": "check_reward_left"},
            output_actions=[("SoftCode", settings_obj.soft_code_stop_open_loop)],
        )

        if probability_obj.stimulus_side["left"]:
            sma.add_state(
                state_name="check_reward_left",
                state_timer=0,
                state_change_conditions={"Tup": "reward_left"},
                output_actions=[],
            )
            sma.add_state(
                state_name="reward_left",
                state_timer=settings_obj.time_dict["time_reward_open"],
                state_change_conditions={"Tup": "reward_left_waiting"},
                output_actions=[("Valve1", 255)],
            )
            sma.add_state(
                state_name="reward_left_waiting",
                state_timer=settings_obj.time_dict["time_reward_waiting"],
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[("SoftCode", settings_obj.soft_code_end_present_stimulus)],
            )

        else:
            # no reward
            sma.add_state(
                state_name="check_reward_left",
                state_timer=0,
                state_change_conditions={"Tup": "no_reward_left"},
                output_actions=[],
            )
            sma.add_state(
                state_name="no_reward_left",
                state_timer=0,
                state_change_conditions={"Tup": "reward_left_waiting"},
                output_actions=[("SoftCode", settings_obj.soft_code_end_present_stimulus)],
            )
            sma.add_state(
                state_name="reward_left_waiting",
                state_timer=punish_time,
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[],
            )

        # reward right -------------------------------------
        sma.add_state(
            state_name="stop_open_loop_reward_right",
            state_timer=settings_obj.time_dict["time_stimulus_freeze"],
            state_change_conditions={"Tup": "check_reward_right"},
            output_actions=[("SoftCode", settings_obj.soft_code_stop_open_loop)],
        )

        if probability_obj.stimulus_side["right"]:
            sma.add_state(
                state_name="check_reward_right",
                state_timer=0,
                state_change_conditions={"Tup": "reward_right"},
                output_actions=[],
            )
            sma.add_state(
                state_name="reward_right",
                state_timer=settings_obj.time_dict["time_reward_open"],
                state_change_conditions={"Tup": "reward_right_waiting"},
                output_actions=[("Valve1", 255)],
            )
            sma.add_state(
                state_name="reward_right_waiting",
                state_timer=settings_obj.time_dict["time_reward_waiting"],
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[("SoftCode", settings_obj.soft_code_end_present_stimulus)],
            )

        else:
            # no reward
            sma.add_state(
                state_name="check_reward_right",
                state_timer=0,
                state_change_conditions={"Tup": "no_reward_right"},
                output_actions=[],
            )
            sma.add_state(
                state_name="no_reward_right",
                state_timer=0,
                state_change_conditions={"Tup": "reward_right_waiting"},
                output_actions=[("SoftCode", settings_obj.soft_code_end_present_stimulus)],
            )
            sma.add_state(
                state_name="reward_right_waiting",
                state_timer=punish_time,
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[],
            )

        # inter trial time
        sma.add_state(
            state_name="inter_trial",
            state_timer=settings_obj.time_dict["time_inter_trial"],
            state_change_conditions={"Tup": "end_state"},
            output_actions=[],
        )

        # end state
        sma.add_state(
            state_name="end_state",
            state_timer=0,
            state_change_conditions={"Tup": "exit"},
            output_actions=[("SoftCode", settings_obj.soft_code_end_logging)],
        )

        # send & run state machine
        bpod.send_state_machine(sma)

        closer = threading.Thread(
            target=post_session_cleanup,
            args=(
                stimulus_game,
                bpod,
                sma,
                event_display_stimulus,
                event_still_show_stimulus,
                rotary_encoder_module,
            ),
        )
        closer.start()

        try:
            stimulus_game.run_game_habituation_2(settings_obj, event_flags)
        except Exception as e:
            print(e)
            break

        closer.join()
        print("---------------------------------------------------")
        print("finished")

        # save session settings
        session_name = bpod.session_name
        settings_obj.times_li = times_punish_li
        settings_obj.insist_mode_li = insist_mode_li
        settings_obj.save_usersettings(session_name)

try_run_function(rotary_encoder_module.close())()
try_run_function(bpod.close())()
