import bge.logic as logic
import time
import math
import FSNObjects
from scripts.abstract.RaceState import RaceState
scene = logic.getCurrentScene()
owner = logic.getCurrentController().owner
#logic.globalDict["playerQuad"] = owner
flowState = logic.flowState
def main():
    startTime = time.perf_counter()
    if "lastGhostUpdate" not in owner:
        owner["lastGhostUpdate"] = time.perf_counter()
    if abs(time.perf_counter()-owner["lastGhostUpdate"]) > (1/60.0):
        owner["lastGhostUpdate"] = time.perf_counter()
        if(flowState.getGameMode()==flowState.GAME_MODE_SINGLE_PLAYER):
            lap = logic.flowState.getRaceState().getChannelLapCount(5658)
            if lap < 0:
                logic.ghosts = []
            else:
                if len(logic.ghosts)-1<lap:
                    ghostObject = addGhostQuad()
                    ghostObject["lap"] = lap
                    logic.ghosts.append(createGhostData(owner,ghostObject))
                currentGhost = logic.ghosts[len(logic.ghosts)-1]
                #if(lap<6):
                recordGhostData(owner,currentGhost)
                if len(logic.ghosts)>1:
                    for i in range(0,len(logic.ghosts)-1):
                        lastGhost = logic.ghosts[i]
                        setGhostData(lastGhost)
                        if(lastGhost["obj"]["spectatorCamera"]["cameraName"] == "ghost0"):
                            lastGhost["obj"]["spectatorCamera"]["cameraName"] = "ghostSpectate"+str(lap)
                        if(lastGhost["obj"]["fpvCamera"]["cameraName"] == "ghost0"):
                            lastGhost["obj"]["fpvCamera"]["cameraName"] = "ghostFPV"+str(lap)
        endTime = time.perf_counter()
        #print("main("+str(endTime-startTime))
def getFrameData(obj,ghostObject):
    digits = 3
    xa=round(obj.orientation[0][0],digits)
    xb=round(obj.orientation[0][1],digits)
    xc=round(obj.orientation[0][2],digits)
    ya=round(obj.orientation[1][0],digits)
    yb=round(obj.orientation[1][1],digits)
    yc=round(obj.orientation[1][2],digits)
    za=round(obj.orientation[2][0],digits)
    zb=round(obj.orientation[2][1],digits)
    zc=round(obj.orientation[2][2],digits)
    px = round(obj.position[0],digits)
    py = round(obj.position[1],digits)
    pz = round(obj.position[2],digits)
    lvx = round(obj.localLinearVelocity[0],digits)
    lvy = round(obj.localLinearVelocity[1],digits)
    lvz = round(obj.localLinearVelocity[2],digits)
    avx = round(obj.localAngularVelocity[0],digits)
    avy = round(obj.localAngularVelocity[1],digits)
    avz = round(obj.localAngularVelocity[2],digits)
    result = {"time":time.perf_counter(),"pos":[px,py,pz],"ori":[[xa,xb,xc],[ya,yb,yc],[za,zb,zc]],"linVel":[lvx,lvy,lvz],"angVel":[avx,avy,avz]}
    return result

def createGhostData(obj,ghostObject):
    startTime = time.perf_counter()
    result =result = {"obj":ghostObject,"currentFrame":0,"frames":[getFrameData(obj,ghostObject)],"spawnComplete":False}
    endTime = time.perf_counter()
    return result

def recordGhostData(obj, currentGhost):
    if(not logic.finishedLastLap):
        startTime = time.perf_counter()

        currentGhost["frames"].append(getFrameData(obj,currentGhost))
        endTime = time.perf_counter()
        #print("recordGhostData("+str(endTime-startTime))

def setGhostData(ghost):
    startTime = time.perf_counter()
    frame = ghost["currentFrame"]
    ghost["currentFrame"] += 1
    try:
        ghost["frames"][frame]
    except:
        ghost["currentFrame"] = -1
        frame = 0
        #countLap(ghost)
    try:
        vtx = ghost['obj']['fpvCamera']['vtx']
        if(ghost['spawnComplete']==False):
            ghost['spawnComplete'] = True
            lap = ghost["obj"]["lap"]
            #we don't want a ghost to be on the same video channel as the player
            vtx.setChannel(lap+1)
            vtx.setPitMode(0)
        else:
            if(frame==1):
                countLap(ghost)
    except:
        pass
    if(ghost["currentFrame"] < 180):
       disableGhostCollision(ghost["obj"])
    else:
        enableGhostCollision(ghost["obj"])

    ghost["obj"].position = ghost["frames"][frame]["pos"]
    ghost["obj"].orientation = ghost["frames"][frame]["ori"]
    #else:
    #    ghost["obj"]["camera"]
    #    #logic.sendMessage("disable shaders")
    #    #ghost["obj"].position = [0,0,-100000]
    endTime = time.perf_counter()
    #print("createGhostData("+str(endTime-startTime))

def countLap(ghost):
    vtx = ghost['obj']['fpvCamera']['vtx']
    vtxFrequency = vtx.getFrequency()
    gatePass = {"channel":vtxFrequency, "time":time.time()}
    clientNetwork = flowState.getNetworkClient()
    if(clientNetwork == None):
        clientID = None
    else:
        clientID = clientNetwork.clientID
    gatePassEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.EVENT_LAP,clientID,gatePass)
    flowState.getRaceState().addTimelineEvent(gatePassEvent,False)

def addGhostQuad():
    actuator = owner.actuators["addGhost"]
    actuator.object = "ghostQuad"
    startTime = time.perf_counter()
    actuator.instantAddObject()
    endTime = time.perf_counter()
    obj = actuator.objectLastCreated
    disableGhostCollision(obj)
    obj.position = [0,0,-100000]
    return obj

def disableGhostCollision(obj):
    startTime = time.perf_counter()
    obj.collisionGroup = 4
    for child in obj.children:
        child.collisionGroup = 4
        for childOfChild in child.children:
            childOfChild.collisionGroup = 4
    endTime = time.perf_counter()
    #print("disableGhostCollision("+str(endTime-startTime))

def enableGhostCollision(obj):
    startTime = time.perf_counter()
    obj.collisionGroup = 1
    for child in obj.children:
        child.collisionGroup = 1
        for childOfChild in child.children:
            childOfChild.collisionGroup = 1
    endTime = time.perf_counter()
    #print("enableGhostCollision("+str(endTime-startTime))

main()
