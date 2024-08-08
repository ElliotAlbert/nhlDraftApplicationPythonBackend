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
# TODO implement something to check for the season ending
"""
All this would change is the season ID of the skater/keeper_stats database entries 
"""

running = True
update_queue = []


def update_cycle():
    while running:
        # Run whilest not set to terminate
        if update_queue.count != 0:
            """
            Check outstanding updates in the database and see if the update time has elapsed 
            This only needs to be done every 30 minutes or so, the api is updated frequently enough so that we will 
            know well ahead of time when the next set of games will be 
            """
            pass
        # Check for new games in the schedule
        new_games = convert_schedule()
        for game in new_games:
            update_queue.append(game)
