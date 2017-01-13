__author__ = 'civa'

import json
from shared.api import BaseApiParams
from shared.enums import Target
from shared.converters import CoordinatesConverter
from shared.utils import DictQuery

class BaseVOParams(BaseApiParams):
    term = ''
    target = Target.Object

    def unpack(self, json_data):
        result = json.loads(json_data)

        super(BaseVOParams, self).unpack(json_data)

        if not super(BaseVOParams, self).validate(result):
            return None

        if result and ('vo_params' in result):
            self.term = DictQuery(result).get('vo_params/term')
            self.target = DictQuery(result).get('vo_params/target')
        else:
            return None

        if self.target == Target.tostring(0):
            self.__class__ = ObjectParams
        else:
            self.__class__ = CatalogParams

        return self.unpack(json_data)

class ObjectParams(BaseVOParams):
    exact = False
    cone = False
    radius = ''
    coordinates = None
    epoch = ''
    equinox = 0
    catalog_filter = []

    def __str__(self):
        if self.cone:
            return "Search term : {0}, radius : {1}, coordinates : {2}".format(self.term, self.radius, self.coordinates)
        else:
            return "Search term : {0}".format(self.term)

    def unpack(self, json_data):
        result = json.loads(json_data)

        if result and ('vo_params' in result):
            self.exact = DictQuery(result).get('vo_params/exact')
            self.cone = DictQuery(result).get('vo_params/cone')

            if self.cone:
                self.radius = DictQuery(result).get('vo_params/radius')
                coordinates_str = DictQuery(result).get('vo_params/coordinates')

                if coordinates_str:
                    self.coordinates = CoordinatesConverter.convert(coordinates_str)

                self.epoch = DictQuery(result).get('vo_params/epoch')
                self.equinox = DictQuery(result).get('vo_params/equinox')
                self.catalog_filter = DictQuery(result).get('vo_params/catalog_filter')
        else:
            return None

        return self

class CatalogParams(BaseVOParams):
    obsolete_catalogs = False
    all = False
    def unpack(self, json_data):
        result = json.loads(json_data)

        if result and ('vo_params' in result):
            self.obsolete_catalogs = DictQuery(result).get('vo_params/obsolete_catalogs')
            self.all = DictQuery(result).get('vo_params/all')
        else:
            return None

        return self

class ImageParams(BaseVOParams):
    '''
    position='22:57:00,62:38:00',survey=['DSS2 Blue','DSS2 IR','DSS2 Red'],pixels='2400,2400',coordinates='J2000',grid=True,gridlabels=True
    '''
    '''
    term should be either in format like this : '22:57:00,62:38:00', or name of the object
    '''
    coordinates = None
    survey = []

    def unpack(self, json_data):
        result = json.loads(json_data)

        if result and ('vo_params' in result):
            self.coordinates = DictQuery(result).get('vo_params/coordinates')
            self.survey = DictQuery(result).get('vo_params/survey')
        else:
            return None

        return self