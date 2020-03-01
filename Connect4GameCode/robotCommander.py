import S71200       # S71200 Library
from time import sleep
from time import time
import snap7
from snap7.util import *
import struct
from game import game
from game import difficulty
from player import player, playerType
import random

class runState(object):
    hold=0
    home=1
    sort=2
    transfer=3
    gamePos1=4
    gamePos2=5
    gamePos3=6
    gamePos4=7

class robotCommander():
    def __init__(self):
        self.Player1 = player(playerType.robot, 1,'r',0)
        self.Player2 = player(playerType.robot, 2,'b',0)
        self.Player1.opponent = self.Player2
        self.Player2.opponent = self.Player1
        self.gamePositions = 'A','B','C','D'
        self.currentGame = game(self.Player1, self.Player2)
        self.plc = S71200.S71200("151.141.148.26")

    def showMenu(self):
        menuChoice = ""
        menuText = ("----- Main Menu -----"
                    "\n\t1. Robot Commands"
                    "\n\t2. Game Settings"
                    "\n\t3. Exit"
                    "\nEnter an option: ")
        while menuChoice != '3':
            print(menuText)
            menuChoice = input()
            if menuChoice == '1':
                self.robotMenu()
            elif menuChoice == '2':
                self.gameSetings()
            elif menuChoice == '3':
                print("Returning to the game...")
            else:
                print("Enter a valid menu option!\n\n")

    def robotMenu(self):
        menuChoice = ""
        menuText = ("----- Robot Commands -----"
                    "\n\t1. Go Home"
                    "\n\t2. Pick Red"
                    "\n\t3. Pick Black"
                    "\n\t4. Sort"
                    "\n\t5. Return")
        while menuChoice != '5':
            print(menuText)
            menuChoice = input()
            if menuChoice == '1':
                print("Executing Go Home")
                self.stopBelt()
                self.setRobotMode(1, runState.home)
                self.setRobotMode(2, runState.home)
                sleep(5)
                self.setRobotMode(1, runState.hold)
                self.setRobotMode(2, runState.hold)

            elif menuChoice == '2':
                print("Executing Pick Red")
                self.stopBelt()
                print("Enter a column to place:", end=" ")
                col = input().upper()
                if col == 'A':
                    self.setRobotMode(1, runState.gamePos1)
                elif col == 'B':
                    self.setRobotMode(1, runState.gamePos2)
                elif col == 'C':
                    self.setRobotMode(1, runState.gamePos3)
                elif col == 'D':
                    self.setRobotMode(1, runState.gamePos4)

                sleep(5)
                self.setRobotMode(1, runState.hold)
                
            elif menuChoice == '3':
                print("Executing Pick Black")
                self.stopBelt()
                print("Enter a column to place:", end=" ")
                col = input().upper()
                if col == 'A':
                    self.setRobotMode(2, runState.gamePos1)
                elif col == 'B':
                    self.setRobotMode(2, runState.gamePos2)
                elif col == 'C':
                    self.setRobotMode(2, runState.gamePos3)
                elif col == 'D':
                    self.setRobotMode(2, runState.gamePos4)

                sleep(5)
                self.setRobotMode(2, runState.hold)

            elif menuChoice == '4':
                print("Executing Sort Routine")
                self.cleanUp()
            elif menuChoice == '5':
                print("Returning to main menu...")

            else:
                print("Enter a valid menu option!\n\n")
    def gameSetings(self):
        menuChoice = ""
        menuText = ("----- Game Settings -----"
                    "\n\t1. Player 1 Mode"
                    "\n\t2. Player 2 Mode"
                    "\n\t3. Difficulty"
                    "\n\t4. Game Information"
                    "\n\t5. Return")
        while menuChoice != '5':
            print(menuText)
            menuChoice = input()
            if menuChoice == '1':
                print("----- Mode Options -----"
                    "\n\t1. Human"
                    "\n\t2. Robot")
                print("Set Player 1 Mode:")
                mode = input()
                if mode == '1':
                    self.Player1.type = playerType.human
                elif mode == '2':
                    self.Player1.type = playerType.robot
                else:
                    print("Invalid mode choice!")

            elif menuChoice == '2':
                print("----- Mode Options -----"
                    "\n\t1. Human"
                    "\n\t2. Robot")
                print("Set Player 2 Mode:")
                mode = input()
                if mode == '1':
                    self.Player2.type = playerType.human
                elif mode == '2':
                    self.Player2.type = playerType.robot
                else:
                    print("Invalid mode choice!")
                
            elif menuChoice == '3':
                print("----- Robot Difficulty Options -----"
                    "\n\t1. Easy"
                    "\n\t2. Medium"
                    "\n\t3. Hard"
                    "\n\t4. Expert")
                print("Set Robot Difficulty:")
                mode = input()
                if mode == '1':
                    self.currentGame.level = difficulty.easy
                elif mode == '2':
                    self.currentGame.level = difficulty.medium
                elif mode == '3':
                    self.currentGame.level = difficulty.hard
                elif mode == '4':
                    self.currentGame.level = difficulty.expert
                else:
                    print("Invalid difficulty choice!")

            elif menuChoice == '4':
                gameInformation()
            elif menuChoice == '5':
                print("Returning to main menu...")
            else:
                print("Enter a valid menu option!\n\n")

    def gameInformation(self):
        print("Board Width:", self.currentGame.boardWidth)
        print("Board Height:", self.currentGame.boardHeight)
        print("Red:", self.currentGame.players[0].id, self.currentGame.players[0].wins)
        print("Black:", self.currentGame.players[1].id, self.currentGame.players[1].wins)
        print("Current Player:", self.currentGame.currentPlayer.id)
        print("Game Board:\n")
        self.currentGame.showGrid()
        print("\n\n")


    def stopBelt(self):
        self.plc.writeMem('QX0.0', False)
        self.plc.writeMem('QX0.1', False)

    def moveBelt(self, direction):
        self.plc.writeMem('QX0.0', direction)
        self.plc.writeMem('QX0.1', not direction)

    # Performs Cleanup Routine
    def cleanUp(self):
        # Begin robot 2 cleanup (drop pieces)
        self.setRobotMode(2, runState.sort)
        io1 = self.plc.getMem('IX8.1')
        # Wait unitl signal is received that pieces are dropped
        while io1 == False:
            sleep(1)
            io1 = self.plc.getMem('IX8.1')

        self.setRobotMode(2, runState.hold)

        # Oscillate belt to align peices
        for n in range(8):
            self.moveBelt(1)
            sleep(1)
            self.moveBelt(0)
            sleep(1.5)
        
        # Begin robot 1 cleanup (sort)
        self.setRobotMode(1, runState.sort)
        sleep(1)
        io0 = self.plc.getMem('IX8.0')
        io1 = self.plc.getMem('IX8.1')
        tout = 20.0
        t0 = time()
        tw = time()
        intA = 5.0
        intB = 1.0
        # Continue sorting until timeout
        while time() - t0 < tout and io1 == True:
            tw = time()
            # Non-Blocking belt oscillation
            while time() - tw < intB and io0 == False:
                io0 = self.plc.getMem('IX8.0')
                self.moveBelt(1)
                sleep(0.25)

            tw = time()
            while time() - tw < intA and io0 == False:
                io0 = self.plc.getMem('IX8.0')
                self.moveBelt(0)
                sleep(0.25)

            # Move belt forward to keep pieces at end
            while io0 == True:
                self.moveBelt(0)
                print("Prep Grab Forward")
                sleep(1)
                t0 = time()
                io0 = self.plc.getMem('IX8.0')

            io1 = self.plc.getMem('IX8.1')

        # Begin transfer routine
        self.Transfer()
        self.stopBelt()

    def Transfer(self):
        # Set robot 1 & 2 to clean up
        self.setRobotMode(1, runState.transfer)
        self.setRobotMode(2, runState.transfer)

        sleep(1)
        io0 = self.plc.getMem('IX8.0')
        io1 = self.plc.getMem('IX8.1')
        self.moveBelt(1)
        tWait = 20
        t0 = time()
        count = 0
        # Loop until timeout expires or both robots are done (state is low)
        while time() - t0 < tWait and (io0 == True or io1 == True):
            io0 = self.plc.getMem('IX8.0')
            io1 = self.plc.getMem('IX8.1')
            if io0 == True:
                t0 = time()

            sleep(0.25)
            count+=1
            if count == 40:
                self.setRobotMode(1, runState.hold)
                self.setRobotMode(2, runState.hold)
        
        self.stopBelt


    def setRobotMode(self, robot, runState):
        setVal = runState
        reg = '7'
        output = self.plc.getMem('MW{0}'.format(reg), True)
        block = output[1]
        mask = 0b11110000
        if robot == 1:
            block = block & mask
            setVal = setVal & ~mask
        elif robot == 2:
            mask = ~mask
            block = block & mask
            setVal = setVal << 4
        else:
            return False

        block = block | setVal
        #print('Status: {0} | {1:b} | {2:b} | {3:b} | {4:b}'.format(robot, mode, value, setVal, block))
        self.plc.writeMem('MB{0}'.format(reg), block)
        return True

    def readInput(self):
        value = input().upper()
        robotState = runState.hold
        if value == 'A':
            robotState = runState.gamePos1
        elif value == 'B':
            robotState = runState.gamePos2
        elif value == 'C':
            robotState = runState.gamePos3
        elif value == 'D':
            robotState = runState.gamePos4
        elif value == 'MENU':
            self.showMenu()
        else:
            robotState = runState.hold
            print('Invalid move!')
        return robotState

    def start(self, numRounds=1):
        try:
            self.setRobotMode(1, runState.home)
            self.setRobotMode(2, runState.home)
            sleep(5)
            self.setRobotMode(1, runState.hold)
            self.setRobotMode(2, runState.hold)
            while self.plc.getMem('IX8.0') == True or self.plc.getMem('IX8.1') == True:
                sleep(0.5)

            keepGoing = True
            for i in range(numRounds):
                print("Game {0} of {1}".format(i+1, numRounds))
                self.currentGame = game(self.Player1, self.Player2)
                while keepGoing:
                    currentId = self.currentGame.currentPlayer.id
                    if self.currentGame.currentPlayer.type == playerType.robot:
                        if self.currentGame.remaining == game.boardHeight * game.boardWidth:
                            movePos = random.randint(0,3)
                        else:
                            movePos = self.currentGame.findBestMove().col
                        print("Player",currentId, "moves to", self.gamePositions[movePos])
                        movePos += 4
                    elif self.currentGame.currentPlayer.type == playerType.human:
                        print("Player",currentId," - Enter a move: ")
                        movePos = self.readInput()

                    if movePos >= 4:
                        self.setRobotMode(currentId, movePos)
                        sleep(1)
                        matchFound = self.currentGame.move(self.currentGame
                        .currentPlayer, movePos)
                    
                        self.currentGame.showGrid()
                        self.setRobotMode(currentId, runState.hold)
                        if currentId == 1:
                            while self.plc.getMem('IX8.0') == True:
                                sleep(0.5)
                        elif currentId == 2:
                            while self.plc.getMem('IX8.1') == True:
                                sleep(0.5)
                        print(matchFound)
                        if (matchFound == True):
                            print("Player", currentId, "Wins!")
                            keepGoing = False
                        elif self.currentGame.remaining == 0:
                            keepGoing = False
                print("Game Over!")
                sleep(10)
                self.cleanUp()

        except Exception as ex:
            print("An error occured during runtine: ", ex)

        finally:
            if self.plc.plc.get_connected:
                self.stopBelt()
                self.setRobotMode(1, runState.hold)
                self.setRobotMode(2, runState.hold)
                self.plc.plc.disconnect()
