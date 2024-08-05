import mysql.connector
from mysql.connector import Error
import database_connection_variables as db_vars
import api.api_conversion_layer as api_convert


def create_connection():
    connection = mysql.connector.connect(host=db_vars.host,
                                         database=db_vars.database1,
                                         user=db_vars.user,
                                         password=db_vars.password)
    cursor = connection.cursor()
    return cursor, connection


def save_team_to_database(team, cursor, connection):
    try:
        # Check if the team exists in the database TODO place this in a function to be reused
        check_exist_query = f"SELECT EXISTS (SELECT 1 FROM teams WHERE triCode = %s)"
        cursor.execute(check_exist_query, (team.triCode,))
        exists = cursor.fetchone()[0]

        if not exists:
            # Create new entry if team does not exist
            query = ("INSERT INTO teams (id, franchise_id, leagueId, teamLogo, fullName, rawTricode, triCode) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            data = (
                team.id, team.franchise_id, team.leagueId, team.teamLogo, team.fullName, team.rawTricode, team.triCode)
            cursor.execute(query, data)
            connection.commit()
        else:
            # Update the entry if the team already exists
            update_query = ("""
                UPDATE teams
                SET franchise_id = %s,
                    leagueId = %s,
                    teamLogo = %s,
                    fullName = %s,
                    rawTricode = %s,
                    triCode = %s
                WHERE triCode = %s
            """)
            data = (
                team.id, team.franchise_id, team.leagueId, team.teamLogo, team.fullName, team.rawTricode, team.triCode)
            cursor.execute(update_query, data)
            connection.commit()
    except mysql.connector.Error as error:
        # TODO create redundancy for if the connection is lost
        print(f"Failed to insert record into team table {error}")


def save_players_to_database(cursor, connection, player):
    try:
        # Determine the correct table
        table = 'skaters' if player.position != "G" else 'keepers'

        # Check if the player already exists in the database
        check_exist_query = f"SELECT EXISTS (SELECT 1 FROM {table} WHERE playerId = %s)"
        cursor.execute(check_exist_query, (player.playerId,))  # Pass as a tuple
        exists = cursor.fetchone()[0]

        # Default query is INSERT
        query = (f"""
            INSERT INTO {table} (teamID, headshot, number, firstName, lastName, position, 
            shootsCatches, heightCM, weightKilograms, playerId)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)

        # If the player exists, prepare an UPDATE query
        if exists:
            query = (f"""
                UPDATE {table}
                SET teamID = %s,
                    headshot = %s,
                    number = %s,
                    firstName = %s,
                    lastName = %s,
                    position = %s,
                    shootsCatches = %s,
                    heightCM = %s,
                    weightKilograms = %s
                WHERE playerId = %s
            """)

        # Data tuple for either query
        data = (
            player.teamID, player.headshot, player.number, player.firstName, player.lastName,
            player.position, player.shootsCatches, player.heightCm, player.weightKg, player.playerId
        )

        # Execute the query
        cursor.execute(query, data)
        connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to insert record into player table: {error}")


def get_team_id_by_tricode(team_tricode, cursor):
    query = "SELECT id FROM teams WHERE triCode = %s"
    cursor.execute(query, (team_tricode,))
    team_id = cursor.fetchone()[0]
    return team_id


def close_connection(cursor, connection):
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


teams = api_convert.convert_to_team_object(get_logo=False)
for team in teams:
    roster = api_convert.convert_roster_to_player_objects(team.triCode)
    if roster == 404:
        print(f"Failed to get roster for {team.triCode}")
    else:
        cursor, connection = create_connection()
        teamId = get_team_id_by_tricode(team.triCode, cursor)
        for player in roster:
            player.teamID = teamId
            save_players_to_database(cursor, connection, player)
        close_connection(cursor, connection)
