__author__ = 'civa'

from jsonweb.encode import to_object
from ..utils import vo_helpers
from ..model.observation_data import *

def celestial_object_collection_encoder(cel_object_collection):
    return {"objects":  cel_object_collection.objects}

def celestial_object_encoder(cel_object):
    return {"object_data":  cel_object.parts}

@to_object(handler=celestial_object_collection_encoder)
class CelestialObjectCollection(object):

    def __init__(self, objects):
        self.objects = objects

@to_object(handler=celestial_object_encoder)
class CelestialObject(object):
    parts = []

    def add_simple_part(self, simple_part):
        self.parts.append(simple_part)

    def add_complex_part(self,complex_part):
        self.parts.append(complex_part)

    def add_multi_part(self,multi_part):
        self.parts.append(multi_part)

    def add_multi_item_value(self, multi_item, value):
        multi_item.add_value(value)

    def add_composite_part(self, composite_part):
        self.parts.append(composite_part)

    def __iter__(self):
        for part in self.parts:
            yield part

    def __init__(self, entry, identifiers):
        del self.parts[:]
        self.create_object_data(entry, identifiers)

    def create_object_data(self, entry, identifiers):
        self.add_simple_part(SimpleItem(
                    'object_name', SimpleValue(
                        entry['MAIN_ID']
                    )
                ))

        self.add_simple_part(SimpleItem(
            'object_type', SimpleValue(
                entry['OTYPE']
            )
        ))

        self.add_simple_part(SimpleItem(
            'constellation', SimpleValue(
                vo_helpers.get_constellation(entry['RA'], entry['DEC'])
            )
        ))

        self.add_simple_part(SimpleItem(
            'declination', SimpleValue(
                entry['DEC']
            )
        ))

        self.add_simple_part(SimpleItem(
            'right_ascension', SimpleValue(
                entry['RA']
            )
        ))

        self.add_simple_part(SimpleItem(
            'spectral_type', SimpleValue(
                entry['SP_TYPE']
            )
        ))

        self.add_simple_part(SimpleItem(
            'B-V_color_index', SimpleValue(
                entry['UBV_B_V']
            )
        ))

        self.add_simple_part(SimpleItem(
            'U-B_color_index', SimpleValue(
                entry['UBV_U_B']
            )
        ))

        self.add_simple_part(SimpleItem(
            'apparent_magnitude', SimpleValue(
                entry['FLUX_V']
            )
        ))

        self.add_simple_part(SimpleItem(
            'variable_type', SimpleValue(
                entry['V__vartyp']
            )
        ))

        self.add_simple_part(SimpleItem(
            'radial_velocity', SimpleValue(
                entry['oRV_RVel']
            )
        ))

        self.add_simple_part(SimpleItem(
            'proper_motion_RA', SimpleValue(
                entry['PMRA']
            )
        ))

        self.add_simple_part(SimpleItem(
            'proper_motion_DEC', SimpleValue(
                entry['PMDEC']
            )
        ))

        self.add_simple_part(SimpleItem(
            'parallax', SimpleValue(
                entry['PLX_VALUE']
            )
        ))

        id_list = []

        for id in identifiers:
            str_id = id['ID']
            id_list.append(SimpleValue(str_id))

        multi = MultiItem('other_identifiers', id_list)
        self.add_multi_part(multi)
