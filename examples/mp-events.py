import multiprocessing
import time

def wait_for_event(e):
    """Wait for the event to be set before doing anything"""
    print('wait_for_event: starting')
    e.wait()
    print('wait_for_event: e.is_set()->', e.is_set())

def wait_for_event_timeout(e, t):
    """Wait t seconds and then timeout"""
    print('wait_for_event_timeout: starting')
    e.wait(t)
    print('wait_for_event_timeout: e.is_set()->', e.is_set())


if __name__ == '__main__':
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(name='block', 
                                 target=wait_for_event,
                                 args=(e,))
    w1.start()

    w2 = multiprocessing.Process(name='non-block', 
                                 target=wait_for_event_timeout, 
                                 args=(e, 2))
    w2.start()

    print('main: waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    print('main: event is set')



flag1 = multiprocessing.Value('b',True)



import multiprocessing
import time

mng = multiprocessing.Manager()
#global run_closed_loop
global mv
mv = mng.Value('b',True)

def tester():
    time.sleep(5)
    global mv
    mv.value=False

mp = multiprocessing.Process(target=tester)
mp.start()

for i in range(6):
    print(mv.value)
    time.sleep(1)