__author__ = 'civa'
import time, logging, sys
sys.path.append('D:\Programming\Astronomy\Dev\Zenith\src\Backend\Local')
from  multiprocessing import Process
from infrastructure.receiver import Receiver
from infrastructure.agent import Agent

def main():
    agent_process = Process(target=start_agent, args=())
    receiver_process = Process(target=start_receiver, args=())
    # pipeline = {'agent':Agent(), 'receiver':Receiver()}
    #
    # for key, pipe in pipeline.iteritems():
    #     print pipe
    #     print getattr(pipe, 'run')
    #     Process(target=getattr(pipe, 'run'), args=()).start()

    # agent_process = Process(target=start_agent, args=())
    # receiver_process = Process(target=start_receiver, args=())
    #
    agent_process.start()
    receiver_process.start()

def start_agent():
    #Agent().run()
    Agent().execute()

def start_receiver():
    #Receiver().run()
    Receiver().execute()

if __name__ == "__main__":
    #start_receiver()
    main()
