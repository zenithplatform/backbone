__author__ = 'civa'

from jsonweb.encode import to_object
from ...model.builders.result_builders import ResultBuilder

def result_encoder(provider_result):
    type = provider_result.type

    if type == 'Object':
        return {"objects":  provider_result.body}
    elif type == 'Catalog':
        return {"catalogs":  provider_result.body}

@to_object(handler=result_encoder)
class ProviderResult(object):
    type = ''
    body = []

    def __init__(self, result, type, provider):
        self.type = type
        builder_input = {'result': result, 'provider': provider, 'type': type}

        builder = ResultBuilder()
        self.body = builder.execute(**builder_input)
