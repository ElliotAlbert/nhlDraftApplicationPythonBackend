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
            query = ("INSERT INTO teams (id, franchise_id, leagueId, teamLogo, fullName, rawTricode, tricode) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            data = (team.id, team.franchise_id, team.leagueId, team.teamLogo, team.fullName, team.rawTricode, team.triCode)
            cursor.execute(query, data)
            connection.commit()

        print("Record inserted successfully into team table")
    except mysql.connector.Error as error:
        # TODO create redundancy for if the connection is lost
        print(f"Failed to insert record into team table {error}")


teams = api_convert.convert_to_team_object(get_logo=False)
cursor, connection = create_connection()
for team in teams:
    save_team_to_database(team, cursor, connection)

if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")