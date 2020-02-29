class playerType:
    human = 0
    robot = 1
    
class player:
    def __init__(self, newType = playerType.robot, newId = 0, newSym = '#', newWins= 0):
        self.type = newType
        self.id = newId
        self.symbol = newSym
        self.opponent = None
        self.wins = newWins
