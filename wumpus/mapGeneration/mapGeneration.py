import random

def initialMap():
    map = [[[]for x in range(5)] for x in range(5)]
    wumpusGetIntoMap(map)
    holeGetIntoMap(map)
    goldIntoMap(map)
    return map

def wumpusGetIntoMap(map):
    row = 4
    column = 0
    while row == 4 and column == 0:
        row = random.randint(0,4)
        column = random.randint(0,4)
    map[row][column].append("wumpus")

    if row < 4:
        map[row+1][column].append("odor")
    if row > 0:
        map[row-1][column].append("odor")
    if column < 4:
        map[row][column+1].append("odor")
    if column > 0:
        map[row][column-1].append("odor")



def holeGetIntoMap(map):
    for row in range(0,len(map)):
        for column in range(0,len(map[row])):
            roll = random.randint(1,5)
            if roll == 1 and not (row == 4 and column == 0):
                map[row][column].append("hole")
                if row < 4 and 'wind' not in map[row + 1][column]:
                    map[row + 1][column].append("wind")
                if row > 0 and 'wind' not in map[row - 1][column]:
                    map[row - 1][column].append("wind")
                if column < 4 and 'wind' not in map[row][column + 1]:
                    map[row][column + 1].append("wind")
                if column > 0 and 'wind' not in map[row][column - 1]:
                    map[row][column - 1].append("wind")

def goldIntoMap(map):
    row = 4
    column = 0
    while (row == 4 and column == 0) or ('wumpus' in map[row][column]) or ('hole' in map[row][column]):
        row = random.randint(0,4)
        column = random.randint(0,4)
    map[row][column].append("gold")