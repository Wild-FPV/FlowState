# Python program to implement client side of chat room.
import FSNClient
import FSNObjects
import socket
import bge
import math
import time
from uuid import getnode as get_mac
import random
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
    newObj.suspendDynamics(True)
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
    messageType = message[FSNObjects.MESSAGE_TYPE_KEY]
    #   ("message handler called! "+str(messageType))

    #server event
    if messageType == FSNObjects.SERVER_EVENT_TYPE_KEY:
        #print("handling server event")
        #print("message = "+str(message))
        message = FSNObjects.ServerEvent.getMessage(message)
        if(message.eventType == FSNObjects.ServerEvent.PLAYER_JOINED):
            #print("- player join event")
            addNewPlayer(message.senderID)
        if(message.eventType == FSNObjects.ServerEvent.ACK):
            flowState.getNetworkClient().serverReady = True
        if(message.eventType == FSNObjects.ServerEvent.MAP_SET):
            print("we should load a map!")
            mapData = message.extra
            mapLoad.spawnMapElements(mapData)
            print("map load complete!")

    #player state
    if messageType == FSNObjects.PLAYER_STATE:
        #print("handling player state")
        #print("message = "+str(message))
        message = FSNObjects.PlayerState.getMessage(message)
        if(message.senderID in logic.peers):
            peerObject = logic.peers[message.senderID]
            peerObject.position = message.position
            peerObject.orientation = message.orientation
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

    #player event
    if messageType == FSNObjects.PLAYER_EVENT:
        print("handling player event")
        print("message = "+str(message))
        message = FSNObjects.PlayerEvent.getMessage(message)
        if(message.eventType == FSNObjects.PlayerEvent.PLAYER_JOINED):
            #print("- player join event")
            addNewPlayer(message.senderID)
        if(message.eventType == FSNObjects.PlayerEvent.PLAYER_QUIT):
            removePlayer(message.senderID)
        if(message.eventType == FSNObjects.PlayerEvent.PLAYER_MESSAGE):
            messageBody = None
            MessageTo = None
            MessageFrom = None
            sendMessage(message.extra,messageBody,MessageTo,MessageFrom)

    #server state
    if messageType == FSNObjects.SERVER_STATE:
        print("handling server state")
        print("message = "+str(message))
        message = FSNObjects.ServerState.getMessage(message)

        gameMode = message.gameMode
        print("game mode = "+str(gameMode))
        if(gameMode == FSNObjects.MULTIPLAYER_MODE_1V1):
            flowState.log("server setting game mode to 1v1")
            flowState.setGameMode(flowState.GAME_MODE_MULTIPLAYER)
        if(gameMode == FSNObjects.MULTIPLAYER_MODE_TEAM):
            flowState.log("server setting game mode to team race")
            flowState.setGameMode(flowState.GAME_MODE_TEAM_RACE)
            flowState.setTimeLimit(600)

        #handle the states of our peers
        peerStates = message.playerStates
        for key in peerStates:
            if(key==flowState.getNetworkClient().clientID):
                pass
            else:
                peerState = peerStates[key]
                #print(peerStates)
                message = FSNObjects.PlayerState.getMessage(peerState)
                newObj = scene.addObject("playerQuad",logic.player,0)
                print("ADDING NEW PLAYER OBJECT!!!!!")
                logic.peers[key] = newObj #lets add this new player model to a dict so we can reference it later
                #print(logic.peers)
                peerObject = logic.peers[key]
                peerObject.position = message.position
                peerObject.orientation = message.orientation


def setup():
    flowState.log("FSNetwork: joining server: "+str(flowState.getServerIP())+":"+str(flowState.getServerPort()))
    #
    flowState.setNetworkClient(FSNClient.FSNClient(flowState.getServerIP(),flowState.getServerPort()))
    flowState.getNetworkClient().connect()
    playerJoinEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_JOINED,flowState.getNetworkClient().clientID)
    flowState.getNetworkClient().sendEvent(playerJoinEvent)
    flowState.getNetworkClient().setMessageHandler(clientMessageHandler)
    logic.peers = {}

def run():
    position = list(logic.player.position)
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
    myState = FSNObjects.PlayerState(flowState.getNetworkClient().clientID,None,position,orientation,color,frequency,power)

    flowState.getNetworkClient().updateState(myState)
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
