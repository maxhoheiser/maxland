from typing import Dict, List


class Usersettings:
    def __init__(self) -> None:
        self.TASK: str = ""

        self.GAMBLE_SIDE: str = ""
        self.BLOCKS: Dict[str, List[int]] = dict()

        # reward in seconds
        self.BIG_REWARD: float = float()
        self.SMALL_REWARD: float = float()
        self.LAST_CALLIBRATION: str = ""

        # trial times
        self.TIME_START: float = float()
        self.TIME_WHEEL_STOPPING_CHECK: float = float()
        self.TIME_WHEEL_STOPPING_PUNISH: float = float()
        self.TIME_PRESENT_STIMULUS: float = float()
        self.TIME_OPEN_LOOP: float = float()
        self.TIME_OPEN_LOOP_FAIL_PUNISH: float = float()
        self.TIME_STIMULUS_FREEZE: float = float()
        self.TIME_NO_REWARD: float = float()
        self.TIME_INTER_TRIAL: float = float()
        # confidentiality times
        self.TIME_REWARD: float = float()
        self.TIME_RANGE_OPEN_LOOP_WRONG_PUNISH: List[float] = list()

        # stimulus size and color - only for moving stimulus
        self.STIMULUS_RADIUS: int = int()
        self.STIMULUS_COLOR: List[int] = list()
        self.BACKGROUND_COLOR: List[int] = list()

        # thresholds
        self.ROTARYENCODER_THRESHOLDS: List[int] = list()
        self.STIMULUS_END_POSITION: List[int] = list()

        self.LIFE_PLOT: bool = bool()
        # animal weight in grams
        self.ANIMAL_WEIGHT: int = int()

        # confidentiality task
        self.REWARD: float = float()
        self.TRIAL_NUMBER: int = int()
        self.STIMULUS_TYPE: str = ""
        self.STIMULUS_CORRECT: Dict[str, float] = dict()
        self.STIMULUS_WRONG: Dict[str, float] = dict()

        # insist mode
        self.INSIST_RANGE_TRIGGER: int = int()
        self.INSIST_CORRECT_DEACTIVATE: int = int()
        self.INSIST_RANGE_DEACTIVATE: int = int()

        # rule switching
        self.RULE_SWITCH_INITIAL_WAIT: int = int()
        self.RULE_SWITCH_RANGE: int = int()
        self.RULE_SWITCH_CORRECT: int = int()

        # fade away
        self.FADE_START: int = int()
        self.FADE_END: int = int()
