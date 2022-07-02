from typing import Dict

from mypy_extensions import TypedDict

StimulusParameter = TypedDict(
    "StimulusParameter",
    {
        "correct": bool,
        "conflicting": bool,
        "grating_frequency": float,
        "grating_orientation": float,
        "grating_size": float,
        "grating_speed": float,
    },
)

Stimulus = TypedDict(
    "Stimulus",
    {
        "grating_frequency": float,
        "grating_orientation": float,
        "grating_size": int,
        "grating_speed": float,
        "stimulus_id": str,
    },
)

StimulusType = Dict[str, Stimulus]


StimulusHistory = TypedDict(
    "StimulusHistory",
    {
        "correct_side": StimulusParameter,
        "wrong_side": StimulusParameter,
    },
)

StimulusHistoryType = Dict[str, StimulusHistory]
