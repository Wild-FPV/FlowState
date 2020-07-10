# Python program to implement client side of chat room.
import FSNClient
import FSNObjects
import socket
import pickle
import bge
import math
import time
from uuid import getnode as get_mac
import random
from scripts.abstract.RaceFormat import RaceFormat
logic = bge.logic
scene = logic.getCurrentScene()
flowState = logic.flowState
import mapLoad
def quitGame():
    print("exiting game")
    try:
        flowState.getNetworkClient().quit()
    except:
        pass
    scenes = logic.getSceneList()
    currentScene = logic.getCurrentScene()
    for scene in scenes:
        if(scene!=currentScene):
            scene.end()
    flowState.resetGameState()
    flowState.setViewMode(flowState.VIEW_MODE_MENU)
    currentScene.replace("Menu Background")

def addNewPlayer(playerID):
    print("addNewPlayer("+str(playerID)+")")
    newObj = scene.addObject("playerQuad",logic.player,0)
    newObj.position = [0,0,-100]
    #newObj.suspendDynamics(True)
    logic.peers[playerID] = newObj #lets add this new player model to a dict so we can reference it later

def removePlayer(playerID):
    try:
        print("removePlayer("+str(playerID)+")")
        logic.peers[playerID].endObject()
        del logic.peers[playerID]
    except:
        print("failed to remove player: "+str(playerID))

def sendMessage(subject,body,to,messageFrom):
    print("sending game message from server")
    logic.sendMessage(subject)

def clientMessageHandler(message):
    if(FSNObjects.MESSAGE_TYPE_KEY in message):

        messageType = message[FSNObjects.MESSAGE_TYPE_KEY]
        #   ("message handler called! "+str(messageType))

        #server event
        if messageType == FSNObjects.SERVER_EVENT_TYPE_KEY:
            #print("- handling server event")
            message = FSNObjects.ServerEvent.getMessage(message)
            if(message.eventType == FSNObjects.ServerEvent.PLAYER_JOINED):
                print("  - player join event")
                addNewPlayer(message.senderID)
            if(message.eventType == FSNObjects.ServerEvent.ACK):
                #print("  - server ack")
                flowState.getNetworkClient().serverReady = True
                flowState.getNetworkClient().updatePing()
            if(message.eventType == FSNObjects.ServerEvent.MAP_SET):
                print("  - we should load a map!")
                mapData = message.extra
                mapLoad.spawnMapElements(mapData)
                print("map load complete!")
            if(message.eventType == FSNObjects.ServerEvent.FORMAT_SET):
                print("  - we should set the race format!")
                raceFormatDict = message.extra
                formatPriority = raceFormatDict['raceFormatPriority']
                raceFormat = RaceFormat(formatPriority,raceFormatDict['timeLimit'],raceFormatDict['lapLimit'],raceFormatDict['consecutiveLapCount'])
                flowState.getRaceState().setRaceFormat(raceFormat)
                print("map load complete!")
            if(message.eventType == FSNObjects.ServerEvent.SET_VTX_CHANNEL):
                print("  - we should set our VTX channel")
                print(message.extra)
                vtx = flowState.setInitialVTXChannel(message.extra)
                logic.player['camera']['vtx'].setChannel(flowState.getInitialVTXChannel())
                flowState.getRFEnvironment().getCurrentVRX().setChannel(flowState.getInitialVTXChannel())

        #player state
        if messageType == FSNObjects.PLAYER_STATE:
            #print("- handling server player state")
            message = FSNObjects.PlayerState.getMessage(message)
            #print(message)
            if(message.senderID in logic.peers):
                peerObject = logic.peers[message.senderID]
                peerObject.position = message.position
                peerObject.orientation = message.orientation
                #peerObject.setLinearVelocity(message.velocity,True)
                #peerObject.setAngularVelocity(message.angularVelocity,True)
                peerObject['state'] = message
                try:
                    vtx = logic.player['camera']['vtx']
                    frequency = vtx.getFrequency()
                    power = vtx.getPower()*(1-vtx.getPitMode())
                    #print("player frequency = "+str(frequency))
                except:
                    pass
                if("fpvCamera" in peerObject):
                    camera = peerObject['fpvCamera']
                    if("vtx" in camera):
                        vtx = camera['vtx']
                        vtx.setPower(message.vtxPower)
                        vtx.setFrequency(message.vtxFrequency)
                        vtx.setPitMode(0)
                        vtx.setPilotTag(message.playerName)

        #player event
        if messageType == FSNObjects.PLAYER_EVENT:
            print("- handling player event")
            message = FSNObjects.PlayerEvent.getMessage(message)
            print(message)
            if(message.eventType == FSNObjects.PlayerEvent.PLAYER_JOINED):
                print("- player join event")
                print(message)
                addNewPlayer(message.senderID)
            if(message.eventType == FSNObjects.PlayerEvent.PLAYER_QUIT):
                print("  - player quit event")
                removePlayer(message.senderID)

            #player is sending some race state update
            if(message.eventType == FSNObjects.PlayerEvent.EVENT_HOLE_SHOT):
                #print("- player holeshot event")
                flowState.getRaceState().addTimelineEvent(message, False)
            if(message.eventType == FSNObjects.PlayerEvent.EVENT_LAP):
                #print("- player lap event")
                flowState.getRaceState().addTimelineEvent(message, False)
            if(message.eventType == FSNObjects.PlayerEvent.EVENT_CHECKPOINT_COLLECT):
                #print("- player checkpoint event")
                flowState.getRaceState().addTimelineEvent(message, False)
            if(message.eventType == FSNObjects.PlayerEvent.EVENT_RACE_FINISH):
                #print("- player race finish event")
                flowState.getRaceState().addTimelineEvent(message, False)

            #player sent a message which should be broadcast as a generic game engine message
            if(message.eventType == FSNObjects.PlayerEvent.PLAYER_MESSAGE):
                print("  - player game engine message event")
                messageBody = None
                MessageTo = None
                MessageFrom = None
                sendMessage(message.extra,messageBody,MessageTo,MessageFrom)

            #A player is resetting the race and has sent a time at which the race should begin
            if(message.eventType == FSNObjects.PlayerEvent.PLAYER_RESET):
                print("  - player reset event")
                message.extra = message.extra
                messageSubject = 'reset'
                startTime = message.extra[messageSubject]
                messageBody = startTime
                MessageTo = None
                MessageFrom = None
                flowState._countdownTime = startTime-time.time()
                print("current time is "+str(time.time()))
                print("message time is "+str(startTime))
                print("diff - "+str(startTime-time.time()))
                sendMessage(messageSubject,messageBody,MessageTo,MessageFrom)

        #server state
        if messageType == FSNObjects.SERVER_STATE:
            print("handling server state")
            message = FSNObjects.ServerState.getMessage(message)
            print(message)
            gameMode = message.gameMode
            #if(gameMode == FSNObjects.MULTIPLAYER_MODE_1V1):
            #    flowState.log("server setting game mode to 1v1")
            #    flowState.setGameMode(flowState.GAME_MODE_MULTIPLAYER)
            #if(gameMode == FSNObjects.MULTIPLAYER_MODE_TEAM):
            #    flowState.log("server setting game mode to team race")
            #    flowState.setGameMode(flowState.GAME_MODE_TEAM_RACE)
            #    flowState.setTimeLimit(600)

            #handle the states of our peers
            peerStates = message.playerStates
            for key in peerStates:
                if(key==flowState.getNetworkClient().clientID):
                    pass
                else:
                    newObj = scene.addObject("playerQuad",logic.player,0)
                    logic.peers[key] = newObj #lets add this new player model to a dict so we can reference it later
                    #print(logic.peers)


                    peerState = peerStates[key]
                    message = FSNObjects.PlayerState.getMessage(peerState)
                    peerObject = logic.peers[key]
                    peerObject.position = message.position
                    peerObject.orientation = message.orientation
                    #peerObject.setLinearVelocity(message.velocity,True)
                    #peerObject.setAngularVelocity(message.angularVelocity,True)
                    peerObject['state'] = peerState
    else:
        print("WARNING: invalid message!!! "+str(message))

def interpolate(posA,posB,damp):
    return [(posA[0]*damp)+(posB[0]*(1-damp)),(posA[1]*damp)+(posB[1]*(1-damp)),(posA[2]*damp)+(posB[2]*(1-damp))]

def rotate2D(point, angle):
    origin = (0,0)
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def interpolateOrientation(vecA,vecB,damp,obj=None):

    x = math.cos(vecB[1])*math.cos(vecB[0])
    y = math.sin(vecB[1])*math.cos(vecB[0])
    z = math.sin(vecB[0])
    print([x,y,z])
    origin = obj.position
    result = [origin[0]+(x*10),origin[1]+(y*10),origin[2]+(z*10)]
    bge.render.drawLine(origin,result,[1,1,1,1])
    #for axis in range(0,len(vecA)):
    #    angleA = vecA[axis]
    #    angleB = vecB[axis]
        #oA = math.sin(angleA)
        #aA = math.cos(angleA)

        #oB = math.sin(angleB)
        #aB = math.cos(angleB)

        #oC = (oB*damp)+(oA*(1-damp))
        #aC = (aB*damp)+(aA*(1-damp))

        #degreesToRotate = (angleA-angleB)*damp
        #oC, aC = rotate2D((oC,aC),degreesToRotate)
        #newAngle = math.atan2(oC,aC)
        #if(newAngle>math.pi):
        #    newAngle = newAngle % math.pi

        #if(newAngle<-math.pi):
        #     newAngle = newAngle % math.pi
        #if(newAngle>)
        #result.append(newAngle)

        #rotation goes from -pi to pi
        #if(abs(valueA-valueB)>math.pi): #the start and end like on opposite sides of the maximum rotation value
        #    if(valueB > valueA):#let's find the accute angle
        #        valueA += math.pi*2
        #    else:
        #        valueB += math.pi*2
        #value = (valueB*damp)+(valueA*(1-damp))

        #if(value > math.pi):

            #value = -math.pi+(value % math.pi)
        #    print("value too large!!! " +str(value))
        #if(value < -math.pi):

            #value = value % math.pi
        #    print("value too small!!! " +str(value))
        #result.append(value)
    #print(result)
    return result


#this method continues moving the players based on their last known velocities. It is a good place for any other predictive code
def enterpolatePlayerObjects():
    interpolation = True
    for key in logic.peers:
        try:
            playerObj = logic.peers[key]
            if "state" in playerObj:
                state = playerObj['state']
                if(interpolation):
                    damp = 0.75
                    #interpLinearVelocity = interpolate(state.velocity,playerObj.getLinearVelocity(True),0.1)#[(lv[0]*damp)+(olv[0]*(1-damp)),(lv[1]*damp)+(olv[1]*(1-damp)),(lv[2]*damp)+(olv[2]*(1-damp))]
                    #interpAngularVelocity = interpolate(state.angularVelocity,playerObj.getAngularVelocity(True),0.1)#[(av[0]*damp)+(oav[0]*(1-damp)),(av[1]*damp)+(oav[1]*(1-damp)),(av[2]*damp)+(oav[2]*(1-damp))]
                    interpLinearVelocity = interpolate([0,0,0],state.velocity,0.9)#[(lv[0]*damp)+(olv[0]*(1-damp)),(lv[1]*damp)+(olv[1]*(1-damp)),(lv[2]*damp)+(olv[2]*(1-damp))]
                    interpAngularVelocity = interpolate([0,0,0],state.angularVelocity,0.9)
                    interpPosition = interpolate(state.position,playerObj.position,damp)
                    #o = playerObj.orientation.to_euler()
                    #orientation = [o[0],o[1],o[2]]
                    #interpOrientation = interpolateOrientation(orientation,state.orientation,0.1,playerObj)

                    playerObj.setLinearVelocity(interpLinearVelocity,True)
                    playerObj.setAngularVelocity(interpAngularVelocity,True)
                    #playerObj.position = interpPosition
                    #playerObj.orientation = interpOrientation
                    #playerObj.orientation = state.orientation
                    #print(orientation)
                else:
                    #playerObj.setLinearVelocity(interpLinearVelocity,True)
                    #playerObj.setAngularVelocity(interpAngularVelocity,True)
                    playerObj.position = state.position
                    playerObj.orientation = state.orientation
        except Exception as e:
            print("failed to predict peer positions")
            print(e)

def setup():
    flowState.log("FSNetwork: joining server: "+str(flowState.getServerIP())+":"+str(flowState.getServerPort()))
    #
    flowState.setNetworkClient(FSNClient.FSNClient(flowState.getServerIP(),flowState.getServerPort()))
    flowState.getNetworkClient().connect()
    playerJoinEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_JOINED,flowState.getNetworkClient().clientID,{"playerName":flowState.getPlayerName()})
    flowState.getNetworkClient().sendEvent(playerJoinEvent)
    flowState.getNetworkClient().setMessageHandler(clientMessageHandler)
    logic.peers = {}

def run():
    position = list(logic.player.position)
    velocity = list(logic.player.getLinearVelocity(True))
    angularVelocity = list(logic.player.getAngularVelocity(True))
    o = logic.player.orientation.to_euler()
    orientation = [o[0],o[1],o[2]]
    color = [0,0,1]
    try:
        vtx = logic.player['camera']['vtx']
        frequency = vtx.getFrequency()
        power = vtx.getPower()*(1-vtx.getPitMode())
    except:
        power = 0
        frequency = 0
    playerName = flowState.getPlayerName()
    myState = FSNObjects.PlayerState(flowState.getNetworkClient().clientID,time.time(),position,orientation,velocity,angularVelocity,color,frequency,power,playerName)

    flowState.getNetworkClient().updateState(myState)
    enterpolatePlayerObjects()
    flowState.getNetworkClient().run()


def main():
    #if hasattr(logic, 'isSettled'):
    try:
        logic.lastNetworkTick
    except:
        logic.lastNetworkTick = 0
    try:
        logic.lastLogicTic
    except:
        logic.lastLogicTic = float(time.perf_counter())
    if flowState.getNetworkClient()!=None:
        #if(logic.lastNetworkTick>=0.1):
        #if(logic.lastNetworkTick>=0.01):
        if flowState.getNetworkClient().isConnected():
            run()
            logic.lastNetworkTick = 0
        else:
            quitGame()

    else:
        setup()
        logic.lastNetworkTick = 0
    lastFrameExecution = float(time.perf_counter())-logic.lastLogicTic
    logic.lastNetworkTick+=lastFrameExecution

if(flowState.getGameMode()==flowState.GAME_MODE_MULTIPLAYER) or (flowState.getGameMode()==flowState.GAME_MODE_TEAM_RACE):
    main()
