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
        state_timer=5,
        state_change_conditions={"Tup": "reward"},
        output_actions=[("BNC1", 1)],
    )


    # open valve1 for 10 seconds
    sma.add_state(
        state_name="reward",
        state_timer=20,
        state_change_conditions={"Tup": "exit"},
        output_actions=[("Valve2", 255)],
    )


    bpod.send_state_machine(sma)

    # Run state machine
    if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
        break
    print("test ob das geprintet wird\n")
    print("Current trial info: {0}".format(bpod.session.current_trial))

bpod.close()

if __name__ == "__main__":
    print("main")
