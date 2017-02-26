__author__ = 'civa'

import json
from commons.utils import DictQuery

LOOKUPS  = [
    '*params',
]

class BaseApiParams(object):
    preamble = ''

    def unpack(self, json_data):
        result = []

        if isinstance(json_data, dict):
            result = json_data
        elif isinstance(json_data, basestring):
            result = json.loads(json_data)

        try:
            self.preamble = DictQuery(result).get('*params/preamble')

            if self.preamble:
                return self
            else:
                return None
        except:
            #preamble not found
            return None

    def validate(self, result):
        return DictQuery(result).get("*params")

