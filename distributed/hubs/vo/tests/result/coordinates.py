__author__ = 'civa'

from astroquery.simbad import Simbad

from commons.converters import TableConverter
from distributed.hubs.vo.model.builders.extractors import CoordinatesExtractor


def run_simbad_all():
    result_test_coordinates()

def result_test_coordinates():
    # frames = {'ICRS' : [ 'ra(:;A;ICRS;J2000)', 'dec(:;D;ICRS)'],
    #           'FK5' : [ 'ra(:;A;FK5;J2000)', 'dec(:;D;FK5;2000)'],
    #           'FK4' : [ 'ra(:;A;FK4;B1950)', 'dec(:;D;FK4;1950)'],
    #           'GAL' : [ 'ra(:;A;GAL;J2000)', 'dec(:;D;GAL)']}

    coo_default = ['coo_wavelength']

    frames = {'ICRS' : 'coo(ICRS J2000)',
              'FK5' : 'coo(FK5 J2000 2000)',
              'FK4' : 'coo(FK4)',
              'GAL' : 'coo(GAL J2000)'}

    extract_input = []

    Simbad.reset_votable_fields()
    Simbad.remove_votable_fields('coordinates')
    Simbad.add_votable_fields(*coo_default)

    for frame in frames:
        field = frames[frame]
        Simbad.add_votable_fields(field)
        print Simbad._VOTABLE_FIELDS
        table = Simbad.query_object("Vega", wildcard=False)
        Simbad.remove_votable_fields(field)
        extracted_list = TableConverter.extract(table)

        for item in extracted_list:
            item.pop('MAIN_ID')
            extract_input.append(item)

    print CoordinatesExtractor('coordinates', extract_input).get_coordinates()

if __name__ == "__main__":
    run_simbad_all()