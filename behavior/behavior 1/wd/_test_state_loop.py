from probability import ProbabilityConstuctor
import settings

probability_object = ProbabilityConstuctor(settings)
probability_list = probability_object.probability_list


TRIAL_NUM = 0
for block in settings.BLOCKS:
    TRIAL_NUM += block[settings.TRIAL_NUM_BLOCK]

state_j_list = []

for trial in range(TRIAL_NUM):
    trial_j_list = []
    probability_dict = probability_list[trial]
    trial_j_list.append(probability_dict)
    # define states
    trial_j_list.append([
        "start1",
        settings.TIME_START,
        {"Tup": "reset_rotary_encoder_wheel_stopping_check"},
        [],
    ])
    # reset rotary encoder bevore checking for wheel not stoping
    trial_j_list.append([
        "reset_rotary_encoder_wheel_stopping_check",
        0,
        {"Tup":"wheel_stopping_check"},
        [("Serial1", settings.RESET_ROTARY_ENCODER)], # activate white light while waiting
    ] )
    #wheel not stoping check
    trial_j_list.append([
        "wheel_stopping_check",
        settings.TIME_WHEEL_STOPPING_CHECK,
        {
                "Tup":"present_stim",
                settings.THRESH_LEFT:"wheel_stopping_check_failed_punish",
                settings.THRESH_RIGHT:"wheel_stopping_check_failed_punish",
                },
        [],
    ] )
    trial_j_list.append([
        "wheel_stopping_check_failed_punish",
        settings.TIME_WHEEL_STOPPING_PUNISH,
        {"Tup":"start1"},
        [],
    ] )

    # ==========================================
    # continue if wheel stopped for time x
    trial_j_list.append([
        "present_stim",
        settings.TIME_PRESENT_STIM,
        {"Tup": "reset_rotary_encoder_open_loop"},
        [("SoftCode", settings.SC_PRESENT_STIM)],#after wait -> present initial stimulus
    ] )
    # reset rotary encoder bevor open loop starts
    trial_j_list.append([
        "reset_rotary_encoder_open_loop",
        0,
        {"Tup": "open_loop"},
        [("Serial1", settings.RESET_ROTARY_ENCODER),
                        ("SoftCode", settings.SC_START_OPEN_LOOP)
                        ], # reset rotary encoder postition to 0
    ] )
    # open loop detection
    trial_j_list.append([
        "open_loop",
        settings.TIME_OPEN_LOOP,
        {
            "Tup": "stop_open_loop_fail",
            settings.STIMULUS_LEFT: "stop_open_loop_reward_left",
            settings.STIMULUS_RIGHT: "stop_open_loop_reward_right",
            },
        [],
    ] )
    #============================================
    # stop open loop fail
    trial_j_list.append([
        "stop_open_loop_fail",
        0,
        {"Tup": "open_loop_fail_punish"},
        [("SoftCode", settings.SC_END_PRESENT_STIM),
                        ("SoftCode", settings.SC_STOP_OPEN_LOOP)
                        ] # stop open loop in py game
    ] )
    # open loop fail punish time & exit trial
    trial_j_list.append([
        "open_loop_fail_punish",
        settings.TIME_OPEN_LOOP_FAIL_PUNISH,
        {"Tup": "exit"},
        []
    ] )

    #=========================================================================================
    # reward left
    trial_j_list.append([
        "stop_open_loop_reward_left",
        settings.TIME_STIM_FREEZ,
        {"Tup": "reward_left"},
        [("SoftCode", settings.SC_STOP_OPEN_LOOP)] # stop open loop in py game
    ] )

    # check for gmble side:
    if probability_dict["gambl_left"]:
        # check for probability of big reard
        if probability_dict["gambl_reward"]:
            # big rewaerd
            trial_j_list.append([
                "reward_left",
                2,
                {"Tup": "reward_left_waiting"},
                [("SoftCode", settings.SC_END_PRESENT_STIM),
                                #("Valve1", 255)
                                ]
            ] )
            trial_j_list.append([
                "reward_left_waiting",
                settings.big_reward_waiting_time,
                {"Tup": "inter_trial"},
                []
            ] )
        else:
            # no reward
            trial_j_list.append([
                "reward_left",
                0,
                {"Tup": "reward_left_waiting"},
                [("SoftCode", 4)],
            ] )
            trial_j_list.append([
                "reward_left_waiting",
                settings.REWARD_TIME,
                {"Tup": "inter_trial"},
                []
            ] )
    elif probability_dict["safe_reward"]:
        # small reward
        trial_j_list.append([
            "reward_left",
            settings.SMALL_REWARD_TIME,
            {"Tup": "reward_left_waiting"},
            [("SoftCode", 4),
                            #("Valve1", 255)
                            ]
        ] )
        trial_j_list.append([
            "reward_left_waiting",
            settings.small_reward_waiting_time,
            {"Tup": "inter_trial"},
            []
        ] )
    else:
        # no reward
        trial_j_list.append([
            "reward_left",
            REWARD_TIME,
            {"Tup": "reward_left_waiting"},
            [("SoftCode", 4),
                            #("Valve1", 255)
                            ]
        ] )
        trial_j_list.append([
            "reward_left_waiting",
            settings.REWARD_TIME,
            {"Tup": "inter_trial"},
            []
        ] )

    #=========================================================================================
    # reward right
    trial_j_list.append([
        "stop_open_loop_reward_right",
        settings.TIME_STIM_FREEZ,
        {"Tup": "reward_right"},
        [("SoftCode", settings.SC_STOP_OPEN_LOOP)] # stop open loop in py game
    ] )

    # check for gmble side:
    if not probability_dict["gambl_left"]:
        # check for probability of big reard
        if probability_dict["gambl_reward"]:
            # big rewaerd
            trial_j_list.append([
                "reward_right",
                2,
                {"Tup": "reward_right_waiting"},
                [("SoftCode", 4),
                                #("Valve1", 255)
                                ]
            ] )
            trial_j_list.append([
                "reward_right_waiting",
                settings.big_reward_waiting_time,
                {"Tup": "inter_trial"},
                []
            ] )
        else:
            # no reward
            trial_j_list.append([
                "reward_right",
                0,
                {"Tup": "reward_right_waiting"},
                [("SoftCode", 4)],
            ] )
            trial_j_list.append([
                "reward_right_waiting",
                settings.REWARD_TIME,
                {"Tup": "inter_trial"},
                []
            ] )
    elif probability_dict["safe_reward"]:
        # small reward
        trial_j_list.append([
            "reward_right",
            settings.SMALL_REWARD_TIME,
            {"Tup": "reward_right_waiting"},
            [("SoftCode", 4),
                            #("Valve1", 255)
                            ]
        ] )
        trial_j_list.append([
            "reward_right_waiting",
            settings.small_reward_waiting_time,
            {"Tup": "inter_trial"},
            []
        ] )
    else:
        # no reward
        trial_j_list.append([
            "reward_right",
            settings.REWARD_TIME,
            {"Tup": "reward_right_waiting"},
            [("SoftCode", 4),
                            #("Valve1", 255)
                            ]
        ] )
        trial_j_list.append([
            "reward_right_waiting",
            settings.REWARD_TIME,
            {"Tup": "inter_trial"},
            []
        ] )

    # inter trial time
    trial_j_list.append([
        "inter_trial",
        settings.INTER_TRIAL_TIME,
        {"Tup": "exit"},
        []
    ] )
    state_j_list.append(trial_j_list)


for trial in range(TRIAL_NUM):
    trial_j_list = []
    probability_dict = probability_list[trial]
    trial_j_list.append(probability_dict)
    # define states
    # define states
    trial_j_list.append([
        "start1",
        settings.TIME_START,
        {"Tup": "reset_rotary_encoder_wheel_stopping_check"},
        [],
    ] )
    # reset rotary encoder bevore checking for wheel not stoping
    trial_j_list.append([
        "reset_rotary_encoder_wheel_stopping_check",
        0,
        {"Tup":"wheel_stopping_check"},
        [("Serial1", settings.RESET_ROTARY_ENCODER)], # activate white light while waiting
    ] )
    #wheel not stoping check
    trial_j_list.append([
        "wheel_stopping_check",
        settings.TIME_WHEEL_STOPPING_CHECK,
        {
                "Tup":"present_stim",
                settings.THRESH_LEFT:"wheel_stopping_check_failed_punish",
                settings.THRESH_RIGHT:"wheel_stopping_check_failed_punish",
                },
        [],
    ] )
    trial_j_list.append([
        "wheel_stopping_check_failed_punish",
        settings.TIME_WHEEL_STOPPING_PUNISH,
        {"Tup":"start1"},
        [],
    ] )

    # ==========================================
    # continue if wheel stopped for time x
    trial_j_list.append([
        "present_stim",
        settings.TIME_PRESENT_STIM,
        {"Tup": "reset_rotary_encoder_open_loop"},
        [("SoftCode", settings.SC_PRESENT_STIM)],#after wait -> present initial stimulus
    ] )
    # reset rotary encoder bevor open loop starts
    trial_j_list.append([
        "reset_rotary_encoder_open_loop",
        0,
        {"Tup": "open_loop"},
        [("Serial1", settings.RESET_ROTARY_ENCODER),
                        ("SoftCode", settings.SC_START_OPEN_LOOP)
                        ], # reset rotary encoder postition to 0
    ] )
    # open loop detection
    trial_j_list.append([
        "open_loop",
        settings.TIME_OPEN_LOOP,
        {
            "Tup": "stop_open_loop_fail",
            settings.STIMULUS_LEFT: "stop_open_loop_reward_left",
            settings.STIMULUS_RIGHT: "stop_open_loop_reward_right",
            },
        [],
    ] )
    #============================================
    # stop open loop fail
    trial_j_list.append([
        "stop_open_loop_fail",
        0,
        {"Tup": "open_loop_fail_punish"},
        [("SoftCode", settings.SC_STOP_OPEN_LOOP)] # stop open loop in py game
    ] )
    # open loop fail punish time & exit trial
    trial_j_list.append([
        "open_loop_fail_punish",
        settings.TIME_OPEN_LOOP_FAIL_PUNISH,
        {"Tup": "exit"},
        [("SoftCode", settings.SC_END_PRESENT_STIM)]
    ] )

    #=========================================================================================
    # reward left
    trial_j_list.append([
        "stop_open_loop_reward_left",
        settings.TIME_STIM_FREEZ,
        {"Tup": "reward_left"},
        [("SoftCode", settings.SC_STOP_OPEN_LOOP)] # stop open loop in py game
    ] )

    # check for gmble side:
    if probability_dict["gambl_left"]:
        # check for probability of big reard
        if probability_dict["gambl_reward"]:
            # big rewaerd
            trial_j_list.append([
                "reward_left",
                settings.BIG_REWARD_TIME,
                {"Tup": "reward_left_waiting"},
                [("SoftCode", settings.SC_END_PRESENT_STIM),
                                ("Valve1", 255)
                                ]
            ] )
            trial_j_list.append([
                "reward_left_waiting",
                settings.big_reward_waiting_time,
                {"Tup": "inter_trial"},
                []
            ] )
        else:
            # no reward
            trial_j_list.append([
                "reward_left",
                0,
                {"Tup": "reward_left_waiting"},
                [("SoftCode", settings.SC_END_PRESENT_STIM)],
            ] )
            trial_j_list.append([
                "reward_left_waiting",
                settings.REWARD_TIME,
                {"Tup": "inter_trial"},
                []
            ] )
    elif probability_dict["safe_reward"]:
        # small reward
        trial_j_list.append([
            "reward_left",
            settings.SMALL_REWARD_TIME,
            {"Tup": "reward_left_waiting"},
            [("SoftCode", settings.SC_END_PRESENT_STIM),
                            ("Valve1", 255)
                            ]
        ] )
        trial_j_list.append([
            "reward_left_waiting",
            settings.small_reward_waiting_time,
            {"Tup": "inter_trial"},
            []
        ] )
    else:
        # no reward
        trial_j_list.append([
            "reward_left",
            0,
            {"Tup": "reward_left_waiting"},
            [("SoftCode", settings.SC_END_PRESENT_STIM)]
        ] )
        trial_j_list.append([
            "reward_left_waiting",
            settings.REWARD_TIME,
            {"Tup": "inter_trial"},
            []
        ] )

    #=========================================================================================
    # reward right
    trial_j_list.append([
        "stop_open_loop_reward_right",
        settings.TIME_STIM_FREEZ,
        {"Tup": "reward_right"},
        [("SoftCode", settings.SC_STOP_OPEN_LOOP)] # stop open loop in py game
    ] )

    # check for gmble side:
    if not probability_dict["gambl_left"]:
        # check for probability of big reard
        if probability_dict["gambl_reward"]:
            # big rewaerd
            trial_j_list.append([
                "reward_right",
                settings.BIG_REWARD_TIME,
                {"Tup": "reward_right_waiting"},
                [("SoftCode", settings.SC_END_PRESENT_STIM),
                                ("Valve1", 255)
                                ]
            ] )
            trial_j_list.append([
                "reward_right_waiting",
                settings.big_reward_waiting_time,
                {"Tup": "inter_trial"},
                []
            ] )
        else:
            # no reward
            trial_j_list.append([
                "reward_right",
                0,
                {"Tup": "reward_right_waiting"},
                [("SoftCode", settings.SC_END_PRESENT_STIM)],
            ] )
            trial_j_list.append([
                "reward_right_waiting",
                settings.REWARD_TIME,
                {"Tup": "inter_trial"},
                []
            ] )
    elif probability_dict["safe_reward"]:
        # small reward
        trial_j_list.append([
            "reward_right",
            settings.SMALL_REWARD_TIME,
            {"Tup": "reward_right_waiting"},
            [("SoftCode", settings.SC_END_PRESENT_STIM),
                            ("Valve1", 255)
                            ]
        ] )
        trial_j_list.append([
            "reward_right_waiting",
            settings.small_reward_waiting_time,
            {"Tup": "inter_trial"},
            []
        ] )
    else:
        # no reward
        trial_j_list.append([
            "reward_right",
            0,
            {"Tup": "reward_right_waiting"},
            [("SoftCode", settings.SC_END_PRESENT_STIM)]
        ] )
        trial_j_list.append([
            "reward_right_waiting",
            settings.REWARD_TIME,
            {"Tup": "inter_trial"},
            []
        ] )

    # inter trial time
    trial_j_list.append([
        "inter_trial",
        settings.INTER_TRIAL_TIME,
        {"Tup": "exit"},
        []
    ] )
    state_j_list.append(trial_j_list)


# json:
import json
with open('states.txt', 'w') as f:
    for line in state_j_list:
        for line_2 in line:
            json.dump(line_2, f)
            f.write('\n')
        f.write('\n')
        f.write('\n')