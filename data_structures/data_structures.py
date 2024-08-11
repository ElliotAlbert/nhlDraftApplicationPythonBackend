
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
