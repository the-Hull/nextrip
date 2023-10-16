from genericpath import exists
import sys
# sys.path.insert(0,'..')
# sys.path.insert(1, './config/')
import config.VARS as VARS
# import VARS
import pandas as pd
import numpy as np
from time import sleep
import overpy
from functools import reduce
import operator as op

geopath = './00_data/city_geolocation.csv'

api = overpy.Overpass(retry_timeout=240)


if exists(geopath):

    geoloc = pd.read_csv(geopath)
    # print(geoloc)
    last_idx = geoloc.shape[0]
else:
    last_idx = 0





cities = list(VARS.CITY_REVIEWS.columns)
cities = cities[last_idx:]
print(f'city index is: {last_idx}, starting with {cities[0]}')





# city_string = list(map(lambda x: 'node["place"="city"][~"^name(:.*)?$"~"{}"];'.format(x), cities))
# all_cities = reduce(op.add, city_string)
# print(all_cities)


print(last_idx)


# r = api.query(f"""
# (
# {all_cities}
# );
# out center;
# """)


#  r = api.query(f"""
#     node[
#     "place"="city"]["name"="{ct}"];
#     out center;
#     """)
coords = []
try: 
        
    for idx, ct in enumerate(cities):

        print(f'current city is {ct}')

        r = api.query(f"""
        [timeout:240];
        node[
        place~"^(city|town|village)$"][~"^name(:.*)?$"~"{ct}"];
        out center;
        """)
        

        co = [(float(node.lon), float(node.lat)) 
                for node in r.nodes]
        
        
        # if len(co) < 1:
        #     co = [(float(way.center_lon), float(way.center_lat)) 
        #         for way in r.ways]
        # if len(co) < 1:
        #     co = [(float(rel.center_lon), float(rel.center_lat)) 
        #         for rel in r.relations]
        
        if len(co) < 1:
            co = [(np.nan, np.nan)]



        print(co)
        print('saving next')

        h = True if last_idx == 0 else False

        m = 'w' if last_idx == 0 else 'a'

        # print(h, m)
                


        pd.DataFrame(
            {
                'city' : [ct],
                'lon' :  [co[0][0]],
                'lat' : [co[0][1]]
                }
            ).to_csv(geopath, mode=m,header=h, index=False)

        last_idx += 1
        
        sleep(1)


except Exception as e: 
    print('failed with', e)
    sleep(30)
    print('restarting')
    try:
        exec(open('./01_etl/03_geolocation.py').read())
    except:
        print('cannott launch script')




