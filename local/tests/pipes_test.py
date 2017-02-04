__author__ = 'civa'

import os
from commons.config import JsonConfig
from local.infrastructure.pipes import *
from local.infrastructure.distributor import Distributor
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def main():
    channel_setup_test()
    #pipe_setup_test()

def channel_setup_test():
    config = JsonConfig()
    config.load(filename=os.path.join(__location__, 'cfg.json'))

    context, channels = ChannelSetup.fromconfig(config=config)

    descriptor = Distributor('agent', context, channels, config)
    #agent_channels = dict((x.channel_name, x) for x in all_channels if not x.exit and x.belongs_to == 'agent')
    #self.channels = dict(map(lambda x : [x.channel_name, x] if not x.exit else None, channels))
    #agent = Agent('agent', _context, all_channels, mode='multiplex')

    print 'test'

def pipe_setup_test():
    config = JsonConfig()
    config.load(filename=os.path.join(__location__, 'cfg.json'))
    pipe_descriptor = PipeSetup.create('agent', config)
    agent = Distributor(pipe_descriptor)

    print 'test'

if __name__ == "__main__":
    main()
