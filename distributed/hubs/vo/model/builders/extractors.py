__author__ = 'civa'

from astropy.coordinates import SkyCoord
from astropy import units as u

from commons.utils import DictQuery
from ...utils.vo_helpers import get_constellation
from ...model.object_types import ObjectTypesLoader


class DimensionsExtractor(object):
    def extract(self, **kwargs):
        otypes = ObjectTypesLoader().load()

        result = kwargs.pop('result')
        otype = otypes.find(result['OTYPE'])

        if otype == 'Star':
            diameter = result['diameter_diameter']
            diameter_unit = result['diameter_unit']

            return {'diameter' : {'value':diameter, 'unit':diameter_unit, 'data_type':type(diameter).__name__}}
        elif otype == 'Galaxy':
            angle = result['GALDIM_ANGLE']
            inclination = result['GALDIM_INCL']
            maj_axis = result['GALDIM_MAJAXIS']
            min_axis = result['GALDIM_MINAXIS']

            return {'dimensions' : {'angle':angle, 'inclination':inclination, 'major_axis':maj_axis, "minor_axis":min_axis}}

class MagnitudesExtractor(object):
    def extract(self, **kwargs):
        result = kwargs.pop('result')

class ColorIndexExtractor(object):

    color_index_table = {'UBV_B_V':'B-V_color_index', 'UBV_U_B': 'U-B_color_index'}

    def extract(self, **kwargs):
        result = kwargs.pop('result')
        bv = result['UBV_B_V']
        ub = result['UBV_U_B']

        return {'color_index' : {'B-V':bv, 'U-B':ub}, 'data_type':type(ub).__name__}

class ProperMotionsExtractor(object):

    def extract(self, **kwargs):
        result = kwargs.pop('result')
        pmra = result['PMRA']
        pmrdec = result['PMDEC']

        return {'proper_motion' : {'declination':pmrdec, 'right_ascension':pmra}, 'data_type':type(pmra).__name__, 'unit':'mas/yr'}

class ConstellationExtractor(object):
    def extract(self, **kwargs):
        ra_ICRS = None
        dec_ICRS = None

        coordinates = kwargs.pop('coordinates')

        if coordinates and coordinates['coordinates'] != 'Unknown':
            icrs = DictQuery(coordinates).get('coordinates/frame', where='ICRS', single=True)
            ra_ICRS = icrs['right_ascension']
            dec_ICRS = icrs['declination']

        if ra_ICRS and dec_ICRS:
            return get_constellation(ra_ICRS,dec_ICRS)

        return None

class CoordinatesExtractor(object):

    def __init__(self):
        self.values = []
        self.skycoord = None

    def extract(self, **kwargs):
        result = kwargs.pop('result')
        raw_coo = result['coordinates']

        self.get_skycoord('ICRS',
                          raw_coo.get('ICRS', 'ra'),
                          raw_coo.get('ICRS', 'dec'))

        for frame, val in raw_coo.all_coordinates.iteritems():
            self.format(frame, raw_coo, val)

        return {'coordinates' : self.values}

    def format(self, frame, raw_coo, raw_values):
        ra = None
        dec = None
        gal_l = None
        gal_b = None
        coo_frame = frame.lower()

        if frame == 'ICRS':
            ra = self.skycoord.fk5.ra
            dec = self.skycoord.fk5.dec
        if frame == 'FK5':
            ra = self.skycoord.fk5.ra
            dec = self.skycoord.fk5.dec
        elif frame== 'FK4':
            ra = self.skycoord.fk4.ra
            dec = self.skycoord.fk4.dec
        elif frame == 'GAL':
            coo_frame = 'galactic'
            gal_l = self.skycoord.galactic.l
            gal_b = self.skycoord.galactic.b

        if frame == 'GAL':
            self.values.append({'frame' : frame,
                                'galactic_latitude' : gal_l.to_string(u.hour),
                                'galactic_latitude_precision' : raw_values['RA_PREC'],
                                'galactic_longitude' : gal_b.to_string(u.degree, alwayssign=True),
                                'galactic_longitude_precision' : raw_values['DEC_PREC'],
                                'error_angle' : raw_coo.get(frame, 'err_angle'),
                                'error_min_axis' : raw_coo.get(frame, 'err_mina'),
                                'error_major_axis' : raw_coo.get(frame, 'err_maja'),
                                'wavelength': self.get_wavelegth(raw_values['COO_WAVELENGTH']) })
        else:
            self.values.append({'frame' : frame,
                                'right_ascension' : ra.to_string(u.hour),
                                'right_ascension_precision' : raw_values['RA_PREC'],
                                'declination' : dec.to_string(u.degree, alwayssign=True),
                                'declination_precision' : raw_values['DEC_PREC'],
                                'error_angle' : raw_coo.get(frame, 'err_angle'),
                                'error_min_axis' : raw_coo.get(frame, 'err_mina'),
                                'error_major_axis' : raw_coo.get(frame, 'err_maja'),
                                'wavelength': self.get_wavelegth(raw_values['COO_WAVELENGTH']) })


    def get_skycoord(self, frame, ra, dec):
        split_char = ' '

        if ':' in ra or ':' in dec:
            split_char = ':'

        self.skycoord = SkyCoord(ra='{}h{}m{}s'.format(*ra.split(split_char)),
                          dec='{}d{}m{}s'.format(*dec.split(split_char)),
                          frame=frame.lower())

    def get_wavelegth(self, acronym):
        wavelength = ''

        #(Rad, mm, IR, Optical, UV, Xray, Gam
        if acronym == 'G':
            wavelength = 'gamma'
        elif acronym == 'X':
            wavelength = 'x-ray'
        elif acronym == 'U':
            wavelength = 'ultra-violet'
        elif acronym == 'O':
            wavelength = 'optical'
        elif acronym == 'I':
            wavelength = 'infra-red'
        elif acronym == 'm':
            wavelength = 'microwave'
        elif acronym == 'R':
            wavelength = 'radio'
        else:
            wavelength = 'unknown'

        return wavelength

class FieldsExtractor(object):

    fields_map_table = {'MAIN_ID':'object_name','OTYPE':'object_type', 'SP_TYPE':'spectral_type',
                        'FLUX_V': 'apparent_magnitude', 'V__vartyp':'variable_type',
                        'oRV_RVel':'radial_velocity', 'PLX_VALUE':'parallax', 'MORPH_TYPE':'morphologycal_type',
                        'Fe_H_Teff':'temperature(effective)', 'Fe_H_log_g':'surface_gravity(log)',
                        'Fe_H_Fe_H':'metalicity', 'Fe_H_CompStar':'metalicity_based_on', 'ROT_Vsini':'rotational_velocity'}

    def __init__(self):
        pass

    def extract(self, **kwargs):
        result = kwargs.pop('result')
        identifiers = result['identifiers']

        new_dict = {}

        for key, value in result.items():
            if key in self.fields_map_table:
                new_dict[self.fields_map_table[key]] = value

        if identifiers:
            new_dict['identifiers'] = identifiers

        return new_dict