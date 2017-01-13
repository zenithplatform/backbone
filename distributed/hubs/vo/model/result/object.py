__author__ = 'civa'

from jsonweb.encode import to_object

def obj_value_encoder(obj_value):
    return { obj_value.name : { "value": obj_value.value,
                                "unit": obj_value.unit,
                                # "error": obj_value.error,
                                # "precision": obj_value.precision,
                                "data_type": obj_value.datatype}
    }

@to_object(handler=obj_value_encoder)
class ObjectValue(object):
    name = ''
    value = None
    unit = ''
    error = ''
    precision = ''
    datatype = ''

    def __init__(self, name, val):
        self.name = name
        self.value = val
        self.datatype = type(val).__name__