import datetime
import requests

# api: https://gitlab.com/dword4/nhlapi/-/blob/master/new-api.md
data = requests.get('https://api-web.nhle.com/v1/score/now').json()


data['games'][0]['homeTeam']
data['games'][0]['awayTeam']

for game in data['games']:
    teams = [
        game['homeTeam']['name']['default'],
        game['awayTeam']['name']['default'],
    ]
    if "Ducks" in teams:
        print("Ducks")
        break

