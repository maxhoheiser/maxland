from pybpodapi.state_machine import StateMachine
from pybpodapi.bpod import Bpod
from pybpod_rotaryencoder_module.module_api import RotaryEncoderModule
import time

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
#settings_folder = os.path.join(session_folder.split('experiments')[0],"tasks","gamble_task_training")
settings_folder =r"C:\maxland_TRAINING01\experiments\gamble_task\setups\gamble_task_training\sessions\20200902-163349"
settings_obj = TrialParameterHandler(usersettings, settings_folder, session_folder)

# create bpod object
bpod=Bpod('COM3')

# create tkinter userinput dialoge window
window = UserInput(settings_obj)
window.draw_window_bevore()
window.show_window()

window = UserInput(settings_obj)
window.draw_window_after()
window.show_window()

print(settings_obj.manual_reward)
print(settings_obj.animal_waight_after)
print(settings_obj.notes)


settings_obj.update_userinput_file()


# rotary encoder
rotary_encoder_module = BpodRotaryEncoder('COM4', settings_obj, bpod)

#test loggin
rotary_encoder_module.rotary_encoder.enable_logging()
rotary_encoder_module.rotary_encoder.disable_logging()
log = rotary_encoder_module.rotary_encoder.get_logged_data()

rotary_encoder_module.load_message()
rotary_encoder_module.configure()

t_end = time.time() + 10
while time.time() < t_end:
    print(rotary_encoder_module.rotary_encoder.current_position())

rotary_encoder_module.enable_stream()
rotary_encoder_module.disable_stream()
stream = rotary_encoder_module.read_stream()


rotary_encoder_module.close()

# direct test
rotary_encoder = RotaryEncoderModule('COM4')
rotary_encoder.enable_stream()
rotary_encoder.enable_logging()
rotary_encoder.disable_logging()
rotary_encoder.disable_stream()
log = rotary_encoder.get_logged_data()




COM_STOP_STREAMANDLOGGING   = ord('X')