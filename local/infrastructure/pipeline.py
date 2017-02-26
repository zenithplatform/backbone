__author__ = 'civa'

import os, time, logging, sys, importlib
from multiprocessing import Process
from local.dynamic.loader import ModuleLoader
from local.infrastructure.pipes import *
from commons.config import JsonConfig

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

pipes = {'receiver': 'receiver.Receiver',
         'distributor': 'distributor.Distributor',
         'executor': 'executor.Executor',
         'emitter': 'emitter.Emitter'
}

class Pipeline(Process):
    def __init__(self, name, config_filename):
        Process.__init__(self)
        self.entry_channels = []
        self.exit_channels = []
        self.ldr = ModuleLoader(__location__)
        self.name = name
        self.running = True
        self.config = JsonConfig()
        self.config.load(filename=os.path.join(__location__, config_filename))
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def setup(self):
        context, channels = ChannelSetup.fromconfig(self.config)
        self.entry_channels = [x for x in channels if x.entry]
        self.exit_channels = [x for x in channels if x.exit]
        self.ldr.find('pipes')

        for name, activation in pipes.iteritems():
            mod, cls = activation.split('.')
            module, pipe_class = self.ldr.find(mod, cls=cls)

            if pipe_class:
                pipe_channels = dict((x.name, x) for x in channels if x.belongs_to == name)
                pipe = pipe_class(self, name, context, pipe_channels, config=self.config)
                pipe.start()

    def exit(self, message):
        for channel in self.exit_channels:
            channel.real_channel.send(message)

    def run(self):
        self.setup()
        self.log.info('[%s] pipeline is running at process id: %s\n' % (self.name, os.getpid()))

        while self.running:
            time.sleep(0.1)

        self.log.info('[%s] exited.\n' % (self.name))

    def stop(self):
        self.running = False


class Supervisor(Process):
    def __init__(self, name):
        Process.__init__(self)
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def run(self):
        self.log.info('Attempting to spawn main pipeline\n')
        pipeline = Pipeline('main', 'pipeline_config.json')
        pipeline.start()

        self.log.info('Running supervisor [%s - %s] for [%s] \n' % (self.name, os.getpid(), pipeline.name))
        while True:
            if not pipeline.is_alive():
                self.log.info('%s exited unexpectedly. Restarting...\n' % (pipeline.name))
                pipeline.start()

            time.sleep(0.1)

