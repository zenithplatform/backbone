__author__ = 'civa'

from astroquery.vizier import Vizier

from vo_hub.search_providers.vizier import VizierSearch


def create_vizier_metafile():
    result = Vizier.query_object("sirius")

    text_file = open("D:\\Programming\\Astronomy\\VizierMeta.txt", "w")
    text_file.truncate()

    for table in result:
        #print table.colnames
        text_file.write('(' + table.meta['name'] + ') ' + table.meta['description'] + '\n')

        for col in table.colnames:
            text_file.write('\t' + col + '\n')

        text_file.write('\n')
        text_file.write('\n')
        #print table.colnames
        #print table.meta['description']

    text_file.close()
    #table = result['V/109/sky2kv4']

    #print(table)

def query():
    result = Vizier.query_object("Betelgeuse", catalog=["V/137D/XHIP", "V/85A/catalog"])
    #result = Vizier.query_object("sirius", catalog="J/A+A/501/949/table")

    text_file = open("D:\\Programming\\Astronomy\\VizierTest.txt", "w")
    text_file.truncate()

    for table in result:
        text_file.write('\n')
        text_file.write('\n')
        text_file.write('(' + table.meta['name'] + ') ' + table.meta['description'] + '\n')
        text_file.write('\n')
        text_file.write('\n')
        for row in table:
            for col in table.colnames:
                text_file.write(col + '\t' + str(row[col]) + '\n')
                text_file.write('\n')
                #print row[col]

            #print row

    text_file.close()
    #text_file = open("D:\\Programming\\Astronomy\\VizierTest.txt", "w")
    #text_file.truncate()

    #table_xhip = result['V/137D/XHIP']
    #table_masses = result['V/85A/catalog']

    #for col in table_xhip.colnames:
    #    text_file.write(col + '\t' + table_xhip[col] + '\n')

    #text_file.write('\n')

    #for col in table_masses.colnames:
    #    text_file.write(col + '\t' + table_masses[col] + '\n')

    #text_file.close()

def query_catalogs():
    vizierSearch = VizierSearch()
    #result = vizierSearch.search_catalog('Hipparcos')
    result = vizierSearch.search_catalog('ALFAALFA')
    print result
    #result = vizierSearch.search_catalog('NOMAD')
    #catalogs = CatalogCollection(result)

    #print dumper(catalogs)
    #print result

def query_known_catalogs():
    vizierSearch = VizierSearch()
    result = vizierSearch.get_known_catalogs()

    print result

if __name__ == "__main__":
    #query()
    query_known_catalogs()

