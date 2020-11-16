#test usersettings dump
import json
import numpy as np

from parameter_handler import TrialParameterHandler
from userinput import UserInput
import usersettings

settings_folder = os.getcwd()
session_folder = os.path.join(settings_folder, "test")
settings_obj = TrialParameterHandler(usersettings, settings_folder, session_folder)

session_name = "1"

file_name = session_name + "usersettings.json"
file_path = os.path.join(session_folder, file_name)

settings_obj.save_usersettings("1")

with open(file_path, "w") as f:
    #json.dump(settings_obj, f)
    #f.write(json.dumps(settings_obj._asdict()))
    f.write(settings_obj.to_json())


print(json.dumps(settings_obj.__dict__, indent=4))

print(settings_obj.to_json())

dictionary = settings_obj.__dict__



# rotary stream test

from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
from rotaryencoder import BpodRotaryEncoder
rotary_encoder_module = RotaryEncoderModule('COM4')

#rotary_encoder_module.enable_stream()
last_position = 0
while True:
    position = rotary_encoder_module.current_position()
    if position != last_position:
        print(rotary_encoder_module.current_position())
    last_position

wrap_point = 0
array = np.array([np.uint8(wrap_point)])
rotary_encoder_module.arcom.write_array([ord('W')] + array )

rotary_encoder_module.set_zero_position()
print(rotary_encoder_module.current_position())
position = []
while True:
    position.append(rotary_encoder_module.current_position())

position = [0,0]
last_position = 0
gain_right =15.25
rotary_encoder_module.set_zero_position()
rotary_encoder_module.enable_stream()
while True:
    stream = rotary_encoder_module.read_stream()
    if len(stream)>0:
        change_position = last_position - stream[-1][2]
        last_position = stream[-1][2]
        # move to the left
        position[0] += int(change_position*gain_right)
        print(position)

rotary_encoder_module.enable_logging()
rotary_encoder_module.disable_logging()

logged_data = rotary_encoder_module.get_logged_data()
print(len(rotary_encoder_module.get_logged_data()))

rotary_encoder_module.close()


log1 = logged_data
log2 = logged_data

# create numpy array
wheel_log = np.empty(shape=[0,4])


, Columns=["trial", "trial index", "timestamp", "position"]




# import custom modules
from stimulus import Stimulus
from probability import ProbabilityConstuctor
from rotaryencoder import BpodRotaryEncoder
from parameter_handler import TrialParameterHandler
from userinput import UserInput

# import usersettings
import usersettings


# create settings object
session_folder = os.getcwd()
settings_folder = os.path.join(session_folder.split('experiments')[0],"tasks","gamble_task_training")
settings_obj = TrialParameterHandler(usersettings, settings_folder, session_folder)

bpod = 

# rotary encoder config
# enable thresholds
rotary_encoder_module = BpodRotaryEncoder('COM4', settings_obj, bpod)
rotary_encoder_module.load_message()
rotary_encoder_module.configure()
rotary_encoder_module.enable_stream()


clamp = lambda n, minn, maxn: max(min(maxn, n), minn)


min(50, 90)
max(min(50, -90), -50)