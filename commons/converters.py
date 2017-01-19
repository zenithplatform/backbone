__author__ = 'civa'

from astropy.coordinates import SkyCoord  # High-level coordinates
from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
from astropy.coordinates import Angle, Latitude, Longitude  # Angles
import astropy.units as u

class CoordinatesConverter:
    @staticmethod
    def convert(coordinates):
        return SkyCoord(coordinates, ICRS)

class TableConverter:
    @staticmethod
    def convert(table):
        dict_collection = []

        if len(table.colnames) == 1:
            name = table.colnames[0]
            return table[name].tolist()
        else:
            for row in table:
                total_data = {}

                for col in table.colnames:
                    total_data[col] = row[col]

                dict_collection.append(total_data)

        return dict_collection

