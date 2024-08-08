import data_structures.data_structures as data_struct
import api.api_testing as api_test  # TODO change this to final api manager when it is finished
import json
import datetime



def convert_to_team_object(get_logo):
    # TODO implement get_logo logic
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


def convert_roster_to_player_objects(triCode):
    roster = []
    response = api_test.get_team_roster(triCode)
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
    hold_game = data_struct.scheduled_game(0, 0, "date", "update_time", 0, 0, 'aaa', 'aaa')
    hold_game.game_Id = game['id']
    hold_game.season = game['season']
    hold_game.date = datetime.datetime.strptime(game['startTimeUTC'], '%Y-%m-%dT%H:%M:%SZ')
    hold_game.update_time = hold_game.date + datetime.timedelta(hours=4)
    hold_game.away_team_triCode = game['awayTeam']['abbrev']
    hold_game.home_team_triCode = game['homeTeam']['abbrev']
    # TODO implement team id outside of this function
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



