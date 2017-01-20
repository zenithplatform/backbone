__author__ = 'civa'

from distributed.hubs.vo.providers.params import BaseVOParams

def main():
    base = BaseVOParams()

    base_json = '{ "vo_params": { "preamble":"83fac637bc8a6306ce4df3847af87b68de27733f", "term": "Betelgeuse", "target": "Object"}}'
    obj_json = '{ "vo_params": { "preamble":"83fac637bc8a6306ce4df3847af87b68de27733f", "term": "Betelgeuse", "exact": false, "cone": true, "target": "Object", "region":"m81", "radius":"0d6m0s", "coordinates":"05h35m17.3s -05h23m28s", "epoch":"B1950", "equinox":1950 }}'
    catalogs_json = '{ "vo_params": { "preamble":"83fac637bc8a6306ce4df3847af87b68de27733f", "term": "HIP 223", "target": "Catalog", "obsolete_catalogs": false }}'

    base = BaseVOParams()
    object_instance = base.unpack(obj_json)
    base = BaseVOParams()
    catalog_instance = base.unpack(catalogs_json)

    print(object_instance)
    print(catalog_instance)

    print('end')

if __name__ == "__main__":
    main()
