import requests
import time
import sys
import json



clientId = {'client_id':'68tskg1eib5q4n0kzsa2i3wl0egcow', 'query':'arma 3', 'limit':'100'}
r = requests.get('https://api.twitch.tv/kraken/search/channels',params=clientId)
print(r.json())

with open('file_tw.txt','w') as file:
    json.dump(r.json(), file)
