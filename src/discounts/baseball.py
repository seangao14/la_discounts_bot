import datetime
import requests
import pandas as pd

today = datetime.date.today()
yday = today - datetime.timedelta(days=1)

year = yday.year
month = str(yday.month).zfill(2)
day = str(yday.day).zfill(2)

yday_str = f'{year}-{month}-{day}'

discounts = []

# baseball
data = requests.get(
    r'https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate='
    rf'{yday_str}&endDate={yday_str}'
    r'&gameType=R&'
    r'fields=dates,date,games,gamePk,status,abstractGameState,teams,away,home,team,id,name,gameDate,isWinner'
)

games_dicts = data.json()

for game in games_dicts['dates'][0]['games']:
    teams = {
        game['teams']['away']['team']['name']: 'away',
        game['teams']['home']['team']['name']: 'home',
    }
    if ('Los Angeles Dodgers' in teams.keys()) or ('Los Angeles Angels' in teams.keys()):
        break
    
    lad_away_home = teams['Los Angeles Dodgers']
    a_away_home = teams['Los Angeles Angels']

    lad_win = game['teams'][lad_away_home]['isWinner']

    game_pk = game['gamePk']
    game_data = requests.get(
        r'https://statsapi.mlb.com/api/v1/game/'
        rf'{game_pk}/boxscore&fields='
    ).json()

    lad_runs = game_data['teams'][lad_away_home]['teamStats']['batting']['runs']
    lad_sos = game_data['teams'][lad_away_home]['teamStats']['pitching']['strikeOuts']
    lad_sbs = game_data['teams'][lad_away_home]['teamStats']['batting']['stolenBases']



