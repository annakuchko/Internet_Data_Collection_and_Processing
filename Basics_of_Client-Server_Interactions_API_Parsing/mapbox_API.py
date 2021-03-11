# https://docs.mapbox.com/api/
import requests
import datetime
from pprint import pprint as pp
import random

# generate random coordinates nearby
latitude = 19.99
longitude = 73.78
random.seed(123)

def generate_random_data(lat, lon, num_rows):
    s = ''
    for _ in range(num_rows):
        #hex1 = '%012x' % random.randrange(16**10) # 12 char random string
        #flt = float(random.randint(0,100))
        dec_lat = random.random()
        dec_lon = random.random()
        s+=f'{lat+dec_lat},{lon+dec_lon};'
    return s

# define api params
api_type = 'directions-matrix'
move_type = 'walking'

long_lat = generate_random_data(latitude, longitude, 10)[:-1]

access_token = 'pk.eyJ1IjoiYW5uYWt1Y2hrbyIsImEiOiJja2x0eDBraWgwb2dtMnZueGVrZGI4aHV6In0.t7DYd924TYKu__5oJJEt0g'
concrete_params = {
    'sources': 1,
    'access_token': access_token
    }

# api base path
base_url = f'https://api.mapbox.com/{api_type}/v1/mapbox/{move_type}/{long_lat}'

# retrieve data
try:    
    r = requests.get(base_url, concrete_params)
    
    # print requested json data
    pp(r.json())
    
    # save json data to file
    if r.ok:
        import json
        path = "walking_data.json"
        with open(path, "w") as f:
            json.dump(r.json(), f, indent=4)
    else:
        raise Exception(f'Status code: {r.status_code}')
except:
    raise Exception(f'Status code: {r.status_code}')
            
            
            
            