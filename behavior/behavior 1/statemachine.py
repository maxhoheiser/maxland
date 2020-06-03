"""
State machine constructor
"""
from pybpodapi.state_machine import StateMachine

class StateMachineBuilder():
    def __init__(self, bpod, settings, probability_dict):
        self.sma = StateMachine(bpod)
        self.TIME_START = settings.TIME_START
        self.TIME_WHEEL_STOPPING_CHECK = settings.TIME_WHEEL_STOPPING_CHECK
        self.TIME_WHEEL_STOPPING_PUNISH = settings.TIME_WHEEL_STOPPING_PUNISH
        self.TIME_PRESENT_STIM = settings.TIME_PRESENT_STIM
        self.TIME_OPEN_LOOP = settings.TIME_OPEN_LOOP
        self.TIME_OPEN_LOOP_FAIL_PUNISH = settings.TIME_OPEN_LOOP_FAIL_PUNISH
        self.TIME_STIM_FREEZ = settings.TIME_STIM_FREEZ
        self.REWARD_TIME = settings.REWARD_TIME
        self.BIG_REWARD_TIME = settings.BIG_REWARD_TIME
        self.SMALL_REWARD_TIME = settings.SMALL_REWARD_TIME
        self.SC_PRESENT_STIM = settings.SC_PRESENT_STIM
        self.SC_START_OPEN_LOOP = settings.SC_START_OPEN_LOOP
        self.SC_STOP_OPEN_LOOP = settings.SC_STOP_OPEN_LOOP
        self.SC_END_PRESENT_STIM = settings.SC_END_PRESENT_STIM
        self.RESET_ROTARY_ENCODER = settings.RESET_ROTARY_ENCODER
        self.THRESH_LEFT = settings.THRESH_LEFT
        self.THRESH_RIGHT = settings.THRESH_RIGHT
        self.STIMULUS_LEFT = settings.STIMULUS_LEFT
        self.STIMULUS_RIGHT = settings.STIMULUS_RIGHT
        self.probability_dict = probability


    def add_trial(self):
        self.sma.add_state(
            state_name="start1",
            state_timer=self.TIME_START,
            state_change_conditions={"Tup": "reset_rotary_encoder_wheel_stopping_check"},
            output_actions=[],
        )
        # reset rotary encoder bevore checking for wheel not stoping
        self.sma.add_state(
            state_name="reset_rotary_encoder_wheel_stopping_check",
            state_timer=0,
            state_change_conditions={"Tup":"wheel_stopping_check"},
            output_actions=[("Serial1", self.RESET_ROTARY_ENCODER)], # activate white light while waiting
        )
        #wheel not stoping check
        self.sma.add_state(
            state_name="wheel_stopping_check",
            state_timer=self.TIME_WHEEL_STOPPING_CHECK,
            state_change_conditions={
                    "Tup":"present_stim",
                    self.THRESH_LEFT:"wheel_stopping_check_failed_punish",
                    self.THRESH_RIGHT:"wheel_stopping_check_failed_punish",
                    },
            output_actions=[],
        )
        self.sma.add_state(
            state_name="wheel_stopping_check_failed_punish",
            state_timer=self.TIME_WHEEL_STOPPING_PUNISH,
            state_change_conditions={"Tup":"start1"},
            output_actions=[],
        )

        # ==========================================
        # continue if wheel stopped for time x
        self.sma.add_state(
            state_name="present_stim",
            state_timer=self.TIME_PRESENT_STIM,
            state_change_conditions={"Tup": "reset_rotary_encoder_open_loop"},
            output_actions=[("SoftCode", self.SC_PRESENT_STIM)],#after wait -> present initial stimulus
        )
        # reset rotary encoder bevor open loop starts
        self.sma.add_state(
            state_name="reset_rotary_encoder_open_loop",
            state_timer=0,
            state_change_conditions={"Tup": "open_loop"},
            output_actions=[("Serial1", self.RESET_ROTARY_ENCODER),
                            ("SoftCode", self.SC_START_OPEN_LOOP)
                            ], # reset rotary encoder postition to 0
        )
        # open loop detection
        self.sma.add_state(
            state_name="open_loop",
            state_timer=self.TIME_OPEN_LOOP,
            state_change_conditions={
                "Tup": "stop_open_loop_fail",
                self.STIMULUS_LEFT: "stop_open_loop_reward_left",
                self.STIMULUS_RIGHT: "stop_open_loop_reward_right",
                },
            output_actions=[],
        )
        #============================================
        # stop open loop fail
        self.sma.add_state(
            state_name="stop_open_loop_fail",
            state_timer=0,
            state_change_conditions={"Tup": "open_loop_fail_punish"},
            output_actions=[("SoftCode", self.SC_END_PRESENT_STIM),
                            ("SoftCode", self.SC_STOP_OPEN_LOOP)
                            ] # stop open loop in py game
        )
        # open loop fail punish time & exit trial
        self.sma.add_state(
            state_name="open_loop_fail_punish",
            state_timer=self.TIME_OPEN_LOOP_FAIL_PUNISH,
            state_change_conditions={"Tup": "exit"},
            output_actions=[]
        )

        #===========================================
        # reward left
        self.sma.add_state(
            state_name="stop_open_loop_reward_left",
            state_timer=self.TIME_STIM_FREEZ,
            state_change_conditions={"Tup": "reward"},
            output_actions=[("SoftCode", self.SC_STOP_OPEN_LOOP)] # stop open loop in py game
        )

        # check for gmble side:
        if self.probability_dict["gambl_left"]:
            # check for probability of big reard
            if self.probability_dict["gambl_reward"]:
                # big rewaerd
                self.sma.add_state(
                    state_name="reward",
                    state_timer=self.BIG_REWARD_TIME,
                    state_change_conditions={"Tup": "reward_waiting"},
                    output_actions=[("SoftCode", self.SC_END_PRESENT_STIM),
                                    ("Valve1", 255)
                                    ]
                )
                self.sma.add_state(
                    state_name="reward_waiting",
                    state_timer=self.big_reward_waiting_time,
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[]
                )
            else:
                # no reward
                self.sma.add_state(
                    state_name="reward",
                    state_timer=0,
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[("SoftCode", self.SC_END_PRESENT_STIM)],
                )
                self.sma.add_state(
                    state_name="reward_waiting",
                    state_timer=self.REWARD_TIME,
                    state_change_conditions={"Tup": "inter_trial"},
                    output_actions=[]
                )
        elif self.probability_dict["safe_reward"]:
            # self.small reward
            self.sma.add_state(
                state_name="reward",
                state_timer=self.smaLL_REWARD_TIME,
                state_change_conditions={"Tup": "reward_waiting"},
                output_actions=[("SoftCode", self.SC_END_PRESENT_STIM),
                                ("Valve1", 255)
                                ]
            )
            self.sma.add_state(
                state_name="reward_waiting",
                state_timer=self.small_reward_waiting_time,
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[]
            )
        else:
            # no reward
            self.sma.add_state(
                state_name="reward",
                state_timer=REWARD_TIME,
                state_change_conditions={"Tup": "reward_waiting"},
                output_actions=[("SoftCode", self.SC_END_PRESENT_STIM),
                                ("Valve1", 255)
                                ]
            )
            self.sma.add_state(
                state_name="reward_waiting",
                state_timer=self.REWARD_TIME,
                state_change_conditions={"Tup": "inter_trial"},
                output_actions=[]
            )

        # inter trial time
        self.sma.add_state(
            state_name="inter_trial",
            state_timer=self.INTER_TRIAL_TIME,
            state_change_conditions={"Tup": "exit"},
            output_actions=[]
        )
        return(self.sma)

    def update_state_numbers(self):
        return self.sma.update_state_numbers()

    def build_message(self):
        return self.sma.build_message()
