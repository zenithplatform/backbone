__author__ = 'civa'

import os, time
from multiprocessing import Process
from commons.config import JsonConfig
from .receiver import Receiver
from .agent import Agent

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Pipeline(object):
    def __init__(self):
        # root = os.path.abspath(os.path.join(__file__ ,"../../.."))
        # filename = os.path.join(root, 'vo_config.json')
        #os.path.join(__file__ ,"../../..")
        self.config = JsonConfig()
        self.config.load(filename=os.path.join(__location__, 'pipeline_config.json'))

        #Receiver('receiver', self.config).open()
        #Agent('agent', self.config).open()
        Process(target=self.run_agent, args=()).start()
        Process(target=self.run_receiver, args=()).start()

        #agent_process.start()
        #receiver_process.start()

        while True:
            time.sleep(0.1)

    def run(self):
        pass

    def run_receiver(self):
        Receiver('receiver', config=self.config).open()

    def run_agent(self):
        Agent('agent', polling=True, config=self.config).open()