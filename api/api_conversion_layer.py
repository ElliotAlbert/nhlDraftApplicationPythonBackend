import data_structures.data_structures as data_struct
import api.api_testing as api_test
import json
import datetime



def convert_to_team_object(get_logo):
    # TODO implement get_logo logic
    """
    :param get_logo: This can be set to false always as there is currently no application for this
    :return: A list of team objects converted from the api layer
    """
    teams = []
    response = api_test.get_all_teams()
    if response.status_code != 200:
        return response.status_code
    parsed = json.loads(response.text)
    for team in parsed['data']:
        hold_team = data_struct.team(0, 0, 0, "blank", "fullName", 'aaa', 'aaa')
        hold_team.franchise_id = team['franchiseId']
        hold_team.leagueId = team['leagueId']
        hold_team.fullName = team['fullName']
        hold_team.rawTricode = team['rawTricode']
        hold_team.triCode = team['triCode']
        teams.append(hold_team)
        ''' 
        After data is loaded there is one missing value which is the team logo this can only be gathered from player 
        data so we will need to make a second call to get this data
        '''
    return teams


def create_new_player_object(player):
    hold_player = data_struct.player(0, 0, "blank", 0, "firstName", "lastName", "position", "shootsCatches", 0, 0, 0)
    hold_player.headshot = player['headshot']
    try:
        hold_player.number = player['sweaterNumber']
    except:
        hold_player.number = 0
    hold_player.firstName = player['firstName']['default']
    hold_player.lastName = player['lastName']['default']
    hold_player.position = player['positionCode']
    hold_player.shootsCatches = player['shootsCatches']
    hold_player.heightCm = player['heightInCentimeters']
    hold_player.weightKg = player['weightInKilograms']
    hold_player.playerId = player['id']
    return hold_player


def convert_roster_to_player_objects(triCode, season):
    roster = []
    response = api_test.get_team_roster(triCode, season)
    if response.status_code != 200:
        return response.status_code
    parsed = json.loads(response.text)
    for player in parsed['forwards']:
        hold_player = create_new_player_object(player)
        roster.append(hold_player)
    for player in parsed['defensemen']:
        hold_player = create_new_player_object(player)
        roster.append(hold_player)
    for player in parsed['goalies']:
        hold_player = create_new_player_object(player)
        roster.append(hold_player)
    return roster


def create_new_schedule_object(game):
    hold_game = data_struct.scheduled_game(0, 0, "date", "update_time", 0, 0, 'aaa', 'aaa',0)
    hold_game.game_Id = game['id']
    hold_game.season = game['season']
    hold_game.date = datetime.datetime.strptime(game['startTimeUTC'], '%Y-%m-%dT%H:%M:%SZ')
    hold_game.update_time = hold_game.date + datetime.timedelta(hours=4)
    hold_game.away_team_triCode = game['awayTeam']['abbrev']
    hold_game.home_team_triCode = game['homeTeam']['abbrev']
    hold_game.playoffs = 0
    if game['gameType'] == 3:
        hold_game.playoffs = 1
    return hold_game


# This function is just to prevent circular imports
def check_against_logged(id, logged_games):
    for game in logged_games:
        if id == game.game_Id:
            return True


def convert_schedule(logged_games):
    games = []
    response = api_test.get_schedule()
    if response.status_code != 200:
        return response.status_code
    parsed = json.loads(response.text)
    for day in parsed['gameWeek']:
        # We wanna check if the games are already logged
        for game in day['games']:
            if not check_against_logged(game['id'], logged_games):
                hold_game = create_new_schedule_object(game)
                games.append(hold_game)
    return games


# season as int eg. 20232024
def convert_player_stats_to_skater_stats_object(player_id, season, playoffs):
    response_main = api_test.get_player_stats_seasonal(player_id, season, season, playoffs)
    response_hits = api_test.get_player_stats_seasonal_hits(player_id, season, season, playoffs)
    if response_main == 404:
        return 404
    elif response_hits == 404:
        return 404
    skater_stats = data_struct.skater_stats(
    0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,
    0,0,0,0,0,0
    )

    if len(response_main["data"]) == 0:
        return 404
    skater_stats.playerId = player_id
    skater_stats.season = season
    skater_stats.playoffs = playoffs
    skater_stats.gamesPlayed = response_main['data'][0].get("gamesPlayed")
    skater_stats.goals = response_main['data'][0].get("goals")
    skater_stats.assists = response_main['data'][0].get("assists")
    skater_stats.points = response_main['data'][0].get("points")
    skater_stats.plusMinus = response_main['data'][0].get("plusMinus")
    skater_stats.pointsPerGame = response_main['data'][0].get("pointsPerGame")
    skater_stats.evenStrengthGoals = response_main['data'][0].get("evGoals")
    skater_stats.evenStrengthPoints = response_main['data'][0].get("evPoints")
    skater_stats.powerPlayGoals = response_main['data'][0].get("ppGoals")
    skater_stats.powerPlayPoints = response_main['data'][0].get("ppPoints")
    skater_stats.shortHandedGoals = response_main['data'][0].get("shGoals")
    skater_stats.shortHandedPoints = response_main['data'][0].get("shPoints")
    skater_stats.overTimeGoals = response_main['data'][0].get("otGoals")
    skater_stats.gameWinningGoals = response_main['data'][0].get("gameWinningGoals")
    skater_stats.FaceoffWinPercentage = response_main['data'][0].get("faceoffWinPct")
    skater_stats.blockedShots = response_hits['data'][0]["blockedShots"]
    skater_stats.emptyNetGoals = response_hits['data'][0]["emptyNetGoals"]
    skater_stats.gameFirstGoals = response_hits['data'][0]["firstGoals"]
    skater_stats.hits = response_hits['data'][0]["hits"]
    skater_stats.penaltyMinutes = response_main['data'][0]["penaltyMinutes"]

    return skater_stats


def convert_keepers_stats_to_keeper_stats_object(player_id, season, playoffs):
    response = api_test.get_keeper_stats_seasonal(player_id, season, season, playoffs)
    if len(response['data']) == 0:
        return 404
    keeper_stats = data_struct.keeper_stats(
    0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0)
    keeper_stats.playerId = player_id
    keeper_stats.season = season
    keeper_stats.gamesPlayed = response['data'][0].get("gamesPlayed")
    keeper_stats.gamesStarted = response['data'][0].get("gamesStarted")
    keeper_stats.wins = response['data'][0].get("wins")
    keeper_stats.losses = response['data'][0].get("losses")
    keeper_stats.overtimeLosses = response['data'][0].get("otLosses")
    keeper_stats.shotsAgainst = response['data'][0].get("shotsAgainst")
    keeper_stats.saves = response['data'][0].get("saves")
    keeper_stats.goalsAgainst = response['data'][0].get("goalsAgainst")
    keeper_stats.savePercentage = response['data'][0].get("savePct")
    keeper_stats.goalsAgainstAverage = response['data'][0].get("goalsAgainstAverage")
    keeper_stats.timeOnIce = response['data'][0].get("timeOnIce")
    keeper_stats.shutOuts = response['data'][0].get("shutouts")
    keeper_stats.goals = response['data'][0].get("goals")
    keeper_stats.assists = response['data'][0].get("assists")
    keeper_stats.points = response['data'][0].get("points")
    keeper_stats.penaltyMinutes = response['data'][0].get("penaltyMinutes")
    keeper_stats.playoffs = playoffs
    return keeper_stats


convert_player_stats_to_skater_stats_object(8478402, 20242025, 1)

