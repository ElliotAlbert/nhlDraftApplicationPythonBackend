'''
-All Teams in database
https://api.nhle.com/stats/rest/en/team
Returns all the teams that exist

-Current Roster For Given Team
https://api-web.nhle.com/v1/roster/LAK/current

Use 3 Letter Team Acronym "TriCode" as it is stated in team gather information

-Player Stats
This is some python to get misc player data
https://api-web.nhle.com/v1/player/{PlayerID}/landing

This is the python for finding the "misc" data about a player using the season you wish to search and the player id
This is how we get stats like hits and penalty stats
Define the URL
url = "https://api.nhle.com/stats/rest/en/skater/realtime"

Define the query parameters
params = {
    "limit": 50,
    "cayenneExp": "gameTypeId=2 and seasonId<=20232024 and seasonId>=20232024 and playerId=8477903"
} This is all the api endpoints we should need for implementing the whole application

'''
import requests
def sample_api_request():
    season_lower = "20232024"
    season_upper = "20232024"
    player_id = 8477903
    # Place end point we need to reach here
    url = "https://api.nhle.com/stats/rest/en/skater/realtime"
    params = {
        "limit":1,
        # This might not always be required but if post parameters are needed they can go here
        "cayenneExp": f"gameTypeId=2 and seasonId<={season_lower} and seasonId>={season_upper} and playerId={player_id}"
    }
    # Send the http request and capture the response within a variable
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # Do something with response
        print(response.json)
    else:
        print(f"Request failed with status code {response.status_code}")

def get_all_teams():
    url = "https://api.nhle.com/stats/rest/en/team"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return response
    else:
        return response


get_all_teams()