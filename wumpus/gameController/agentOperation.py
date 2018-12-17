def move(row,column,direct):
    if direct == "up":
        return moveUp(row,column)
    elif direct == "down":
        return moveDown(row,column)
    elif direct == "left":
        return moveLeft(row,column)
    else:
        return moveRight(row,column)


def moveRight(row,column):
    return row,column + 1

def moveLeft(row,column):
    return row,column - 1

def moveUp(row,column):
    return row - 1,column

def moveDown(row,column):
    return row + 1,column

def shoot(map,row,column,direct):
    kill = False
    for i in range(0,5):
        for j in range(0,5):
            if "odor" in map[i][j]:
                map[i][j].remove("odor")
    if direct == "up":
        if "wumpus" in map[row - 1][column]:
            kill = True
            map[row - 1][column].remove("wumpus")

    elif direct == "down":
        if "wumpus" in map[row + 1][column]:
            kill = True
            map[row + 1][column].remove("wumpus")
    elif direct == "left":
        if "wumpus" in map[row][column - 1]:
            kill = True
            map[row][column-1].remove("wumpus")
    else:
        if "wumpus" in map[row][column + 1]:
            kill = True
            map[row][column + 1].remove("wumpus")
    return kill

