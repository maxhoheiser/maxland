from typing import List

from mypy_extensions import TypedDict

TimeDict = TypedDict(
    "TimeDict",
    {
        "time_start": float,
        "time_wheel_stopping_check": float,
        "time_wheel_stopping_punish": float,
        "time_present_stimulus": float,
        "time_open_loop": float,
        "time_open_loop_fail_punish": float,
        "time_stimulus_freeze": float,
        "time_no_reward": float,
        "time_inter_trial": float,
        "time_range_no_reward_punish": List[float],
        "time_reward_waiting": float,
        "time_reward": float,
        "time_big_reward_waiting": float,
        "time_big_reward_open": float,
        "time_small_reward_open": float,
        "time_small_reward_waiting": float,
        "time_reward_open": float,
    },
)
