__author__ = 'civa'

from hubs.vo.concurrency.threadpool import ThreadPool
from ..providers import ned, simbad, vizier

class Search():

    pool = ThreadPool(3)

    ned_search = ned.NedSearch()
    simbad_search = simbad.SimbadSearch()
    vizier_search = vizier.VizierSearch()

    def __init__(self):
        self.ned_search.init_search()
        self.simbad_search.init_search()
        self.vizier_search.init_search()

    def start(self):
        self.pool.add_task(self.ned_search.search_object('test'))
        self.pool.add_task(self.simbad_search.search_object('test'))
        self.pool.add_task(self.vizier_search.search_object('test'))

        self.pool.wait_completion()