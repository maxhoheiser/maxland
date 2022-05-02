from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine

trials = 1
time_valve_open = 30
time_inter_trial = 0.5

bpod = Bpod()


for i in range(trials):
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
        state_timer=time_valve_open,
        state_change_conditions={"Tup": "iti"},
        output_actions=[("Valve1", 255)],
    )

    sma.add_state(
        state_name="iti",
        state_timer=time_inter_trial,
        state_change_conditions={"Tup": "exit"},
        output_actions=[],
    )

    bpod.send_state_machine(sma)

    if not bpod.run_state_machine(sma):
        break

    try:
        print(f"Current trial info: {bpod.session.current_trial}")
    except Exception as e:
        print(e)
        break

bpod.close()
