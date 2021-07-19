from pybpodapi.bpod import Bpod



from pybpodapi.state_machine import StateMachine







bpod = Bpod()







trials = 10



iti = 2











for trial in range(trials):







    # send ttl to bnc1



    sma = StateMachine(bpod)







    # initial state



    #sma.add_state(



     #   state_name="start",



      #  state_timer=5,



       # state_change_conditions={"Tup": "reward"},



        #output_actions=[("BNC1", 1)],



    #)











    # open valve1 for 20 seconds



    sma.add_state(



        state_name="reward",



        # output action will be performed for whole time state is active



        state_timer=100,



        state_change_conditions={"Tup": "exit"},



        # output action for valve open = 255



        # notation for valve alsways Valve + numer of port connected to



        output_actions=[("Valve1", 255)],



    )











    bpod.send_state_machine(sma)







    # Run state machine



    if not bpod.run_state_machine(sma):  # Locks until state machine 'exit' is reached



        break







    print("Current trial info: {0}".format(bpod.session.current_trial))







bpod.close()



