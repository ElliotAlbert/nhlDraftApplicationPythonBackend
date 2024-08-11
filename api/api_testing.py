import requests


def get_player_stats_seasonal(player_id):
    url_player_stats = f"https://api.nhle.com/stats/rest/en/skater/summary?cayenneExp=playerId={player_id}"
    response = requests.get(url_player_stats)

    if response.status_code == 200:
        return response.json()
    else:
        return 404


def get_player_stats_seasonal_hits(player_id):
    url_player_stats_hits = f"https://api.nhle.com/stats/rest/en/skater/realtime?cayenneExp=playerId={player_id}"
    response = requests.get(url_player_stats_hits)

    if response.status_code == 200:
        return response.json()
    else:
        return 404


def get_player_stats_gamebook(player_id, season, game_type):
    url = f"https://api-web.nhle.com/v1/player/{player_id}/game-log/{season}/{game_type}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return 404
