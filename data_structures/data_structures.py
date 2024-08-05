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
