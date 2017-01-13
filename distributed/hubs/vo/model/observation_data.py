__author__ = 'civa'

from jsonweb.encode import to_object, dumper, to_list

def complex_value_encoder(complex_value):
    return {"$type": "ComplexValue",
            "value": complex_value.value,
            "unit":  complex_value.unit,
            "error": complex_value.error}

def complex_item_encoder(complex_item):
    return {"name": complex_item.name,
            "values":  complex_item.complex_values}

def multi_item_encoder(multi_item):
    return {"name": multi_item.name,
            "values":  multi_item.simple_values}

def simple_item_encoder(simple_item):
    return {"name": simple_item.name,
            "values": simple_item.simple_values}

def simple_value_encoder(simple_value):
    return {"value": simple_value.value}

@to_object(suppress=["__type__"], handler=complex_value_encoder)
class ComplexValue(object):
    value = None
    unit = ''
    error = ''

    def __init__(self, value, unit, error):
        self.value = value
        self.unit = unit
        self.error = error

@to_object(suppress=["__type__"], handler=simple_value_encoder)
class SimpleValue(object):
    value = None

    def __init__(self, value):
        self.value = value

@to_object(suppress=["__type__"], handler=simple_item_encoder)
class SimpleItem(object):
    name = ''
    simple_values = None

    def __init__(self, name, *simple_values):
        self.name = name
        self.simple_values = simple_values

@to_object(suppress=["__type__"], handler=complex_item_encoder)
class ComplexItem(object):
    name = ''
    complex_values = None

    def __init__(self, name, *complex_values):
        self.name = name
        self.complex_values = complex_values

@to_object(suppress=["__type__"], handler=multi_item_encoder)
@to_list()
class MultiItem(object):
    name = ''
    simple_values = None

    def __init__(self, name, simple_values):
        self.name = name
        self.simple_values = simple_values

    def __iter__(self):
        for simple_value in self.simple_values:
            yield simple_value