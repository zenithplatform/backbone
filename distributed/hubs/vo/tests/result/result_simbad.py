__author__ = 'civa'

import os

from astroquery.simbad import Simbad
from jsonweb.encode import dumper

from shared.converters import TableConverter
from shared.serialization import ProviderResultEncoder
from hubs.vo.model.result.base import ProviderResult
from hubs.vo.vo_config import VoConfig
from hubs.vo.providers.raw_result import RawResult, FuncResult, RawCoordinates


def run_simbad_all():
    #run_default()
    result_test_single()
    #result_test_multi()
    #result_test_coordinates()

def run_default():
    Simbad.add_votable_fields('rot')#,"jp11","dim",
    table = Simbad.query_object("Vega", wildcard=False)

    dict_collection = TableConverter.convert(table)
    print dict_collection

def result_test_single():
    root = os.path.abspath(os.path.join(__file__ ,"../../.."))
    filename = os.path.join(root, 'vo_config.json')

    config = VoConfig()
    config.load(filename=filename)

    fields = config.find("configuration/providers/Simbad/search_fields")
    Simbad.add_votable_fields(*fields)
    Simbad.remove_votable_fields('coordinates')

    table = Simbad.query_object("Vega", wildcard=False)

    result = RawResult()
    result.load(table)
    result.foreach(get_all_coordinates)
    result.foreach(get_identifiers)
    result.foreach(get_result)

def get_identifiers(context, **kwargs):
    ids = Simbad.query_objectids(context["MAIN_ID"])
    return FuncResult(ids, merge=True, merge_key='identifiers')
    #context['identifiers'] = TableConverter.to_dict(ids, True)['ID']

def get_all_coordinates(context, **kwargs):
    coordinates = RawCoordinates()
    main_id = context['MAIN_ID']
    coo_default = ['coo_wavelength', 'dec_prec', 'ra_prec']

    frames = {'ICRS' : 'coo(ICRS J2000)',
              'FK5' : 'coo(FK5 J2000 2000)',
              'FK4' : 'coo(FK4 B1950 1950)',
              'GAL' : 'coo(GAL J2000)'}

    extract_input = []

    Simbad.reset_votable_fields()
    Simbad.add_votable_fields(*coo_default)
    Simbad.remove_votable_fields('coordinates', 'main_id')

    for frame in frames:
        field = frames[frame]
        Simbad.add_votable_fields(field)

        table = Simbad.query_object(main_id, wildcard=False)
        coordinates.add(frame, table)
        Simbad.remove_votable_fields(field)

    return FuncResult(coordinates, merge=True, merge_key='coordinates')

def get_result(context, **kwargs):
    result = ProviderResult(context, 'Object', 'Simbad')
    print(dumper(result, cls=ProviderResultEncoder))

def result_test_multi():
    root = os.path.abspath(os.path.join(__file__ ,"../../.."))
    filename = os.path.join(root, 'vo_config.json')

    config = VoConfig()
    config.load(filename=filename)

    fields = config.find("configuration/providers/Simbad/search_fields")

    for field in fields:
        Simbad.add_votable_fields(field)

    Simbad.ROW_LIMIT = 3
    table = Simbad.query_region("05h35m17.3s -05h23m28s", radius='0d10m0s')
    process_simbad_result(table)

if __name__ == "__main__":
    run_simbad_all()