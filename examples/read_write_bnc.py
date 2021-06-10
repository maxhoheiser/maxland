from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine

# create bpod object all necessary settings are imported from GUI
bpod = Bpod()

trials = 10

# main loop for 10 trials
for trial in range(trials):

    # create state machine object
    sma = StateMachine(bpod)

    # initial state, all states follow the same notation
    sma.add_state(
        # sate nemae can be freely chosen but must be unique
        state_name="start_state",
        # time how long the state is active can be 0 or seconds or fractions of seconds
        # if 0 state will only change if state change condition is met
        state_timer=1,
        # state change condition for switching to respective next state
        # hast to be a dictionary with keys from allowed conditions and values
        state_change_conditions={"Tup": "next_state"},
        # output actions can be none or list of touples with allowed names and values
        output_actions=[("BNC1", 1), ("BNC2", 1)],
    )

    sma.add_state(
        state_name="next_state",
        state_timer=1,
        state_change_conditions={"Tup": "end_state"},
        output_actions=[],
    )

# start testing for recifing signals
    sma.add_state(
        state_name="end_state",
        state_timer=0,
        # last state always next state to exit
        # state change condition must follow allowed names
        state_change_conditions={"BNC1High": "exit"},
        output_actions=[("BNC1", 1)],
    )



    # Send state machine description to Bpod device
    # as soone as the state machine object is transmitted the states are run
    bpod.send_state_machine(sma)

    # wait until state machine has finished
    if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
        break
    # print some infos about the trial
    print("Current trial info: {0}".format(bpod.session.current_trial))

bpod.close()
