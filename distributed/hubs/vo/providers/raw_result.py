__author__ = 'civa'

from astroquery.simbad.core import SimbadVOTableResult
from astroquery.utils.commons import TableList
from astropy.table.table import Table
from commons.converters import TableConverter
from commons.utils import DictQuery

class RawResult(object):

    def __init__(self):
        self.extracted = None
        self.is_multitable = False
        self.count = 0
        self.context = {}

    def load(self, data):
        if self.extracted:
            del self.extracted[:]

        self.count = 0
        self.is_multitable = False

        if isinstance(data, SimbadVOTableResult):
            self.extracted = TableConverter.convert(data)
        elif isinstance(data, Table):
            self.extracted = TableConverter.convert(data)
        elif isinstance(data, TableList):
            self.is_multitable = True
            result = []
            for table in data:
                result.append(TableConverter.convert(table))

            self.extracted = result
            self.count = len(self.extracted)

    def merge_table(self, table):
        extracted_to_merge = TableConverter.convert(table)

        if extracted_to_merge:
            if isinstance(self.extracted, list):
                for entry in extracted_to_merge:
                    self.extracted.append(entry)

    def foreach(self, func, merge=False, **kwargs):
        for entry in self.extracted:
            func_result = func(entry, **kwargs)

            if not func_result:
                return None

            if func_result.merge:
                merge_input = []

                if isinstance(func_result.func_data, RawCoordinates):
                    entry[func_result.merge_key] = func_result.func_data
                else:
                    merge_input = TableConverter.convert(func_result.func_data)
                    entry[func_result.merge_key] = merge_input

            print(func_result)

class RawCoordinates(object):

    coordinate_patterns = { 'ICRS' : {'ra':'RA_ICRS*', 'dec':'DEC_ICRS*', 'err_angle':'COO_ERR_ANGLE_ICRS*', 'err_maja':'COO_ERR_MAJA_ICRS*', 'err_mina':'COO_ERR_MINA_ICRS*'},
                            'FK5' : {'ra':'RA_FK5*', 'dec':'DEC_FK5*', 'err_angle':'COO_ERR_ANGLE_FK5*', 'err_maja':'COO_ERR_MAJA_FK5*', 'err_mina':'COO_ERR_MINA_FK5*'},
                            'FK4' : {'ra':'RA_FK4*', 'dec':'DEC_FK4*', 'err_angle':'COO_ERR_ANGLE_FK4*', 'err_maja':'COO_ERR_MAJA_FK4*', 'err_mina':'COO_ERR_MINA_FK4*'},
                            'GAL': {'ra':'RA_GAL*', 'dec':'DEC_GAL*', 'err_angle':'COO_ERR_ANGLE_GAL*', 'err_maja':'COO_ERR_MAJA_GAL*', 'err_mina':'COO_ERR_MINA_GAL*'}
    }

    def __init__(self):
        self.all_coordinates = {}

    def add(self, frame, data):
        extracted = TableConverter.convert(data)

        if isinstance(extracted, list) and len(extracted) == 1:
            extracted = extracted[0]

        self.all_coordinates[frame] = extracted

    def get(self, frame, key):
        raw_values = self.all_coordinates[frame]
        patterns = self.coordinate_patterns[frame]

        if key in patterns:
            real_key = patterns[key]
            return DictQuery(raw_values).get(real_key)

class FuncResult():
    def __init__(self, func_data, merge=False, merge_key=''):
        self.func_data = func_data
        self.merge = merge
        self.merge_key = merge_key