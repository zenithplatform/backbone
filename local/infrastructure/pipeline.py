__author__ = 'civa'

import os, time, logging, sys, importlib
from multiprocessing import Process
from local.dynamic.loader import ModuleLoader
from local.infrastructure.pipes import *
from commons.config import JsonConfig

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

pipes = {'receiver': {'receiver': 'Receiver'},
         'distributor': {'distributor': 'Distributor'},
         'executor': {'executor': 'Executor'},
         'emitter': {'emitter': 'Emitter'}
}

class Pipeline(Process):
    def __init__(self, name, config_filename):
        Process.__init__(self)
        self.channels = []
        self.ldr = ModuleLoader(__location__)
        self.name = name
        self.running = True
        self.config = JsonConfig()
        self.config.load(filename=os.path.join(__location__, config_filename))
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def setup(self):
        context, channels = ChannelSetup.fromconfig(self.config)
        self.pipeline_entry_channels = [x for x in channels if x.entry]
        self.pipeline_exit_channels = [x for x in channels if x.exit]
        self.ldr.find('pipes')

        for name, activation in pipes.iteritems():
            for mod_name, cls in activation.iteritems():
                module, pipe_class = self.ldr.find(mod_name, cls=cls)

                if pipe_class:
                    pipe_channels = dict((x.name, x) for x in channels if x.belongs_to == name)
                    pipe = pipe_class(self, name, context, pipe_channels, config=self.config)
                    pipe.start()

    def exit(self, message):
        for exit_channel in self.pipeline_exit_channels:
            exit_channel.real_channel.send(message)

    def run(self):
        self.setup()
        self.log.info('[%s] pipeline is running at process id: %s\n'
                         % (self.name, os.getpid()))

        while self.running:
            time.sleep(0.1)

        self.log.info('[%s] exited.\n' % (self.name))

    def stop(self):
        self.running = False