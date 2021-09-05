import json
import requests

req = requests.get('http://ddragon.leagueoflegends.com/cdn/11.15.1/data/en_US/champion.json').json()
champData = {}
champions = req['data']

for champName in champions:
    champData[champName] = {"win": 0, "lose": 0}

with open("data.json", "w") as json_file:
    json.dump(champData, json_file)
