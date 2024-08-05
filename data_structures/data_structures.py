class skaterStats:
    def __init__(self, id, playerId, season, playoffs, gamesPlayed, goals, assists, points, plusMinus, pointsPerGame, evenStrengthGoals, evenStrengthPoints, powerPlayGoals, powerPlayPoints, shortHandedGoals, shortHandedPoints, overTimeGoals, gameWinningGoals, gameFirstGoals, hits, blockedShots, emptyNetGoals, FaceoffWinPercentage):
        self.id = id,
        self.playerId = playerId, #Y
        self.season = season, #Y
        self.playoffs = playoffs, #Y
        self.gamesPlayed = gamesPlayed, #get the length of the gamelog
        self.goals = goals, #Y
        self.assists = assists, #Y
        self.points = points, #Y
        self.plusMinus = plusMinus, #Y
        self.pointsPerGame = pointsPerGame, #DO a function to grab average
        self.evenStrengthGoals = evenStrengthGoals,
        self.evenStrengthPoints = evenStrengthPoints,
        self.powerPlayGoals = powerPlayGoals, #Y
        self.powerPlayPoints = powerPlayPoints,#Y
        self.shortHandedGoals = shortHandedGoals, #Y
        self.shortHandedPoints = shortHandedPoints, #Y
        self.overTimeGoals = overTimeGoals, #Y
        self.gameWinningGoals = gameWinningGoals, #Y
        self.gameFirstGoals = gameFirstGoals,
        self.hits = hits,
        self.blockedShots = blockedShots,
        self.emptyNetGoals = emptyNetGoals,
        self.FaceoffWinPercentage = FaceoffWinPercentage
