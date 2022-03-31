RULE_A = [
    {
        "correct": "a00b03",
        "wrong": "a03b03",
        "conflicting": False,
        "percentage": 0.5,
    },
    {
        "correct": "a00b03",
        "wrong": "a03b03",
        "conflicting": False,
        "percentage": 0.3,
    },
]

RULE_B = [
    {
        "correct": "a00b01",
        "wrong": "a03b01",
        "conflicting": True,
        "percentage": 0.8,
    },
    {
        "correct": "a03b03",
        "wrong": "a03b01",
        "conflicting": True,
        "percentage": 0.2,
    },
]
