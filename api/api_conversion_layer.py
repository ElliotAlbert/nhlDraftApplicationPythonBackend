import json
import api.api_testing
import data_structures.data_structures as data_struct


def convert_player_stats_to_skater_stats_object(player_id, season, game_type):
    response = api.api_testing.get_player_stats(player_id, season, game_type)
    if response is 404:
        return None
    parsed = json.loads(response)
    if game_type == 3:
        skater_stats = data_struct.skaterStats(playerId=player_id, season=season, playoffs=1, gamesPlayed=0, goals=0,
                                               assists=0, points=0, plusMinus=0, pointsPerGame=0, powerPlayGoals=0,
                                               powerPlayPoints=0, shortHandedGoals=0, shortHandedPoints=0,
                                               overTimeGoals=0, gameWinningGoals=0)
    else:
        skater_stats = data_struct.skaterStats(playerId=player_id, season=season, playoffs=0, gamesPlayed=0, goals=0,
                                               assists=0, points=0, plusMinus=0, pointsPerGame=0, powerPlayGoals=0,
                                               powerPlayPoints=0, shortHandedGoals=0, shortHandedPoints=0,
                                               overTimeGoals=0, gameWinningGoals=0)
    assists, goals, points, powerPlayGoals, powerPlayPoints, overTimeGoals, gameWinningGoals = 0

    for game in parsed['gameLog']:
        assists += game['assists']
        goals += game['goals']
        points += game['points']
        powerPlayGoals += game['powerPlayGoals']
        powerPlayPoints += game['PowerPlayPoints']
        overTimeGoals += game['otGoals']
        gameWinningGoals += game['gameWinningGoals']
