from astroquery.simbad import Simbad
from commons.converters import TableConverter

def run():
    #result = get_coordinates('Betelgeuse')

    #print result
    # Simbad.reset_votable_fields()
    # Simbad.remove_votable_fields('main_id')
    # Simbad.add_votable_fields('coo(:A D;ICRS;J2000)')
    # #Simbad.add_votable_fields('ra(:;A;ICRS;J2000)', 'dec(:;D;ICRS;2000)')
    #
    Simbad.add_votable_fields('otype')
    table = Simbad.query_object('Betelgeuse', wildcard=False)

    print table['OTYPE']
    #
    # print(table)

def get_all_coordinates(main_id):
    coo_default = ['coo(ICRS J2000)', 'coo(FK5 J2000 2000)', 'coo(FK4 ep=B1950 eq=1950)', 'coo(GAL J2000)', 'coo_wavelength', 'dec_prec', 'ra_prec']

    # frames = {'ICRS' : 'coo(ICRS J2000)',
    #           'FK5' : 'coo(FK5 J2000 2000)',
    #           'FK4' : 'coo(FK4 ep=B1950 eq=1950)',
    #           'GAL' : 'coo(GAL J2000)'}

    extract_input = []

    Simbad.reset_votable_fields()
    Simbad.remove_votable_fields('coordinates')
    Simbad.add_votable_fields(*coo_default)

    table = Simbad.query_object(main_id, wildcard=False)

    return TableConverter.extract(table)

    # for frame in frames:
    #     field = frames[frame]
    #     Simbad.add_votable_fields(field)
    #
    #     table = Simbad.query_object(main_id, wildcard=False)
    #     Simbad.remove_votable_fields(field)
    #     extracted_list = TableConverter.extract(table)
    #
    #     for item in extracted_list:
    #         item.pop('MAIN_ID')
    #         extract_input.append(item)
    #
    # return extract_input

def get_coordinates(main_id):
    coo_default = ['coo_wavelength', 'dec_prec', 'ra_prec']

    frames = {'ICRS' : 'coo(ICRS J2000)',
              'FK5' : 'coo(FK5 J2000 2000)',
              'FK4' : 'coo(FK4 B1950 1950)',
              'GAL' : 'coo(GAL J2000)'}

    extract_input = []

    Simbad.reset_votable_fields()
    Simbad.remove_votable_fields('coordinates')
    Simbad.add_votable_fields(*coo_default)

    for frame in frames:
        field = frames[frame]
        Simbad.add_votable_fields(field)

        table = Simbad.query_object(main_id, wildcard=False)
        Simbad.remove_votable_fields(field)
        extracted_list = TableConverter.extract(table)

        for item in extracted_list:
            item.pop('MAIN_ID')
            extract_input.append(item)

    return extract_input

if __name__ == "__main__":
    run()