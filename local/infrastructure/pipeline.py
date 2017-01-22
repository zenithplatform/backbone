__author__ = 'civa'

import os, time, logging, sys
from multiprocessing import Process
from commons.config import JsonConfig
from .receiver import Receiver
from .agent import Agent
from .producer import Producer
from .dispatcher import Dispatcher

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Pipeline(Process):
    def __init__(self, name):
        Process.__init__(self)

        self.name = name
        self.running = True
        self.config = JsonConfig()
        self.config.load(filename=os.path.join(__location__, 'pipeline_config.json'))
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def run(self):
        Receiver('receiver', config=self.config).run()
        Agent('agent', config=self.config).run()
        Producer('producer', config=self.config).run()
        Dispatcher('dispatcher', config=self.config).run()

        self.log.info('[%s] pipeline is running at process id: %s\n'
                         % (self.name, os.getpid()))

        # while self.running:
        #     time.sleep(0.1)

        #self.log.info('[%s] completed: %f\n' % (self.name, self.number))

    def stop(self):
        self.running = False