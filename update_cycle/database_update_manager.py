"""
1. Check for outstanding updates in the database
2. Run any necessary updates
(i.e. updating the player stats with the most recent data and checking for new players on rosters)
3. Removed the finished update from the queue
4. Once no updates are found, check for new games in the schedule and set a date and time for their update cycles
Place the update time for 4 hours after the game is scheduled to start
"""
import api.api_testing
import data_structures.data_structures as data_struct
from api.api_conversion_layer import convert_schedule
from database_interface import sql_interface
import time
import datetime
import api.api_conversion_layer as api_convert
import mysql.connector



# data
"""
All this would change is the season ID of the skater/keeper_stats database entries 
"""
running = True
update_queue = []
update_increment = 30  # minutes
current_season = '20232024'
is_playoffs = 0


def update_team_stats(triCode, season, playoffs):
    """
    !!DO NOT CALL THIS FUNCTION BEFORE THE CREATION OF TEAM OBJECTS IN THE DATABASE!!
    1. Update the team roster to look for new players
    2. Get the player ids for the team
    3. Update the player stats for each player
    :param playoffs: Bool to determine if the stats are for the playoffs
    :param season: The season for which you want to update the player stats
    :param triCode: The teams tricode
    :return: Nothing
    """
    # Get current team roster
    print(f"Getting roster for {triCode}")
    roster = api_convert.convert_roster_to_player_objects(triCode, season)
    if roster == 404:
        print(f"No current roster found {triCode}")
        return 404
    print("Fetching team id")
    team_id = sql_interface.get_team_id_by_tricode(triCode)
    print(f"Team id {team_id}")
    # TODO add set team_logo
    for player in roster:
        player.teamID = team_id
        print(f"saving {player.firstName} {player.lastName} to database")
        sql_interface.save_players_to_database(player)
    # Reload roster with all players in the database
    print(f"Reloading roster for {triCode}")
    skaters = sql_interface.get_skater_id_by_team_id(team_id)
    keepers = sql_interface.get_keeper_id_by_team_id(team_id)
    for player in skaters:
        print(f"getting stats for {player}")
        stats = api_convert.convert_player_stats_to_skater_stats_object(player, season, playoffs)
        if stats == 404:
            print(f"No player stats found for {player} {season} {playoffs}")
            continue
        else:
            print(f"saving stats for {player}")
            sql_interface.save_skater_stats_to_database(stats)
    for player in keepers:
        print(f"getting stats for {player}")
        stats = api_convert.convert_keepers_stats_to_keeper_stats_object(player, season, playoffs)
        if stats == 404:
            print(f"No player stats found for {player} {season} {playoffs}")
            continue
        else:
            print(f"saving stats for {player}")
            sql_interface.save_keeper_stats_to_database(stats)



def update_cycle():
    while running:
        # Run whilest not set to terminate
        if len(update_queue) != 0:
            """
            Check outstanding updates in the database and see if the update time has elapsed 
            This only needs to be done every 30 minutes or so, the api is updated frequently enough so that we will 
            know well ahead of time when the next set of games will be 
            """
            print("Entering update queue")
            for update in update_queue:
                if update.update_time < datetime.datetime.now():
                    print("Updating season")
                    current_season = update.season
                    print(f"Game played getting stats: {update.home_team_triCode} vs {update.away_team_triCode}")
                    if (update.playoffs == 1):
                        is_playoffs = 1
                    else:
                        is_playoffs = 0
                    update_team_stats(update.home_team_triCode, current_season, is_playoffs)
                    update_team_stats(update.away_team_triCode, current_season, is_playoffs)
                    print("Player stats updated")
                    update_queue.remove(update)
        # Check for new games in the schedule
        else:
            print("Update Queue is empty")
            print("Checking for new games")
            new_games = convert_schedule(update_queue)
            if len(new_games) > 0:
                print("Name Games found")
                for game in new_games:
                    update_queue.append(game)
                    print(
                        f"{game.home_team_triCode} vs {game.away_team_triCode} added to update queue | {game.date} | "
                        f"To be updated at {game.update_time}")
            else:
                print("No new games found")
            print("Entering rest period")
        time.sleep(update_increment)  # Sleep process for 30 minutes


def init():
    # First startup function
    teams = api_convert.convert_to_team_object(False)
    # Load the current schedule to get the current season
    schedule = convert_schedule(update_queue)
    print("Schedule loaded")
    current_season = schedule[0].season
    previous_season = int(current_season) - 10001
    print(f"Current season is {current_season} Previous season is {previous_season}")
    for team in teams:
        sql_interface.save_team_to_database(team)
        print(f"Team {team.triCode} saved to database")
    for team in teams:
        print(f"Updating roster for {team.triCode}")
        roster = api_convert.convert_roster_to_player_objects(team.triCode, current_season)
        if roster == 404:
            print(f"No current roster found {team.triCode} for season {current_season}")
        else:
            # Add each teams roster to the database of players
            print(f"Getting team id for {team.triCode}")
            team_id = sql_interface.get_team_id_by_tricode(team.triCode)
            print(f"Team id {team_id}")
            for player in roster:
                player.teamID = team_id
                print(f"saving {player.firstName} {player.lastName} to database")
                sql_interface.save_players_to_database(player)
    # load current and previous season player stats to the database
    for team in teams:
        print(f"Updating team stats for {team.triCode} for season {previous_season} non playoff data")
        ret = update_team_stats(team.triCode, previous_season, 0)
        if ret == 404:
            print(f"No current roster found {team.triCode} {previous_season} non playoff data")
            continue
        print(f"Updating team stats for {team.triCode} for season {previous_season} playoff data")
        ret = update_team_stats(team.triCode, previous_season, 1)
        if ret == 404:
            print(f"No current roster found {team.triCode} {previous_season} playoff data")
            continue
        print(f"Updating team stats for {team.triCode} for season {current_season} non playoff data")
        ret = update_team_stats(team.triCode, current_season, 0)
        if ret == 404:
            print(f"No current roster found {team.triCode} {current_season} non playoff data")
            continue
        if is_playoffs:
            print(f"Updating team stats for {team.triCode} for season {current_season} playoff data")
            update_team_stats(team.triCode, current_season, 1)
    print("Player stats updated for all teams, entering update cycle")
    update_cycle()


init()