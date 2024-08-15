import mysql.connector
from mysql.connector import Error
import database_interface.database_connection_variables as db_vars
import api.api_conversion_layer as api_convert


def create_connection():
    connection = mysql.connector.connect(host=db_vars.host,
                                         database=db_vars.database1,
                                         user=db_vars.user,
                                         password=db_vars.password)
    cursor = connection.cursor()
    return cursor, connection


def save_team_to_database(team):
    cursor, connection = create_connection()
    try:
        check_exist_query = f"SELECT EXISTS (SELECT 1 FROM teams WHERE triCode = %s)"
        cursor.execute(check_exist_query, (team.triCode,))
        exists = cursor.fetchone()[0]

        if not exists:
            # Create new entry if team does not exist
            query = ("INSERT INTO teams (id, franchise_id, leagueId, teamLogo, fullName, rawTricode, triCode) "
                     "VALUES (%s, %s, %s, %s,%s, %s, %s)")
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
                    teamLogo = \"%s\",
                    fullName = \"%s\",
                    rawTricode = \"%s\",
                    triCode = \"%s\"
                WHERE triCode = \"%s\"
            """)
            data = (
                team.id, team.franchise_id, team.leagueId, team.teamLogo, team.fullName, team.rawTricode, team.triCode)
            cursor.execute(update_query, data)
            connection.commit()
    except mysql.connector.Error as error:
        print(f"Failed to insert record into team table {error}")
    close_connection(cursor, connection)


def save_players_to_database(player):
    cursor, connection = create_connection()
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
        close_connection(cursor, connection)

    except mysql.connector.Error as error:
        print(f"Failed to insert record into player table: {error}")


def get_team_id_by_tricode(team_tricode):
    cursor, connection = create_connection()
    query = "SELECT id FROM teams WHERE triCode = %s"
    cursor.execute(query, (team_tricode,))
    team_id = cursor.fetchone()[0]
    close_connection(cursor, connection)
    return team_id


def get_skater_id_by_team_id(team_id):
    cursor, connection = create_connection()
    query = f"SELECT playerId FROM skaters WHERE teamId = {team_id}"
    cursor.execute(query)
    player_ids = cursor.fetchall()
    close_connection(cursor, connection)
    # Convert the list of tuples into a list of integers (player IDs)
    player_ids = [item[0] for item in player_ids]
    return player_ids


def get_keeper_id_by_team_id(team_id):
    cursor, connection = create_connection()
    query = f"SELECT playerId FROM keepers WHERE teamId = {team_id}"
    cursor.execute(query)
    player_ids = cursor.fetchall()
    close_connection(cursor, connection)
    # Convert the list of tuples into a list of integers (player IDs)
    player_ids = [item[0] for item in player_ids]
    return player_ids


def close_connection(cursor, connection):
    if connection.is_connected():
        cursor.close()
        connection.close()


def delete_team(triCode):
    cursor, connection = create_connection()
    query = f"DELETE FROM teams WHERE triCode = %s"
    cursor.execute(query, (triCode,))
    connection.commit()
    close_connection(cursor, connection)
    return None


def save_keeper_stats_to_database(stats):
    cursor, connection = create_connection()
    try:
        check_exist_query = """
            SELECT EXISTS (
                SELECT 1 
                FROM keeperStats 
                WHERE playerId = %s AND season = %s AND playoffs = %s
            )
        """
        cursor.execute(check_exist_query, (stats.playerId, stats.season, stats.playoffs))
        exists = cursor.fetchone()[0]

        if exists:
            query = """
                UPDATE keeperStats
                SET gamesPlayed = %s,
                    gamesStarted = %s,
                    wins = %s,
                    losses = %s,
                    overtimeLosses = %s,
                    shotsAgainst = %s,
                    saves = %s,
                    goalsAgainst = %s,
                    savePercentage = %s,
                    goalsAgainstAverage = %s,
                    timeOnIce = %s,
                    shutOuts = %s,
                    goals = %s,
                    assists = %s,
                    points = %s,
                    penaltyMinutes = %s
                WHERE playerId = %s AND season = %s AND playoffs = %s            
            """
            data = (
                stats.gamesPlayed,
                stats.gamesStarted,
                stats.wins,
                stats.losses,
                stats.overtimeLosses,
                stats.shotsAgainst,
                stats.saves,
                stats.goalsAgainst,
                stats.savePercentage,
                stats.goalsAgainstAverage,
                stats.timeOnIce,
                stats.shutOuts,
                stats.goals,
                stats.assists,
                stats.points,
                stats.penaltyMinutes,
                stats.playerId,
                stats.season,
                stats.playoffs
            )
            cursor.execute(query, data)
            connection.commit()
        else:
            query = """
                INSERT INTO keeperStats (
                    playerId, season, gamesPlayed, gamesStarted, wins, losses, overtimeLosses, shotsAgainst, saves, goalsAgainst,
                    savePercentage, goalsAgainstAverage, timeOnIce, shutOuts, goals, assists, points, penaltyMinutes, playoffs
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                """
            data=(
                stats.playerId,
                stats.season,
                stats.gamesPlayed,
                stats.gamesStarted,
                stats.wins,
                stats.losses,
                stats.overtimeLosses,
                stats.shotsAgainst,
                stats.saves,
                stats.goalsAgainst,
                stats.savePercentage,
                stats.goalsAgainstAverage,
                stats.timeOnIce,
                stats.shutOuts,
                stats.goals,
                stats.assists,
                stats.points,
                stats.penaltyMinutes,
                stats.playoffs
            )
            cursor.execute(query, data)
            connection.commit()
    except Exception as e:
        print(f"Failed to insert/update record in keeperStats table \n{e}")
    finally:
        close_connection(cursor, connection)
    return None


def save_skater_stats_to_database(stats):
    cursor, connection = create_connection()
    try:
        check_exist_query = """
            SELECT EXISTS (
                SELECT 1 
                FROM skaterStats 
                WHERE playerId = %s AND season = %s AND playoffs = %s
            )
        """
        cursor.execute(check_exist_query, (stats.playerId, stats.season, stats.playoffs))
        exists = cursor.fetchone()[0]

        if exists:
            query = """
                UPDATE skaterStats
                SET playoffs = %s,
                    gamesPlayed = %s,
                    goals = %s,
                    assists = %s,
                    points = %s,
                    plusMinus = %s,
                    penaltyMinutes = %s,
                    pointsPerGame = %s,
                    evenStrengthGoals = %s,
                    evenStrengthPoints = %s,
                    powerPlayGoals = %s,
                    powerPlayPoints = %s,
                    shortHandedGoals = %s,
                    shortHandedPoints = %s,
                    overTimeGoals = %s,
                    gameWinningGoals = %s,
                    gameFirstGoals = %s,
                    hits = %s,
                    blockedShots = %s,
                    emptyNetGoals = %s,
                    FaceoffWinPercentage = %s
                WHERE playerId = %s AND season = %s AND playoffs = %s
            """
            data = (
                stats.playoffs,
                stats.gamesPlayed,
                stats.goals,
                stats.assists,
                stats.points,
                stats.plusMinus,
                stats.penaltyMinutes,
                stats.pointsPerGame,
                stats.evenStrengthGoals,
                stats.evenStrengthPoints,
                stats.powerPlayGoals,
                stats.powerPlayPoints,
                stats.shortHandedGoals,
                stats.shortHandedPoints,
                stats.overTimeGoals,
                stats.gameWinningGoals,
                stats.gameFirstGoals,
                stats.hits,
                stats.blockedShots,
                stats.emptyNetGoals,
                stats.FaceoffWinPercentage,
                stats.playerId,
                stats.season,
                stats.playoffs
            )
            cursor.execute(query, data)
            connection.commit()

        else:
            query = """
                INSERT INTO skaterStats (
                    playerId, season, playoffs, gamesPlayed, goals, assists, points, plusMinus,
                    penaltyMinutes, pointsPerGame, evenStrengthGoals, evenStrengthPoints, 
                    powerPlayGoals, powerPlayPoints, shortHandedGoals, shortHandedPoints, 
                    overTimeGoals, gameWinningGoals, gameFirstGoals, hits, blockedShots, 
                    emptyNetGoals, FaceoffWinPercentage
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                stats.playerId,
                stats.season,
                stats.playoffs,
                stats.gamesPlayed,
                stats.goals,
                stats.assists,
                stats.points,
                stats.plusMinus,
                stats.penaltyMinutes,
                stats.pointsPerGame,
                stats.evenStrengthGoals,
                stats.evenStrengthPoints,
                stats.powerPlayGoals,
                stats.powerPlayPoints,
                stats.shortHandedGoals,
                stats.shortHandedPoints,
                stats.overTimeGoals,
                stats.gameWinningGoals,
                stats.gameFirstGoals,
                stats.hits,
                stats.blockedShots,
                stats.emptyNetGoals,
                stats.FaceoffWinPercentage
            )
            print(query, data)
            cursor.execute(query, data)
            connection.commit()
            print(f"Record inserted successfully into skaterStats table {stats.playerId} {stats.season}")

    except Exception as e:
        print(f"Failed to insert/update record in skaterStats table: {e}")

    finally:
        close_connection(cursor, connection)
