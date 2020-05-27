from pybpodapi.bpod import Bpod

from pybpodapi.state_machine import StateMachine

bpod = Bpod()

trials = 10
iti = 2


for trial in range(trials):

    # send ttl to bnc1
    sma = StateMachine(bpod)
# initial state blink = trial start
    sma.add_state(
        state_name="signal_bnc1",
        state_timer=1,
        state_change_conditions={"Tup": "iti"},
        output_actions=[("BNC1", 1)],
    )

    sma.add_state(
        state_name="iti",
        state_timer=1,
        state_change_conditions={"Tup": "wait_input"},
        output_actions=[],
    )

# start testing for recifing signals
    sma.add_state(
        state_name="wait_input",
        state_timer=0,
        state_change_conditions={"BNC1High": "exit"},
        output_actions=[("BNC1", 1)],
    )



    # Send state machine description to Bpod device
    bpod.send_state_machine(sma)

    # Run state machine
    if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
        break
    print("test ob das geprintet wird\n")
    print("Current trial info: {0}".format(bpod.session.current_trial))

bpod.close()

if __name__ == "__main__":
    print("main")
