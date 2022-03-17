from enum import Enum
from typing import Dict, List, Union

from mypy_extensions import TypedDict

from maxland.types_rule_definition import RuleDefinitionType

Blocks = TypedDict(
    "Blocks",
    {
        "trial_range_block": List[int],
        "prob_reward_gamble_block": float,
        "prob_reward_save_block": float,
    },
)


class TaskName(str, Enum):
    GAMBLE = "gamble"
    CONFIDENTIALITY = "conf"


class StageName(str, Enum):
    HABITUATION = "habituation"
    HABITUATION_COMPLEX = "habituation-complex"
    TRAINING = "training"
    TRAINING_COMPLEX = "training-complex"
    RECORDING = "recording"


class GambleSide(str, Enum):
    LEFT = "left"
    RIGHT = "right"


class StimulusTypes(str, Enum):
    ONE = "one-stimulus"
    TWO = "two-stimuli"
    THEE = "three-stimuli"


class UsersettingsTypes:
    def __init__(self) -> None:
        self.TASK: TaskName = TaskName()
        self.STAGE: StageName = StageName()

        self.GAMBLE_SIDE: Union[GambleSide, None] = None
        self.BLOCKS: List[Blocks] = list()

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
        self.TIME_RANGE_NO_REWARD_PUNISH: List[float] = list()

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

        # stimulus predefined
        self.STIMULUS_TYPE: Union[StimulusTypes, None] = None
        self.STIMULUS_CORRECT: Dict[str, float] = dict()
        self.STIMULUS_WRONG: Dict[str, float] = dict()

        # rules defined
        self.RULE_A: RuleDefinitionType = list()
        self.RULE_B: RuleDefinitionType = list()

        # insist mode
        self.INSIST_RANGE_TRIGGER: int = int()
        self.INSIST_CORRECT_DEACTIVATE: int = int()
        self.INSIST_RANGE_DEACTIVATE: int = int()

        # rule switching

        self.RULE_SWITCH_INITIAL_TRIALS_WAIT: int = int()
        self.RULE_SWITCH_CHECK_TRIAL_RANGE: int = int()
        self.RULE_SWITCH_TRIALS_CORRECT_TRIGGER_SWITCH: int = int()

        # fade away
        self.FADE_START: int = int()
        self.FADE_END: int = int()
