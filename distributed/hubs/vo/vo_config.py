__author__ = 'civa'

import os
import json
from commons.singleton import Singleton
from commons.utils import DictQuery
from commons.config import JsonConfig

#@Singleton
class VoConfig(JsonConfig):
    def __init__(self, *args, **kwds):
        super(VoConfig, self).__init__(*args, **kwds)