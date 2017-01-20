__author__ = 'civa'
from suds.client import Client
from bs4 import BeautifulSoup, Tag, NavigableString
from distributed.hubs.vo.model.catalog import *
import unicodedata, re
import sys
import string

all_chars = (unichr(i) for i in xrange(sys.maxunicode))
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
# or equivalently and much more efficiently
control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))
control_char_re = re.compile('[%s]' % re.escape(control_chars))

def get_vizier():
    url = 'http://cdsws.u-strasbg.fr/axis/services/VizieR?wsdl'
    client = Client(url)

    available = client.service.getAvailability()

    if available:
        allCatalogues = client.service.metaAll()

    print allCatalogues

def get_ucd():
    url = 'http://cdsws.u-strasbg.fr/axis/services/UCD?wsdl'
    client = Client(url)

    #print client
    available = client.service.getAvailability()

    if available:
        allCatalogues = client.service.UCDList()

    print allCatalogues

if __name__ == "__main__":
    #get_vizier()
    get_ucd()
