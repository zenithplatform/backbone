__author__ = 'civa'

import json, random
from json import JSONEncoder

class PipeMessageEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

class PipeMessage(object):
    def __init__(self, raw_input):
        self._unwrap(raw_input)
        self.valid = self._validate()

    def read_body(self, key):
        if key in self.body:
            return self.body[key]

        return None

    def write_body(self, **kwargs):
        new_body = {}

        for key, val in kwargs.iteritems():
            new_body[key] = val

        self.body = new_body

    def reprJSON(self):
        return dict(body=self.body, metadata=self.meta)

    def _local_token(self):
        return ''

    def _validate(self):
        #FOR TESTING PURPOSES ONLY!!!!
        #DELETE AFTER
        return bool(random.getrandbits(1))
        #return (self.token == self._local_token())

    def _flatten_body(self, raw_body):
        result = {}

        if not raw_body:
            return

        if isinstance(raw_body, dict):
            for key, val in raw_body.iteritems():
                result[key] = val

        return result

    def _unwrap(self, raw_input):
        _dict = {}

        if isinstance(raw_input, basestring):
            _dict = json.loads(raw_input)
        else:
            _dict = raw_input

        self.body = self._flatten_body(_dict['body'])
        self.meta = _dict['metadata']

        if self.meta:
            self.request_id = self.meta['request_id']
            self.token = self.meta['token']
            self.execution_info = self.meta['execution_info']