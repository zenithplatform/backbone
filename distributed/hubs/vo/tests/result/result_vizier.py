__author__ = 'civa'

from astroquery.vizier import Vizier

from shared.converters import TableConverter


def run_vizier_all():
    run_vizier()

def run_vizier():
    tables = Vizier.query_region("3C 273", radius="0d6m0s", catalog='GSC')
    # table_list = TableConverter.to_dict_multi(tables)

def process_vizier_result(table):
    dict_collection = TableConverter.extract(table)

    # for single in dict_collection:
    #     ids = Simbad.query_objectids(single["MAIN_ID"])
    #     single['identifiers'] = TableConverter.to_dict(ids, True)['ID']
    #     result = ProviderResult(single, 'Object', 'Simbad')
    #     print(dumper(result, cls=ProviderResultEncoder))

if __name__ == "__main__":
    run_vizier_all()
