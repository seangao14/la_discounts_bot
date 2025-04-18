import datetime
import requests
import pandas as pd

def get_dodgers_discounts(game, home_away):
    """
    Check if Dodgers discounts are available.

    Args:
        game (dict): Game data.
        home_away (str): 'home' or 'away', whether Dodgers is the home team.

    Returns:
        list: List of tuples with discount information.
    """
    ret = []

    lad_win = game['teams'][home_away]['isWinner']
    game_pk = game['gamePk']

    game_data = requests.get(
        r'https://statsapi.mlb.com/api/v1/game/'
        rf'{game_pk}/boxscore'
    ).json()

    lad_runs = game_data['teams'][home_away]['teamStats']['batting']['runs']
    lad_sos = game_data['teams'][home_away]['teamStats']['pitching']['strikeOuts']
    lad_sbs = game_data['teams'][home_away]['teamStats']['batting']['stolenBases']

    if lad_win and home_away == 'home':
        ret.append(('Dodgers', 'Home win'))
    if lad_runs >= 6:
        ret.append(('Dodgers', 'Score 6+ runs'))
    if lad_sos >= 7:
        ret.append(('Dodgers', '7+ strikeouts'))
    if lad_sbs > 0 and home_away == 'home':
        ret.append(('Dodgers', 'Stolen base at home'))

    return ret


def get_angels_discounts(game, home_away):
    """
    Check if Angels discounts are available.
    
    Args:
        game (dict): Game data.
        home_away (str): 'home' or 'away', whether Angels is the home team.

    Returns:
        list: List of tuples with discount information.
    """
    ret = []

    laa_win = game['teams'][home_away]['isWinner']
    game_pk = game['gamePk']

    game_data = requests.get(
        r'https://statsapi.mlb.com/api/v1/game/'
        rf'{game_pk}/boxscore'
    ).json()

    laa_runs = game_data['teams'][home_away]['teamStats']['batting']['runs']
    laa_shutout = game_data['teams'][home_away]['teamStats']['pitching']['shutouts']
    laa_save = (
        sum([
            game_data['teams'][home_away]['players'][f'ID{pitcher_id}']['stats']['pitching']['saves']
            for pitcher_id in game_data['teams'][home_away]['pitchers']
        ])
    )

    if laa_win:
        ret.append(('Angels', 'Any win'))
    if laa_runs >= 7:
        ret.append(('Angels', 'Score 7+ runs'))
    if laa_shutout and home_away == 'home':
        ret.append(('Angels', 'Home shutout'))
    if laa_save and home_away == 'home':
        ret.append(('Angels', 'Home save'))

    return ret


def get_mlb_discounts(today):
    """
    Get MLB discounts for the previous day.

    Args:
        today (datetime.date): Today's date.

    Returns:
        list: List of tuples with discount information.
    """
    yday = today - datetime.timedelta(days=1)

    year = yday.year
    month = str(yday.month).zfill(2)
    day = str(yday.day).zfill(2)

    yday_str = f'{year}-{month}-{day}'

    data = requests.get(
        r'https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate='
        rf'{yday_str}&endDate={yday_str}'
        r'&gameType=R&'
        r'fields=dates,date,games,gamePk,status,abstractGameState,teams,away,home,team,id,name,gameDate,isWinner'
    )

    games_dicts = data.json()

    discounts = []

    for game in games_dicts['dates'][0]['games']:
        teams = {
            game['teams']['away']['team']['name']: 'away',
            game['teams']['home']['team']['name']: 'home',
        }

        if ('Los Angeles Dodgers' in teams.keys()):
            d = get_dodgers_discounts(game, teams['Los Angeles Dodgers'])
            discounts.extend(d)
        if ('Los Angeles Angels' in teams.keys()):
            d = get_angels_discounts(game, teams['Los Angeles Angels'])
            discounts.extend(d)

    return discounts
