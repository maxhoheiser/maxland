from typing import List

from mypy_extensions import TypedDict

from maxland.types_stimuli_definition import Stimulus

RuleDefinition = TypedDict(
    "RuleDefinition",
    {
        "correct": str,
        "wrong": str,
        "conflicting": bool,
        "percentage": float,
    },
)

RuleDefinitionType = List[RuleDefinition]


Rule = TypedDict(
    "Rule",
    {
        "correct": Stimulus,
        "wrong": Stimulus,
        "conflicting": bool,
        "percentage": float,
    },
)

RuleType = List[Rule]


class RuleDefinitionTypes:
    def __init__(self) -> None:
        # rules defined
        self.RULE_A: RuleDefinitionType = list()
        self.RULE_B: RuleDefinitionType = list()