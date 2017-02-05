__author__ = 'civa'

import os, sys,logging, logging.config
from commons.config import JsonConfig

class BaseProcessor(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        if 'execution_dir' in self.kwargs:
            self.execution_dir = self.kwargs.pop('execution_dir', '')

    def configure(self, config_file=''):
        self.config = JsonConfig()

        if not self.execution_dir:
            return

        if not config_file:
            self.config.load(filename=os.path.join(self.execution_dir, 'processor_config.json'))
        else:
            self.config.load(filename=os.path.join(self.execution_dir, config_file))

        self._configure_logging()

    def _configure_logging(self):
        section = self.config.find('configuration/logging')

        if section:
            logging.config.dictConfig(section)
        else:
            logging.basicConfig(level=logging.INFO)

        self.log = logging.getLogger(__name__)

    def process(self, processing_input):
        pass