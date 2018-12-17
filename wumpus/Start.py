from mapGeneration.mapGeneration import initialMap
from gameController.agentController import agentInitial
from gameController.Constant import constant

def main():
    runTime = 100
    while runTime > 0:
        constant.score = 0
        print("map generating ....")
        map = initialMap()
        print("map completed!")
        agentInitial(map)
        runTime -= 1
        print(constant.score)



main()