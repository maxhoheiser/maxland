from typing import Dict

from mypy_extensions import TypedDict

RuleDefinition = TypedDict(
    "RuleDefinition",
    {
        "correct": bool,
        "conflicting": bool,
    },
)

RuleDefinitionType = Dict[str, RuleDefinition]
