__author__ = 'civa'

import os, time, logging, sys, importlib
from multiprocessing import Process
from local.dynamic.loader import ModuleLoader
from commons.config import JsonConfig

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
pipes = {'receiver': {'receiver': 'Receiver'},
         'agent': {'agent': 'Agent'},
         'producer': {'producer': 'Producer'},
         'dispatcher': {'dispatcher': 'Dispatcher'}
}

class Pipeline(Process):
    def __init__(self, name):
        Process.__init__(self)

        self.ldr = ModuleLoader(__location__)
        self.name = name
        self.running = True
        self.config = JsonConfig()
        self.config.load(filename=os.path.join(__location__, 'pipeline_config.json'))
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def run(self):
        self.start_pipes()
        self.log.info('[%s] pipeline is running at process id: %s\n'
                         % (self.name, os.getpid()))

        while self.running:
            time.sleep(0.1)

        self.log.info('[%s] exited.\n' % (self.name))

    def start_pipes(self):
        self.ldr.find('pipes')

        for name, activation in pipes.iteritems():
            for mod_name, cls in activation.iteritems():
                module, pipe_class = self.ldr.find(mod_name, cls=cls)

                if pipe_class:
                    pipe = pipe_class(name, config=self.config)
                    pipe.start()

    def stop(self):
        self.running = False