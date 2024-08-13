class team:
    def __init__(self, id, franchise_id, leagueId, teamLogo, fullName, rawTricode, tricode):
        self.id = id
        self.franchise_id = franchise_id
        self.leagueId = leagueId
        self.teamLogo = teamLogo
        self.fullName = fullName
        self.rawTricode = rawTricode
        self.triCode = tricode


class player:
    def __init__(self, id, teamID, headshot, number, firstName, lastName, position, shootsCatches, heightCm, weightKg, playerId):
        self.id = id
        self.teamID = teamID
        self.headshot = headshot
        self.number = number
        self.firstName = firstName
        self.lastName = lastName
        self.position = position
        self.shootsCatches = shootsCatches
        self.heightCm = heightCm
        self.weightKg = weightKg
        self.playerId = playerId


class scheduled_game:
    def __init__(self, game_Id, season, date, update_time, home_team_Id, away_team_Id, home_team_triCode, away_team_triCode):
        self.game_Id = game_Id
        self.season = season
        self.date = date
        self.update_time = update_time
        self.home_team_Id = home_team_Id
        self.away_team_Id = away_team_Id
        self.home_team_triCode = home_team_triCode
        self.away_team_triCode = away_team_triCode

    # Might be worth making the check function for whether this has passed an inherent function of the class

# Y is game logbook api call for the player,
# X is the player stats aggregate by seasons,
# C is additional stats aggregated by seasons
class skater_stats:
    def __init__(self, id, playerId, season, playoffs, gamesPlayed, goals, assists, points, plusMinus, pointsPerGame, evenStrengthGoals, evenStrengthPoints, powerPlayGoals, powerPlayPoints, shortHandedGoals, shortHandedPoints, overTimeGoals, gameWinningGoals, gameFirstGoals, hits, blockedShots, emptyNetGoals, FaceoffWinPercentage):
        self.id = id,
        self.playerId = playerId, #Y,X
        self.season = season, #Y,X
        self.playoffs = playoffs, #Y
        self.gamesPlayed = gamesPlayed, #X, C
        self.goals = goals, #Y, X
        self.assists = assists, #Y, X
        self.points = points, #Y, X
        self.plusMinus = plusMinus, #Y, X
        self.pointsPerGame = pointsPerGame, #X
        self.evenStrengthGoals = evenStrengthGoals, #X
        self.evenStrengthPoints = evenStrengthPoints, #X
        self.powerPlayGoals = powerPlayGoals, #Y, X
        self.powerPlayPoints = powerPlayPoints,#Y, X
        self.shortHandedGoals = shortHandedGoals, #Y, X
        self.shortHandedPoints = shortHandedPoints, #Y, X
        self.overTimeGoals = overTimeGoals, #Y, X, C
        self.gameWinningGoals = gameWinningGoals, #Y, X
        self.gameFirstGoals = gameFirstGoals, #X, C
        self.hits = hits, #C
        self.blockedShots = blockedShots, #C
        self.emptyNetGoals = emptyNetGoals, #C
        self.FaceoffWinPercentage = FaceoffWinPercentage #X
