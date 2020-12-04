import bge.logic as logic
import math
import random
import os
import copy
scene = logic.getCurrentScene()

flowState = logic.flowState
cont = logic.getCurrentController()
own = cont.owner
droneSettings = flowState.getDroneSettings()
timeScale = (droneSettings.timeScale/100.0)
def updateLaps():
    if logic.countingDown:
        own['current_lap'] = 0.00
    logic.currentLap = str(own['lap'])
    logic.lapTimer = own
    if(own['lap'] >0):
        logic.lastLapTime = str(format(own['last_lap']/timeScale, '.2f'))
        logic.bestLapTime = str(format(own['best_lap']/timeScale, '.2f'))
    else:
        logic.lapTimes = []
        logic.currentLap = ""
        logic.lastLapTime = ""
        logic.bestLapTime = ""
    if(own['lap'] == -1):
        logic.holeshotTime = 0.0

    logic.raceTimer = str(format(own['race time']/timeScale, '.2f'))

def addLastLap():
    own['lap']+=1
    cont.actuators['Sound'].startSound()
    #if(own['lap'] != 0):

    if own['lap'] >= 0:
        if own['lap'] > 0:
            own['last_lap'] = copy.deepcopy(own['current_lap'])
        if(logic.finishedLastLap==False):
            logic.lapTimes.append(str(format(own['current_lap']/timeScale, '.2f')))
            if(logic.lapTimer['race time'] > flowState.getTimeLimit()):
                logic.finishedLastLap = True
                logic.flowState.setNotification({'Text':"RACE COMPLETE: "+logic.flowState.getSelectedMap()})

    if(own['lap'] == 0):
        logic.holeshotTime = str(format((own['current_lap']/timeScale), '.2f'))
    own['current_lap'] = 0.00
def setCheckpointVisibilities():
    #for checkpoint in logic.flowState.track['checkpoints']:
    #    if(checkpoint['metadata']['checkpoint order'] == logic.flowState.track['nextCheckpoint']):
    #        checkpoint.visible = True
    #        enableCollision(checkpoint)
    #    else:
    #        checkpoint.visible = False
    #        disableCollision(checkpoint)
    pass

def disableCollision(obj):
    mask = 4
    obj.collisionGroup = mask

def enableCollision(obj):
    mask = 2#bytearray(mask)
    obj.collisionGroup = mask

def main():
    collision = cont.sensors['Collision'].triggered and cont.sensors['Collision'].positive
    if(collision):
        if(logic.flowState.track['nextCheckpoint'] == 0):
            addLastLap()
            logic.flowState.track['nextCheckpoint'] = 1
            #setCheckpointVisibilities()
            own.visible = False
    else:
        if(logic.flowState.track['nextCheckpoint'] == 0):
            if own.visible!=True:
                own.visible = True

    if(own['last_lap']<own['best_lap']):
        own['best_lap'] = copy.deepcopy(own['last_lap'])

    updateLaps()
if hasattr(logic, 'countingDown'):
    main()
