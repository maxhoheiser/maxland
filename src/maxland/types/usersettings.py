from typing import Dict, List


class Usersettings:
    def __init__(self) -> None:
        self.TASK = str

        self.GAMBLE_SIDE = str
        self.BLOCKS = Dict[str, List[int]]

        # reward in seconds
        self.BIG_REWARD = float
        self.SMALL_REWARD = float
        self.LAST_CALLIBRATION = str

        # trial times
        self.TIME_START = float
        self.TIME_WHEEL_STOPPING_CHECK = float
        self.TIME_WHEEL_STOPPING_PUNISH = float
        self.TIME_PRESENT_STIMULUS = float
        self.TIME_OPEN_LOOP = float
        self.TIME_OPEN_LOOP_FAIL_PUNISH = float
        self.TIME_STIMULUS_FREEZE = float
        self.TIME_REWARD = float
        self.TIME_NO_REWARD = float
        self.TIME_INTER_TRIAL = float
        # confidentiality times
        self.TIME_REWARD = float
        self.TIME_RANGE_OPEN_LOOP_WRONG_PUNISH = List[float]

        # stimulus size and color - only for moving stimulus
        self.STIMULUS_RADIUS = int
        self.STIMULUS_COLOR = List[int]
        self.BACKGROUND_COLOR = List[int]

        # thresholds
        self.ROTARYENCODER_THRESHOLDS = List[int]
        self.STIMULUS_END_POSITION = List[int]

        self.LIFE_PLOT = bool
        # animal weight in grams
        self.ANIMAL_WEIGHT = int

        # confidentiality task
        self.REWARD = float
        self.TRIAL_NUMBER = int
        self.STIMULUS_TYPE = str
        self.STIMULUS_CORRECT = Dict[str, float]
        self.STIMULUS_WRONG = Dict[str, float]

        # insist mode
        self.INSIST_RANGE_TRIGGER = int
        self.INSIST_CORRECT_DEACTIVATE = int
        self.INSIST_RANGE_DEACTIVATE = int

        # rule switching
        self.RULE_SWITCH_INITIAL_WAIT = int
        self.RULE_SWITCH_RANGE = int
        self.RULE_SWITCH_CORRECT = int

        # fade away
        self.FADE_START = int
        self.FADE_END = int
