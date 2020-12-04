import bge.logic as logic
import math
import random
import os
import time
cont = logic.getCurrentController()
own = cont.owner
flowState = logic.flowState

currentVRX = flowState.getRFEnvironment().getCurrentVRX()
if(currentVRX!=None):
    playerRXFrequency = currentVRX.getFrequency()
else:

    playerRXFrequency = 1
errorLog = logic.getCurrentScene().objects['HUDError']
rxChannel = logic.getCurrentScene().objects['HUDRXChannel']
laps = logic.getCurrentScene().objects['HUDLapCount']
lastLap = logic.getCurrentScene().objects['HUDLastLap']
bestLap = logic.getCurrentScene().objects['HUDBestLap']
times = logic.getCurrentScene().objects['HUDLapTimes']
holeshot = logic.getCurrentScene().objects['HUDHoleshot']
countdown = logic.getCurrentScene().objects['HUDCountdown']
gForceCounter = logic.getCurrentScene().objects['HUDgForceCounter']
aspectRatioCropper = logic.getCurrentScene().objects['aspectRatioCropper']
#logic.flowState.setNotification(logic.getCurrentScene().objects['HUDNotification'])
logic.getCurrentScene().objects['HUDNotification']['Text'] = flowState.getNotification()['Text']

try:
    #let's try to display the channel the user is on
    ping = ""
    if(flowState.getGameMode()==flowState.GAME_MODE_MULTIPLAYER):
        if(flowState.getNetworkClient().ping>1000):
            ping = ", network connection poor"
        else:
            ping = ", ping: "+str(int(flowState.getNetworkClient().ping))+"ms"
    camera = logic.player['camera']
    vtx = camera['vtx']
    rxChannel['Text'] = "VTX Channel: "+str(vtx.getChannel()+1)+ping
except Exception as e:
    pass
    #flowState.error(e)
graphicsSettings = flowState.getGraphicsSettings()
aspectRatioIs43 = graphicsSettings.aspectRatioIs4x3()
if(aspectRatioIs43):
    aspectRatioCropper.visible = True
else:
    aspectRatioCropper.visible = False
try:
    gForceCounter['Text'] = str(round(logic.gForce, 1))+"G"
except:
    pass

def formatLapTime(lapTime):
    result = ""
    try:
        result = str(format(lapTime, '.2f'))
    except:
        pass
    return result

pilotTagStr = ""

pilotTagStr = str(flowState.getRFEnvironment().getCurrentVTX().getPilotTag())

lastLapStr = formatLapTime(flowState.getRaceState().getChannelLastLapTime(playerRXFrequency))
bestLapStr = formatLapTime(flowState.getRaceState().getChannelBestLapTime(playerRXFrequency))
holeshotStr = formatLapTime(flowState.getRaceState().getChannelHoleShot(playerRXFrequency))

laps['Text'] = pilotTagStr
lastLap['Text'] = "LAST LAP: "+lastLapStr
bestLap['Text'] = "BEST LAP: "+bestLapStr
holeshot['Text'] = ""#HOLESHOT: "+holeshotStr
#errorLog['Text'] = "Error: "+logic.errorLog

#flowState.debug("currentCheckpoint = "+str(flowState.getRaceState().currentCheckpoint))
#flowState.debug("lastCheckpoint = "+str(flowState.track.getLastCheckpoint()))
if flowState.getRaceState().raceStartTime > time.time(): #race starts in the future
    countdown['Text'] = int(flowState.getRaceState().raceStartTime-time.time())+1
else:
    if flowState.getRaceState().raceStartTime+0.5 > time.time(): #we are less than one second into the race
        countdown['Text'] = "GO"
    else:
        countdown['Text'] = ""

#let's show the user how well they did
raceCompletionText = ""
lapsCompletedText = flowState.getRaceState().getChannelLapCount(playerRXFrequency)
if flowState.getRaceState().raceCompleted():
    raceCompletionText += "RACE COMPLETE: "
    if(flowState.getGameMode()==flowState.GAME_MODE_SINGLE_PLAYER):
        raceCompletionText += flowState.getSelectedMapName()
    else:
        raceCompletionText += "press space to restart"
    raceCompletionText += "\n"
    fastX = flowState.getRaceState().getRaceFormat().consecutiveLapCount
    fastXCon = flowState.getRaceState().getChannelFastestConcecutiveTime(playerRXFrequency,fastX)
    raceCompletionText += "fast "+str(fastX)+" consecutive laps: "+formatLapTime(fastXCon)
    raceCompletionText += "\n"
    raceCompletionText += "laps: "+str(lapsCompletedText)
    raceCompletionText += "\n"
    timeCompletedText = flowState.getRaceState().getChannelRaceCompletionTime(playerRXFrequency)
    raceCompletionText += "time: "+formatLapTime(timeCompletedText)
    raceCompletionText += "\n"
try:
    raceCompletionText += "Rank: "+str(flowState.getRaceState().getPlayerRanks().index(playerRXFrequency)+1)
except:
    pass

flowState.setNotification({"Text":raceCompletionText})
logic.flowState.track['nextCheckpoint'] = -1



timesText = "TIME: "+formatLapTime(flowState.getRaceState().getRaceTime())
timesText+="\nLAPS: "+str(lapsCompletedText)
#lapTimes = flowState.getRaceState().getChannelLapTimes(playerRXFrequency)
#for i in range(0,len(lapTimes)):
#    timesText+='\n'
#    timesText+="LAP "+str(i+1)+": "+formatLapTime(lapTimes[i])

times['Text'] = timesText

#disables the OSD if it's turned off in the settings
if(flowState.getGraphicsSettings().OSDEnabled==False):
    times['Text'] = ""
    laps['Text'] = ""
    lastLap['Text'] = ""
    bestLap['Text'] = ""
    holeshot['Text'] = ""
    rxChannel['Text'] = ""
    gForceCounter['Text'] = ""
    flowState.setNotification({"Text":""})
