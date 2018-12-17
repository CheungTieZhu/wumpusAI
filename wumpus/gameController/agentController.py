from gameController.agentOperation import *
from gameController.Constant import constant
import random

class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.up = None
        self.down = None

def agentInitial(map):
    agentMap = [[[]for x in range(5)] for x in range(5)]
    survive = True
    leave = False
    arrow = 1
    current_row = 4
    current_column = 0
    shootAction = False
    riskyMove = False
    while 'gold' not in map[current_row][current_column]:
        constant.score -= 1
        if not(current_column == 0 and current_row == 4) and not shootAction and not riskyMove:
            agentMap[current_row][current_column].remove("safe")
        if "pass" not in agentMap[current_row][current_column]:
            if riskyMove:
                agentMap[current_row][current_column] = []
            agentMap[current_row][current_column].append("pass")
        w_risky_move, h_risky_move = agentSensor(map,agentMap,current_row,current_column,arrow)
        # random shoot
        if (len(w_risky_move) == 2 or len(w_risky_move) ==1) and arrow == 1:
            constant.score -= 10
            direct = w_risky_move[random.randint(0,len(w_risky_move)-1)]
            kill = shoot(map,current_row,current_column,direct)
            arrow = 0
            remove_wumpus_alarm(kill, w_risky_move, agentMap, current_row, current_column, direct)
            shootAction = True
            riskyMove = False
        # safe
        elif len(w_risky_move) == 0 and len(h_risky_move) == 0:
            move_direction = location_safe_detected(current_row, current_column, agentMap,map)
            if len(move_direction) == 0:
                current_row,current_column,isSafe = findAnotherWay(current_row, current_column, agentMap)
                if not isSafe:
                    leave = True
                    break
            else:
                direct = move_direction[random.randint(0,len(move_direction)-1)]
                current_row,current_column = move(current_row,current_column,direct)
            shootAction = False
            riskyMove = False
        elif (len(h_risky_move) == 3 and len(w_risky_move) == 3):
            riskyMove = True
            direct = w_risky_move[random.randint(0, len(w_risky_move) - 1)]
            current_row, current_column = move(current_row,current_column,direct)
            shootAction = False
        elif (len(h_risky_move) == 3 and len(w_risky_move) == 0):
            riskyMove = True
            direct = h_risky_move[random.randint(0, len(h_risky_move) - 1)]
            current_row, current_column = move(current_row,current_column,direct)
            shootAction = False
        elif (len(h_risky_move) == 0 and len(w_risky_move) == 3):
            riskyMove = True
            direct = w_risky_move[random.randint(0, len(w_risky_move) - 1)]
            current_row, current_column = move(current_row,current_column,direct)
            shootAction = False
        elif len(h_risky_move) == 2 or len(h_risky_move) == 1:
            no_way_to_go = True
            if current_row < 4:
                if "safe" in agentMap[current_row + 1][current_column]:
                    no_way_to_go = False
                    current_row += 1
            if current_row > 0:
                if "safe" in agentMap[current_row - 1][current_column]:
                    no_way_to_go = False
                    current_row -= 1
            if current_column < 4:
                if "safe" in agentMap[current_row][current_column + 1]:
                    no_way_to_go = False
                    current_column += 1
            if current_column > 0:
                if "safe" in agentMap[current_row][current_column - 1]:
                    no_way_to_go = False
                    current_column -= 1
            shootAction = False
            isSafe = False
            riskyMove = False
            if no_way_to_go:
                current_row, current_column, isSafe = findAnotherWay(current_row, current_column, agentMap)
                if isSafe == False:
                    leave = True
                    break







        if 'hole' in map[current_row][current_column] or 'wumpus' in map[current_row][current_column]:
            survive = False
            constant.score -= 1000
            print('Agent dead!')
            break
    if survive and not leave:
        constant.score += 1000
        print("Yeah! got gold")
    elif survive and leave:
        print("leave")



def agentSensor(map,agentMap,current_row,current_column,arrow):
    w_risky_move = []
    h_risky_move = []
    if 'wind' in map[current_row][current_column]:
        if current_row < 4 and "pass" not in agentMap[current_row + 1][current_column] and "hole?"  not in agentMap[current_row + 1][current_column] and "safe" not in agentMap[current_row + 1][current_column]:
            agentMap[current_row + 1][current_column].append("hole?")
            h_risky_move.append("down")
        if current_row > 0 and "pass" not in agentMap[current_row - 1][current_column] and "hole?"  not in agentMap[current_row - 1][current_column] and "safe"  not in agentMap[current_row - 1][current_column]:
            agentMap[current_row - 1][current_column].append("hole?")
            h_risky_move.append("up")
        if current_column < 4 and "pass" not in agentMap[current_row][current_column + 1] and "hole?"  not in agentMap[current_row][current_column + 1] and "safe"  not in agentMap[current_row][current_column + 1]:
            agentMap[current_row][current_column + 1].append("hole?")
            h_risky_move.append("right")
        if current_column > 0 and "pass" not in agentMap[current_row][current_column - 1] and "hole?"  not in agentMap[current_row][current_column - 1] and "safe"  not in agentMap[current_row][current_column - 1]:
            agentMap[current_row][current_column - 1].append("hole?")
            h_risky_move.append("left")

    if 'odor' in map[current_row][current_column] and arrow == 1:
        if current_row < 4 and "pass"  not in agentMap[current_row + 1][current_column] and "wumpus?"  not in agentMap[current_row + 1][current_column] and "safe" not in agentMap[current_row + 1][current_column]:
            agentMap[current_row + 1][current_column].append("wumpus?")
            w_risky_move.append("down")
        if current_row > 0 and "pass" not in agentMap[current_row - 1][current_column] and "wumpus?"  not in agentMap[current_row - 1][current_column] and "safe" not in agentMap[current_row - 1][current_column]:
            agentMap[current_row - 1][current_column].append("wumpus?")
            w_risky_move.append("up")
        if current_column < 4 and "pass" not in agentMap[current_row][current_column + 1] and "wumpus?"  not in agentMap[current_row][current_column + 1] and "safe" not in agentMap[current_row][current_column + 1]:
            agentMap[current_row][current_column + 1].append("wumpus?")
            w_risky_move.append("right")
        if current_column > 0 and "pass" not in agentMap[current_row][current_column - 1] and "wumpus?"  not in agentMap[current_row][current_column - 1] and "safe" not in agentMap[current_row][current_column - 1]:
            agentMap[current_row][current_column - 1].append("wumpus?")
            w_risky_move.append("left")

    return w_risky_move,h_risky_move

def remove_wumpus_alarm(kill,w_risky_move,agentMap,current_row,current_column,direct):
    if kill == True:
        for i in w_risky_move:
            if i == "up":
                agentMap[current_row - 1][current_column].remove("wumpus?")
            elif i == "down":
                agentMap[current_row + 1][current_column].remove("wumpus?")
            elif i == "left":
                agentMap[current_row][current_column - 1].remove("wumpus?")
            else:
                agentMap[current_row][current_column + 1].remove("wumpus?")
    else:
        if direct == "up":
            agentMap[current_row - 1][current_column].remove("wumpus?")
        elif direct == "down":
            agentMap[current_row + 1][current_column].remove("wumpus?")
        elif direct == "left":
            agentMap[current_row][current_column - 1].remove("wumpus?")
        else:
            agentMap[current_row][current_column + 1].remove("wumpus?")
        w_risky_move.remove(direct)
        if len(w_risky_move) == 1:
            if w_risky_move[0] == "up":
                agentMap[current_row - 1][current_column].remove("wumpus?")
                agentMap[current_row - 1][current_column].append("unsafe")
            elif w_risky_move[0] == "down":
                agentMap[current_row + 1][current_column].remove("wumpus?")
                agentMap[current_row + 1][current_column].append("unsafe")
            elif w_risky_move[0] == "left":
                agentMap[current_row][current_column - 1].remove("wumpus?")
                agentMap[current_row][current_column - 1].append("unsafe")
            else:
                agentMap[current_row][current_column + 1].remove("wumpus?")
                agentMap[current_row][current_column + 1].append("unsafe")

def location_safe_detected(current_row,current_column,agentMap,map):
    move_direction = []
    if current_row < 4 and "pass" not in agentMap[current_row + 1][current_column] and "wumpus" not in map[current_row + 1][current_column]:
        agentMap[current_row + 1][current_column] = []
        agentMap[current_row + 1][current_column].append("safe")
        move_direction.append("down")
    if current_row > 0 and "pass" not in agentMap[current_row - 1][current_column] and "wumpus" not in map[current_row - 1][current_column]:
        agentMap[current_row - 1][current_column] = []
        agentMap[current_row - 1][current_column].append("safe")
        move_direction.append("up")
    if current_column < 4 and "pass" not in agentMap[current_row][current_column + 1] and "wumpus" not in map[current_row][current_column + 1]:
        agentMap[current_row][current_column + 1] = []
        agentMap[current_row][current_column + 1].append("safe")
        move_direction.append("right")
    if current_column > 0 and "pass" not in agentMap[current_row][current_column - 1]  and "wumpus" not in map[current_row][current_column - 1]:
        agentMap[current_row][current_column - 1] = []
        agentMap[current_row][current_column - 1].append("safe")
        move_direction.append("left")

    return move_direction

def findAnotherWay(current_row,current_column,agentMap):
    isSafe = False
    aim_row = 0
    aim_column = 4
    if current_row < 4:
        if "safe" not in agentMap[current_row + 1][current_column] and "unsafe" not in agentMap[current_row][
            current_column] and "pass" not in agentMap[current_row + 1][current_column]:
            agentMap[current_row][current_column].append("unsafe")
    if current_row > 0:
        if "safe" not in agentMap[current_row - 1][current_column] and "unsafe" not in agentMap[current_row][
            current_column] and "pass" not in agentMap[current_row - 1][current_column]:
            agentMap[current_row][current_column].append("unsafe")
    if current_column < 4:
        if "safe" not in agentMap[current_row][current_column + 1] and "unsafe" not in agentMap[current_row][
            current_column] and "pass" not in agentMap[current_row][current_column + 1]:
            agentMap[current_row][current_column].append("unsafe")
    if current_column > 0:
        if "safe" not in agentMap[current_row][current_column - 1] and "unsafe" not in agentMap[current_row][
            current_column] and "pass" not in agentMap[current_row][current_column - 1]:
            agentMap[current_row][current_column].append("unsafe")
    for i in range(0, 5):
        for j in range(0, 5):
            if "safe" in agentMap[i][j]:
                aim_row = i
                aim_column = j
                isSafe = True
                moveDistance = moveToLocationDistance(agentMap, current_row, current_column, aim_row, aim_column)
                constant.score -= moveDistance
                break
    return aim_row,aim_column,isSafe

def moveToLocationDistance(agentMap,current_row,current_column,aim_row,aim_column):
    rootNode = [current_row,current_column]
    root = Tree()
    root.value = rootNode
    treeGetValue(root,agentMap,root.value)
    moveStep = bfsInsert(root,agentMap,current_row,current_column,aim_row,aim_column)
    return moveStep

def bfsInsert(root,agentMap,current_row,current_column,aim_row,aim_column):
    visited = []
    visited.append(root)
    current = root
    row = current_row
    column = current_column
    while current:
        if (column == aim_column - 1 and row == aim_row) or (column == aim_column + 1 and row == aim_row) or (column == aim_column and row == aim_row - 1) or (column == aim_column and row == aim_row + 1):
            break
        if current.left:
            if (column == aim_column - 1 and row == aim_row) or (column == aim_column + 1 and row == aim_row) or (
                    column == aim_column and row == aim_row - 1) or (column == aim_column and row == aim_row + 1):
                break
            if current.left.value:
                row, column = treeGetValue(current.left,agentMap,current.left.value)
                visited.append(current.left)
        if current.right:
            if (column == aim_column - 1 and row == aim_row) or (column == aim_column + 1 and row == aim_row) or (
                    column == aim_column and row == aim_row - 1) or (column == aim_column and row == aim_row + 1):
                break
            if current.right.value:
                row, column = treeGetValue(current.right,agentMap,current.right.value)
                visited.append(current.right)
        if current.up:
            if (column == aim_column - 1 and row == aim_row) or (column == aim_column + 1 and row == aim_row) or (
                    column == aim_column and row == aim_row - 1) or (column == aim_column and row == aim_row + 1):
                break
            if current.up.value:
                row, column = treeGetValue(current.up,agentMap,current.up.value)
                visited.append(current.up)
        if current.down:
            if (column == aim_column - 1 and row == aim_row) or (column == aim_column + 1 and row == aim_row) or (column == aim_column and row == aim_row - 1) or (column == aim_column and row == aim_row + 1):
                break
            if current.down.value:
                row, column = treeGetValue(current.down,agentMap,current.down.value)
                visited.append(current.down)
        visited.pop(0)

        if not visited:
            break
        current = visited[0]

    return len(visited)


def treeGetValue(root,agentMap,location):
    if location[1] > 0:
        if "pass" in agentMap[location[0]][location[1] - 1]:
            root.left = Tree()
            root.left.value = [location[0],location[1] -1]
    if location[1] < 4:
        if "pass" in agentMap[location[0]][location[1] + 1]:
            root.right = Tree()
            root.right.value = [location[0],location[1] + 1]
    if location[0] > 0:
        if "pass" in agentMap[location[0] - 1][location[1]]:
            root.up = Tree()
            root.up.value = [location[0] - 1,location[1]]
    if location[0] < 4:
        if "pass" in agentMap[location[0] + 1][location[1]]:
            root.down = Tree()
            root.down.value = [location[0] + 1,location[1]]

    return location[0],location[1]






