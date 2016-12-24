import requests
import time
import sys

clientId = {'client_id':'68tskg1eib5q4n0kzsa2i3wl0egcow'}
r = requests.get('https://api.twitch.tv/kraken/channels/david_toroczkai/follows',params=clientId)
print(r.json()['_total'])
