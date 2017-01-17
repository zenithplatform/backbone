__author__ = 'civa'
import time, logging, sys, os
sys.path.append('D:\Programming\Astronomy\Dev\Zenith\src\Backend\Local')
from multiprocessing import Process
from infrastructure.receiver import Receiver
from infrastructure.agent import Agent
from infrastructure.pipeline import Pipeline
from infrastructure.config import PipelineConfig

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def main():
    # pipeline = Pipeline()
    # pipeline.run()
    config = PipelineConfig()
    config.load(filename=os.path.join(__location__, 'cfg.json'))

    agent_process = Process(target=start_agent, args=(config, ))
    receiver_process = Process(target=start_receiver, args=(config, ))
    #
    agent_process.start()
    receiver_process.start()
    #
    while True:
        time.sleep(0.1)

def start_agent(config):
    Agent('agent', mode='multiplex', config=config).run()

def start_receiver(config):
    Receiver('receiver', config=config).run()

if __name__ == "__main__":
    #start_receiver()
    main()

    # pipeline = {'agent':Agent(), 'receiver':Receiver()}
    #
    # for key, pipe in pipeline.iteritems():
    #     print pipe
    #     print getattr(pipe, 'run')
    #     Process(target=getattr(pipe, 'run'), args=()).start()

    # agent_process = Process(target=start_agent, args=())
    # receiver_process = Process(target=start_receiver, args=())
    #
