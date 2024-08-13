import requests

# season YYYYYYYY format eg. 20232024, game_type = 2 - regular, 3 - playoffs
def get_player_stats_gamebook(player_id, season, game_type):
    url = f"https://api-web.nhle.com/v1/player/{player_id}/game-log/{season}/{game_type}"

    response = requests.get(url)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(response.status_code)
        return 404
    
print(get_player_stats(8478402, 20232024, 2))