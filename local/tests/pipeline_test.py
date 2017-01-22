__author__ = 'civa'
import time, logging, sys, os
sys.path.append('D:\Programming\Astronomy\Dev\Zenith\src\Backend\Local')
from multiprocessing import Process
from local.infrastructure.receiver import Receiver
from local.infrastructure.producer import Producer
from local.infrastructure.pipeline import Pipeline
from local.infrastructure.agent import Agent
from commons.config import JsonConfig
from local.infrastructure.dispatcher import Dispatcher

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def main():
    # pipeline = Pipeline('main')
    # pipeline.run()


    config = JsonConfig()
    config.load(filename=os.path.join(__location__, 'cfg.json'))

    receiver_process = Process(target=start_receiver, args=(config, ))
    agent_process = Process(target=start_agent, args=(config, ))
    dispatcher_process = Process(target=start_dispatcher, args=(config, ))
    producer_process = Process(target=start_producer, args=(config, ))

    receiver_process.start()
    agent_process.start()
    producer_process.start()
    dispatcher_process.start()

    while True:
        time.sleep(0.1)

def start_receiver(config):
    Receiver('receiver', config=config).run()

def start_agent(config):
    Agent('agent', config=config).run()

def start_producer(config):
    Producer('producer', config=config).run()

def start_dispatcher(config):
    Dispatcher('dispatcher', config=config).run()

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
