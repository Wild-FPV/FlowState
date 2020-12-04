import bge.logic as logic
import ast
import os
import math
cont = logic.getCurrentController()
owner = cont.owner
def readFile(fileName):
    fileName = "maps"+os.sep+fileName
    print("loading map data from "+str(fileName))
    saveDataString = ""
    with open(fileName) as data:
        for line in data:
            saveDataString+=str(line)
    return ast.literal_eval(saveDataString)

def main():
    selectedMap = "custom.fmp"#"2018 Regional Final.fmp"
    mapData = readFile(selectedMap)

    scene = logic.getCurrentScene()
    print("getting assets...")
    print(len(mapData['assets']))
    for asset in mapData['assets']:
        print("loading "+asset['n'])
        spawn = object
        owner.position = asset['p']
        o = asset['o']
        #owner.orientation = o
        owner.orientation = [math.radians(o[1]),math.radians(o[1]),math.radians(o[2])]

        #cont.actuators['spawner']
        newObj = scene.addObject(asset['n'],owner,0)
        newObj['solid'] = True

        if(asset['n'] == "asset launch pad"):
            newSpawnPoint = newObj
            if logic.flowState.track.launchPads!=[]:
                logic.flowState.track.launchPads.append(newSpawnPoint)
            else:
                logic.flowState.track.launchPads = [newSpawnPoint]
            print("setting launch pads "+str(logic.flowState.track.launchPads))

main()
