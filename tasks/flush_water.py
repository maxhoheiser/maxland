from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine

ntrials = 1
valve_on_time = 30
iti = 0.5

bpod = Bpod()


for i in range(ntrials):
    print("Starting trial: ", i + 1)
    sma = StateMachine(bpod)
    sma.add_state(
        state_name="init",
        state_timer=0,
        state_change_conditions={"Tup": "reward"},
        output_actions=[],
    )

    sma.add_state(
        state_name="reward",
        state_timer=valve_on_time,
        state_change_conditions={"Tup": "iti"},
        output_actions=[("Valve1", 255)],
    )

    sma.add_state(
        state_name="iti",
        state_timer=iti,
        state_change_conditions={"Tup": "exit"},
        output_actions=[],
    )

    # Send state machine description to Bpod device
    bpod.send_state_machine(sma)

    # Run state machine
    if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached
        break

    try:
        print("Current trial info: {0}".format(bpod.session.current_trial))
    except:
        pass

bpod.close()
