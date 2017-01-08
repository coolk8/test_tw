import requests
import time
import sys
import json

clientId = {'client_id': '68tskg1eib5q4n0kzsa2i3wl0egcow', 'limit': '100', 'game' : 'Arma 3'}
twitch_request = requests.get('https://api.twitch.tv/kraken/streams/', params=clientId).json()
print(type(twitch_request["streams"]))
for channel in twitch_request["streams"]:
    #time.sleep(1)
    #stream_info = \
    #    requests.get("https://api.twitch.tv/kraken/streams/" + str(channel["name"]), params=clientId).json()
    #print channel
    try:
        print(channel["channel"]["name"] + " " + str(channel["viewers"]))
    except:
        print(channel["channel"]["name"] + " " + str(0))

# print(r.json())

# with open('file_tw.txt','w') as file:
#    json.dump(r, file)
