import requests
import time
import json

with open('data.json', 'r') as f:
    data = json.load(f)

RIOT_API_KEY = 'API_KEY'
Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
    "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": RIOT_API_KEY
}


# 리그 정보 가져오기
def getLeagueData(page):
    leagueURL = f'https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page={page}'
    response = requests.get(url=leagueURL, headers=Headers)
    return response.json()


# 소환사 puuid 가져오기
def getPuuid(summoner_id):
    summonerURL = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}'
    response = requests.get(url=summonerURL, headers=Headers)
    return response.json()


# 메칭 데이터 가져오기
def getMatches(puuid):
    matchURL = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count=100'
    response = requests.get(url=matchURL, headers=Headers)
    return response.json()


# 게임 정보 가져오기
def getGameData(matchid):
    gameURL = f'https://asia.api.riotgames.com/lol/match/v5/matches/{matchid}'
    response = requests.get(url=gameURL, headers=Headers)
    return response.json()


players = []
collectedGames = []


# 챌린저 목록 가져오기
def addPlayers(res):
    for n in range(len(res)):
        players.append({'name': res[n]['summonerName'], 'id': res[n]['summonerId']})


# dict 형식으로 정리하기
addPlayers(getLeagueData(1))
time.sleep(1.21)
addPlayers(getLeagueData(2))
time.sleep(1.21)

# 출력용
for i in range(len(players)):
    SummonerData = getPuuid(players[i]['id'])
    time.sleep(1.21)
    if not SummonerData.get('puuid'):
        continue
    SummonerPuuid = getPuuid(players[i]['id'])['puuid']
    if SummonerPuuid:
        matches = getMatches(SummonerPuuid)
        time.sleep(1.21)
        if matches:
            for j in range(len(matches)):
                gameData = getGameData(matches[j])
                if gameData.get('info'):
                    gameId = gameData['info']['gameId']
                    time.sleep(1.21)
                    if gameId in collectedGames:
                        print(f'중복된 게임(id: {gameId})')
                    else:
                        collectedGames.append(
                            {'gameID': gameData['info']['gameId'], 'players': gameData['info']['participants']})
                        for k in range(len(gameData['info']['participants'])):
                            champ = gameData['info']['participants'][k]
                            champName = champ['championName']
                            if champ['win']:
                                data[champ['championName']]['win'] += 1
                                print(f'{champName} win')
                            else:
                                data[champ['championName']]['lose'] += 1
                                print(f'{champName} lose')

with open("data.json", "w") as json_file:
    json.dump(data, json_file)
