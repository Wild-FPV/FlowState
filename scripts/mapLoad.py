import bge
logic = bge.logic
flowState = logic.flowState
import ast
import os
import math
cont = logic.getCurrentController()
blendPath = logic.expandPath("//")
def readFile(fileName):
    fileName = blendPath+"maps"+os.sep+fileName
    logic.flowState.log("loading map: "+fileName)
    saveDataString = ""
    with open(fileName) as data:
        for line in data:
            saveDataString+=str(line)
    logic.flowState.log("map load complete...")
    return ast.literal_eval(saveDataString)

def main():
    if(flowState.getGameMode()!=flowState.GAME_MODE_MULTIPLAYER) and (flowState.getGameMode()!=flowState.GAME_MODE_TEAM_RACE):
        selectedMap = logic.flowState.getSelectedMap()
        mapData = readFile(selectedMap)
        spawnMapElements(mapData)

def spawnMapElements(mapData):
    scene = logic.getCurrentScene()
    flowState.log("getting assets...")
    flowState.log(len(mapData['assets']))
    try:
        owner = logic.getCurrentScene().objects['Game']
    except:
        owner = logic.getCurrentScene().objects['Game.001']
    #clear any dead checkpoints
    logic.flowState.track['checkpoints'] = []

    for asset in mapData['assets']:
        spawn = object


        #owner.orientation = asset['o']

        if('s' in asset):
            s = asset['s']
            if asset['n']=="asset checkpoint square":
                owner.localScale = [s[0],0.1,s[2]] #checkpoints should always be fixed depth
            else:
                owner.localScale = s
        o = asset['o']
        mirror = False
        if mirror:
            owner.position = [-asset['p'][0],asset['p'][1],asset['p'][2]]
            owner.orientation = [math.radians(o[0]),math.radians(o[1]),-math.radians(o[2])]
        else:
            es = 1
            esx = es*1
            esy = es*1
            owner.position = [asset['p'][0]*esx,asset['p'][1]*esy,asset['p'][2]]
            owner.orientation = [math.radians(o[0]),math.radians(o[1]),math.radians(o[2])]
        #cont.actuators['spawner']
        newObj = scene.addObject(asset['n'],owner,0)
        newObj['solid'] = True
        for child in newObj.childrenRecursive:
            if 'spawn' in child: #we don't want spawners adding junk when we edit them
                child.endObject()
        if('m' in asset):
            flowState.debug("found metadata for asset: "+str(asset))
            m = asset['m']
            newObj['metadata'] = m
        if('m' not in  asset):
            flowState.debug("found no metadata for asset: "+str(asset))
            flowState.addMetadata(newObj)
            asset['m'] = newObj['metadata']
        if(asset['m'] == {}):
            flowState.debug("found empty metadata for asset: "+str(asset))
            flowState.addMetadata(newObj)
        if('id' not in asset['m']):
            flowState.debug("found no ID in metadata for asset: "+str(asset))
            flowState.addMetadata(newObj)
        #print("loading metadata: "+str(newObj['metadata']))
        if(asset['n'] == flowState.ASSET_START_FINISH):
            logic.flowState.track['startFinishPlane'] = newObj
            flowState.log("added start finish gate")
        if('checkpoint order' in newObj['metadata']):
            logic.flowState.track['checkpoints'].append(newObj)
            if newObj['metadata']['checkpoint order'] > logic.flowState.track['lastCheckpoint']:
                logic.flowState.track['lastCheckpoint'] = newObj['metadata']['checkpoint order']

        if(asset['n'] == "asset launch pad"):
            newSpawnPoint = newObj
            if logic.flowState.track['launchPads']!=[]:
                print("adding launch pad "+str(newSpawnPoint.name))
                logic.flowState.track['launchPads'].append(newSpawnPoint)
            else:
                print("creating launch pads "+str(newSpawnPoint.name))
                logic.flowState.track['launchPads'] = [newSpawnPoint]

            print(str(logic.flowState.track['launchPads']))
    #flowState.mapLoadStage = flowState.MAP_LOAD_STAGE_DONE
