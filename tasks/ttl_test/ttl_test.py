from pybpodapi.bpod import Bpod

from pybpodapi.state_machine import StateMachine

bpod = Bpod()

trials = 10



for trial in range(trials):

    # send ttl to bnc1
    sma = StateMachine(bpod)
    sma.add_state(
        state_name="signal_bnc1",
        state_timer=2,
        state_change_conditions={"Tup": "signal_bnc2"},
        output_actions=[("BNC1", 1)],
    )
    sma.add_state(
        state_name="signal_bnc2",
        state_timer=2,
        state_change_conditions={"Tup": "exit"},
        output_actions=[("BNC2", 1)],
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
