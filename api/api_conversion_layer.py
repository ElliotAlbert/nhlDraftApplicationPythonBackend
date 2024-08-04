import data_structures.data_structures as data_struct
import api.api_testing as api_test  # TODO change this to final api manager when it is finished
import json


def convert_to_team_object(get_logo):
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



