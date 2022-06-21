import json
import os
import pickle
import random
import requests

from constant import TENOR_KEY, ckey

file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data.bin")

def get_random_gif(search_term, lmt):
    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, TENOR_KEY, ckey,  lmt))

    if r.status_code == 200:
        results = json.loads(r.content)["results"]
        return results[random.randint(0, len(results) - 1)]["media_formats"]["gif"]["url"]
    else:
        return ""
        
def save_data(servers):
    with open(file, "wb") as handle:
        pickle.dump(servers, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def load_data():
    if os.path.isfile(file):
        with open(file, "rb") as handle:
            return pickle.load(handle)
    else:
        return {}