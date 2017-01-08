import requests
import time
import sys
import json

clientId = {'client_id': '68tskg1eib5q4n0kzsa2i3wl0egcow', 'limit': '100', 'game' : 'Arma 3'}
twitch_request = requests.get('https://api.twitch.tv/kraken/streams/', params=clientId).json()
print(twitch_request)

with open('file_streams.txt','w') as file:
    json.dump(twitch_request, file)
