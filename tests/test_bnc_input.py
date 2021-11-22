from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine

# create bpod object all necessary settings are imported from GUI
bpod = Bpod()

trials = 10

# main loop for 10 trials
for trial in range(trials):

    # create state machine object
    sma = StateMachine(bpod)
    # test output signal 00
    sma.add_state(
        state_name="start",
        state_timer=1,
        state_change_conditions={"Tup": "state_02"},
        output_actions=[("BNC1", 1), ("BNC2", 1)],
    )

    # start testing for recifing signals
    sma.add_state(
        state_name="end_state",
        state_timer=10,
        # last state always next state to exit
        state_change_conditions=[{"BNC1High": "exit"},{"BNC2High":"exit"}],
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
