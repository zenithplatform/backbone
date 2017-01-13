import json
import numpy
import decimal
from jsonweb.encode import to_object,JsonWebEncoder

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            return (str(o) for o in [o])
        if isinstance(o, float):
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)

class NumPyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(NumPyEncoder, self).default(obj)

'''
Old encoder
'''
class CelestialObjectEncoder(JsonWebEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(CelestialObjectEncoder, self).default(obj)

'''
New encoders
'''
class ProviderResultEncoder(JsonWebEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(ProviderResultEncoder, self).default(obj)