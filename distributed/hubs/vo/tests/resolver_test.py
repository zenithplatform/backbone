__author__ = 'civa'

import os, json
from distributed.hubs.vo.providers.resolver import Resolver
from distributed.hubs.vo.providers.params import BaseVOParams
from distributed.hubs.vo.vo_config import VoConfig

def resolve():
    root = os.path.abspath(os.path.join(__file__ ,"../.."))
    filename = os.path.join(root, 'vo_config.json')

    #VoConfig().load(filename=filename)
    config = VoConfig()
    config.load(filename=filename)
    resolver = Resolver(config)

    f = file('resolver_requests.txt', "r")
    json_params = json.load(f)
    f.close()

    base = BaseVOParams()
    request = base.unpack(json_params)
    resolver.resolve(request)

if __name__ == "__main__":
    resolve()
