import json
import os

# create stimuli definitions
spatial_frequencies = [0.01, 0.1, 0.2, 0.3]
orientations = [0, 30, 60, 90]

spatial_frequencies_defintion = dict()
for i in range(len(spatial_frequencies)):
    key = f"a{i:02}"
    value = spatial_frequencies[i]
    spatial_frequencies_defintion[key] = value


orientations_defintion = dict()
for i in range(len(orientations)):
    key = f"b{i:02}"
    value = orientations[i]
    orientations_defintion[key] = value


combinations = dict()
for sf_key, sf_value in spatial_frequencies_defintion.items():
    for ori_key, ori_value in orientations_defintion.items():
        key = f"{sf_key}{ori_key}"
        combinations[key] = {
            "grating_frequency": sf_value,
            "grating_orientation": ori_value,
        }

file_path = os.path.join(os.getcwd(), "stimuli_definition.json")
with open(file_path, "w") as f:
    json.dump(combinations, f, indent=4)


# create rules definition
rule_a = {
    "a00b03": {
        "correct": True,
        "conflicting": False,
    },
    "a00b02": {
        "correct": True,
        "conflicting": False,
    },
    "a00b01": {
        "correct": True,
        "conflicting": False,
    },
    "a00b00": {
        "correct": True,
        "conflicting": False,
    },
    "a03b03": {
        "correct": False,
        "conflicting": False,
    },
    "a03b02": {
        "correct": False,
        "conflicting": False,
    },
    "a03b01": {
        "correct": False,
        "conflicting": False,
    },
    "a03b00": {
        "correct": False,
        "conflicting": False,
    },
}

rule_b = {
    "a00b03": {
        "correct": False,
        "conflicting": False,
    },
    "a00b02": {
        "correct": False,
        "conflicting": False,
    },
    "a00b01": {
        "correct": False,
        "conflicting": False,
    },
    "a00b00": {
        "correct": False,
        "conflicting": False,
    },
    "a03b03": {
        "correct": True,
        "conflicting": False,
    },
    "a03b02": {
        "correct": True,
        "conflicting": False,
    },
    "a03b01": {
        "correct": True,
        "conflicting": False,
    },
    "a03b00": {
        "correct": True,
        "conflicting": False,
    },
}


all_rules = {"rule_a": rule_a, "rule_b": rule_b}
file_path = os.path.join(os.getcwd(), "rules_definition.json")
with open(file_path, "w") as f:
    json.dump(all_rules, f, indent=4)
