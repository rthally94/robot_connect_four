from robotCommander import robotCommander

current = robotCommander()

print("How many games?", end=" ")
numGames = input()

while numGames != "exit":
    if numGames == "":
        numGames = 100
        current.start(numGames)
    elif numGames == "menu":
        current.showMenu()
    else:
        numGames = int(numGames)
        current.start(numGames)
    
    print("How many games?", end=" ")
    numGames = input()
    
