import json
import data_structures.data_structures as data_struct
from api import api_testing


# season as int eg. 20232024
def convert_player_stats_to_skater_stats_object(player_id, season):
    response_main = api_testing.get_player_stats_seasonal(player_id)
    response_hits = api_testing.get_player_stats_seasonal_hits(player_id)

    if response_main == 404:
        return 404
    elif response_hits == 404:
        return 404

    skater_stats = data_struct.skater_stats(
        id=id,
        playerId=player_id,
        season=season,
        playoffs=0,
        gamesPlayed=0,
        goals=0,
        assists=0,
        points=0,
        plusMinus=0,
        pointsPerGame=0,
        evenStrengthGoals=0,
        evenStrengthPoints=0,
        powerPlayGoals=0,
        powerPlayPoints=0,
        shortHandedGoals=0,
        shortHandedPoints=0,
        overTimeGoals=0,
        gameWinningGoals=0,
        FaceoffWinPercentage=0,
        blockedShots=0,
        emptyNetGoals=0,
        gameFirstGoals=0,
        hits=0
    )

    skater_stats.playerId = player_id
    skater_stats.season = season
    skater_stats.playoffs = 0

    for season_in in response_main["data"]:
        if season_in.get("seasonId") == season:
            skater_stats.gamesPlayed = season_in.get("gamesPlayed")
            skater_stats.goals = season_in.get("goals")
            skater_stats.assists = season_in.get("assists")
            skater_stats.points = season_in.get("points")
            skater_stats.plusMinus = season_in.get("plusMinus")
            skater_stats.pointsPerGame = season_in.get("pointsPerGame")
            skater_stats.evenStrengthGoals = season_in.get("evGoals")
            skater_stats.evenStrengthPoints = season_in.get("evPoints")
            skater_stats.powerPlayGoals = season_in.get("ppGoals")
            skater_stats.powerPlayPoints = season_in.get("ppPoints")
            skater_stats.shortHandedGoals = season_in.get("shGoals")
            skater_stats.shortHandedPoints = season_in.get("shPoints")
            skater_stats.overTimeGoals = season_in.get("otGoals")
            skater_stats.gameWinningGoals = season_in.get("gameWinningGoals")
            skater_stats.FaceoffWinPercentage = season_in.get("faceoffWinPct")

    for season_in in response_hits["data"]:
        if season_in.get("seasonId") == season:
            skater_stats.blockedShots = season_in["blockedShots"]
            skater_stats.emptyNetGoals = season_in["emptyNetGoals"]
            skater_stats.gameFirstGoals = season_in["firstGoals"]
            skater_stats.hits = season_in["hits"]

    return skater_stats
