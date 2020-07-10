import bge.logic as logic
import math
import random
import os
import time
cont = logic.getCurrentController()
own = cont.owner
flowState = logic.flowState

playerRXFrequency = flowState.getRFEnvironment().getCurrentVRX().getFrequency()

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
        ping = ", ping: "+str(int(flowState.getNetworkClient().ping))+"ms"
    camera = logic.player['camera']
    vtx = camera['vtx']
    rxChannel['Text'] = "VTX Channel: "+str(vtx.getChannel()+1)+ping
except Exception as e:
    flowState.error(e)
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

lapsStr = str(flowState.getRaceState().getChannelLapCount(playerRXFrequency))
lastLapStr = formatLapTime(flowState.getRaceState().getChannelLastLapTime(playerRXFrequency))
bestLapStr = formatLapTime(flowState.getRaceState().getChannelBestLapTime(playerRXFrequency))
holeshotStr = formatLapTime(flowState.getRaceState().getChannelHoleShot(playerRXFrequency))

laps['Text'] = "LAPS: "+lapsStr
lastLap['Text'] = "LAST LAP: "+lastLapStr
bestLap['Text'] = "BEST LAP: "+bestLapStr
holeshot['Text'] = "HOLESHOT: "+holeshotStr
errorLog['Text'] = "Error: "+logic.errorLog

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
if flowState.getRaceState().raceCompleted():
    raceCompletionText += "RACE COMPLETE: "
    raceCompletionText += flowState.getSelectedMapName()
raceCompletionText += "\n"
fastX = flowState.getRaceState().getRaceFormat().consecutiveLapCount
fastXCon = flowState.getRaceState().getChannelFastestConcecutiveTime(playerRXFrequency,fastX)
raceCompletionText += "fast "+str(fastX)+" consecutive laps: "+formatLapTime(fastXCon)
raceCompletionText += "\n"
lapsCompletedText = flowState.getRaceState().getChannelLapCount(playerRXFrequency)
raceCompletionText += "laps: "+str(lapsCompletedText)
raceCompletionText += "\n"
timeCompletedText = flowState.getRaceState().getChannelRaceCompletionTime(playerRXFrequency)
raceCompletionText += "time: "+formatLapTime(timeCompletedText)
raceCompletionText += "\n"
raceCompletionText += "Rank: "+str(flowState.getRaceState().getPlayerRanks().index(playerRXFrequency)+1)

flowState.setNotification({"Text":raceCompletionText})
logic.flowState.track['nextCheckpoint'] = -1



timesText = "TIME: "+formatLapTime(flowState.getRaceState().getRaceTime())
lapTimes = flowState.getRaceState().getChannelLapTimes(playerRXFrequency)
for i in range(0,len(lapTimes)):
    timesText+='\n'
    timesText+="LAP "+str(i+1)+": "+formatLapTime(lapTimes[i])

times['Text'] = timesText
