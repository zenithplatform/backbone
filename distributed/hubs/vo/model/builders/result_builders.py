__author__ = 'civa'
# -*- coding: iso-8859-15 -*-

from ...model.result.object import ObjectValue
from ...model.builders.extractors import *

class ObjectBuilder:
    # unit_map_table = {'declination' : 'degrees [° ′ ″]',
    #                   'right_ascension' : 'hms [h m s]',
    #                   'radial_velocity':'km/s',
    #                   'proper_motion_RA': 'mas/yr',
    #                   'proper_motion_DEC': 'mas/yr',
    #                   'parallax': 'mas'}
    #
    # error_map_table = {'declination' : 'degrees [° ′ ″]',
    #                    'right_ascension' : 'hms [h m s]',
    #                    'radial_velocity':'km/s',
    #                    'proper_motion_RA': 'mas/yr',
    #                    'proper_motion_DEC': 'mas/yr',
    #                    'parallax': 'mas'}

    def __init__(self):
        pass

    def execute(self, **kwargs):
        provider = kwargs['provider']

        if provider == 'Simbad':
            return self.execute_simbad(**kwargs)

    def execute_simbad(self, **kwargs):
        values = []
        fields = FieldsExtractor().extract(**kwargs)

        for key, value in fields.iteritems():
            val = ObjectValue(key, value)
            values.append(val)

        coordinates = CoordinatesExtractor().extract(**kwargs)
        values.append(coordinates)

        proper_motions = ProperMotionsExtractor().extract(**kwargs)
        values.append(proper_motions)

        color_index = ColorIndexExtractor().extract(**kwargs)
        values.append(color_index)

        dimensions = DimensionsExtractor().extract(**kwargs)
        values.append(dimensions)

        constellation = ConstellationExtractor().extract(**{'coordinates': coordinates})
        values.append(ObjectValue('constellation', constellation))

        return values

class CatalogBuilder:
    def __init__(self):
        pass

class ResultBuilder:

    def __init__(self):
        pass

    def execute(self, **kwargs):
        type = kwargs['type']

        if type == 'Object':
            object_builder = ObjectBuilder()
            return object_builder.execute(**kwargs)
        elif type == 'Catalog':
            return None
