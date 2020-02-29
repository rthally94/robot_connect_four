from player import player
from time import sleep
import random
class Move(object):
    row = 0
    col = 0
class difficulty(object):
    easy = 2
    medium = 4
    hard = 5
    expert = 8

class game:
    numPlayers = 2
    boardWidth = 4
    boardHeight = 4
    currentPlayer = player()
    opponent = player()
    numMatches = 3
    level = difficulty.expert

    def __init__(self, Player1, Player2):
        game.players = [Player1, Player2]
        choice = random.randint(0,1)
        game.currentPlayer = game.players[choice]
        self.board = []
        for n in range(game.boardWidth):
            self.board.append([])

        self.remaining = 0
        self.clear()

    def clear(self):
        self.remaining = game.boardWidth * game.boardHeight
        for col in self.board:
            col.clear()
            for n in range(game.boardHeight):
                col.append('_')

    def move(self, inPlayer, column):
        col = column - 4
        row = len(self.board[col]) - self.board[col].count('_')
        if (game.currentPlayer.id == 1):
            self.board[col][row] ='r'
        elif (game.currentPlayer.id == 2):
            self.board[col][row] = 'b'
        else:
            return False
        game.currentPlayer = game.currentPlayer.opponent
        self.remaining-=1
        return self.matchFound(col, row)

    def isMovesLeft(self):
        for row in range(game.boardHeight):
            for col in range(game.boardWidth):
                if self.board[col][row] == '_':
                    return True
        return False

    def evaluate(self):
        # Check Vertical
        for col in range(self.boardWidth):
            for row in range(self.boardHeight - 2):
                if self.board[col][row] == self.board[col][row+1] and self.board[col][row+1] == self.board[col][row+2]:
                    if self.board[col][row] == game.currentPlayer.symbol:
                        return 10
                    elif self.board[col][row] == game.currentPlayer.opponent.symbol:
                        return -10

        # Check Horizontal
        for row in range(self.boardHeight):
            for col in range(self.boardWidth - 2):
                if self.board[col][row] == self.board[col+1][row] and self.board[col+1][row] == self.board[col+2][row]: 
                    if self.board[col][row] == game.currentPlayer.symbol:
                        return 10
                    elif self.board[col][row] == game.currentPlayer.opponent.symbol:
                        return -10

        # Check Diagonal
        # Check Right
        for col in range(self.boardWidth - 2):
            for row in range(self.boardHeight - 2):
                if self.board[col][row] == self.board[col+1][row+1] and self.board[col+1][row+1] == self.board[col+2][row+2]:
                    if self.board[col][row] == game.currentPlayer.symbol:
                        return 10
                    elif self.board[col][row] == game.currentPlayer.opponent.symbol:
                        return -10

        # Check Left
        for col in range(self.boardWidth - 2, self.boardWidth, 1):
            for row in range(self.boardHeight - 2):
                if self.board[col][row] == self.board[col-1][row-1] and self.board[col-1][row-1] == self.board[col-2][row-2]:
                    if self.board[col][row] == game.currentPlayer.symbol:
                        return 10
                    elif self.board[col][row] == game.currentPlayer.opponent.symbol:
                        return -10
        return 0

    def minimax(self, depth, isMax):
        score = self.evaluate()
        if depth == game.level or score == 10 or score == -10:
            #if score == -10:
                #self.showGrid()
            return score
        
        if self.isMovesLeft() == False:
            return 0

        if isMax == True:
            best = -1000
            for i in range(game.boardWidth):
                for j in range(game.boardHeight - self.board[i].count('_')): 
                    if self.board[i][j] == '_':
                        self.board[i][j] = game.currentPlayer.symbol
                        best = max(best, self.minimax(depth+1, not isMax))
                        self.board[i][j] = '_'
            return best
        else:
            best = 1000
            for i in range(game.boardWidth):
                for j in range(game.boardHeight - self.board[i].count('_')):
                    if self.board[i][j] == '_':
                        self.board[i][j] = game.currentPlayer.opponent.symbol
                        best = min(best, self.minimax(depth+1, not isMax))
                        self.board[i][j] = '_'
            return best

    def findBestMove(self):
        bestVal = -1000
        bestMove = Move()
        bestMove.row = -1
        bestMove.col = -1

        for j in range(game.boardHeight):
            for i in range(game.boardWidth):
                if self.board[i][j] == '_':
                    self.board[i][j] = game.currentPlayer.symbol
                    moveVal = self.minimax(0, False)
                    self.board[i][j] = '_'
                    if moveVal > bestVal:
                        bestMove.row = j
                        bestMove.col = i
                        bestVal = moveVal
        print("Best Move:", bestMove.col, " | ", bestMove.row, " | score:", bestVal)
        return bestMove

    def showGrid(self):
        for row in range(game.boardHeight - 1, -1, -1):
            for col in range(game.boardWidth):
                print(self.board[col][row], end=" ")
            print('\n')
        print('\n')

    def matchFound(self, col, row):
        match = self.board[col][row]
        print("Checking match - col:", col, " | row:", row, " | target:", match)
        if col < 2 and row < 2:     #Up/Right
            #Up Right Diag
            if self.board[col+1][row+1] == match:
                if self.board[col+2][row+2] == match:
                    print("Match Found!")
                    return True

            #Right
            if self.board[col+1][row] == match:
                if self.board[col+2][row] == match:
                    print("Match Found!")
                    return True

            #Up
            if self.board[col][row+1] == match:
                if self.board[col][row+2] == match:
                    print("Match Found!")
                    return True

        if col >= 2 and row < 2:  #Up/Left
            #Left
            if self.board[col-1][row] == match:
                if self.board[col-2][row] == match:
                    print("Match Found!")
                    return True
        
            #Up Left Diag
            if self.board[col-1][row+1] == match:
                if self.board[col-2][row+2] == match:
                    print("Match Found!")
                    return True

            #Up
            if self.board[col][row+1] == match:
                if self.board[col][row+2] == match:
                    print("Match Found!")
                    return True

        if col < 2 and row >= 2:  #Down/Right
            #Down Right Diag
            if self.board[col+1][row-1] == match:
                if self.board[col+2][row-2] == match:
                    print("Match Found!")
                    return True

            #Right
            if self.board[col+1][row] == match:
                if self.board[col+2][row] == match:
                    print("Match Found!")
                    return True

            #Down
            if self.board[col][row-1] == match:
                if self.board[col][row-2] == match:
                    print("Match Found!")
                    return True

        if col >= 2 and row >= 2:   #Down/Left
            #Left
            if self.board[col-1][row] == match:
                if self.board[col-2][row] == match:
                    print("Match Found!")
                    return True
        
            #Down Left Diag
            if self.board[col-1][row-1] == match:
                if self.board[col-2][row-2] == match:
                    print("Match Found!")
                    return True

            #Down
            if self.board[col][row-1] == match:
                if self.board[col][row-2] == match:
                    print("Match Found!")
                    return True

        return False