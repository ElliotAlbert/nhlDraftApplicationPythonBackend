"""
1. Check for outstanding updates in the database
2. Run any necessary updates
(i.e. updating the player stats with the most recent data and checking for new players on rosters)
3. Removed the finished update from the queue
4. Once no updates are found, check for new games in the schedule and set a date and time for their update cycles
Place the update time for 4 hours after the game is scheduled to start
"""
import data_structures.data_structures as data_struct
from api.api_conversion_layer import convert_schedule
from database_interface import sql_interface
import time
import datetime
# TODO implement something to check for the season ending
# TODO implement a way of checking for changes of times in the schedule and updating the update time accordingly
# TODO implement function locks when implementing the web socket to prevent multiple threads from accessing the same
# data
"""
All this would change is the season ID of the skater/keeper_stats database entries 
"""
running = True
update_queue = []
update_increment = 3  # minutes


def update_team_stats(triCode):
    """
    1. Update the team roster to look for new players
    2. Get the player ids for the team
    3. Update the player stats for each player
    :param triCode: The teams tricode
    :return: Nothing
    """
    return None


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
                    print(f"New update found {update.home_team_triCode} vs {update.away_team_triCode}")
                    update_team_stats(update.home_team_triCode)
                    update_team_stats(update.away_team_triCode)
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
                print(f"{game.home_team_triCode} vs {game.away_team_triCode} added to update queue | {game.date} | To be updated at {game.update_time}")
        else:
            print("No new games found")
        print("Entering rest period")


        time.sleep(update_increment)  # Sleep process for 30 minutes


update_cycle()