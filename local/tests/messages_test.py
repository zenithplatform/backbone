__author__ = 'civa'

import json
from local.infrastructure.messages import PipeMessage, PipeMessageEncoder

def main():
    json_str = '{"body": {"name": "Test", "number": 12}, "metadata": {"token": "8d44ca18620c1aa", "execution_info": {"processor": "fits"}, "request_id": "8d44ca18620c1aa"}}'
    json_obj = json.loads(json_str)

    msg = PipeMessage(json_obj)
    result = json.dumps(msg, cls=PipeMessageEncoder)

    print 'test'

if __name__ == "__main__":
    main()
