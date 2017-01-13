from hubs.vo.model.object_types import ObjectTypesLoader
from hubs.vo.model.maps import FieldMapLoader

def o_types():
    o_types = ObjectTypesLoader().load()
    print o_types.find('PulsV*delSct')

    map_collection = FieldMapLoader().load()
    print map_collection.get('simbad', 'common', 'OTYPE')

if __name__ == "__main__":
    o_types()