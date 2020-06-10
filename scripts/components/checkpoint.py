import bge
from collections import OrderedDict


if not hasattr(bge, "__component__"):
    import time
    import numpy as np
    import math as m
    import copy
    import aud
    from scripts.abstract.RaceState import RaceState
    import FSNObjects

    render = bge.render
    logic = bge.logic
    flowState = logic.flowState


class Checkpoint(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("checkpoint number", 1),
        ("Lap Timer", False)
    ])

    def oncollision(self, obj, point, normal, points):
        if(obj==logic.flowState.getPlayer().object):
            self.collision = obj
        #for point in points:
        #    print(point.localPointA)
        #    print(point.localPointB)
        #    print(point.worldPoint)
        #    print(point.normal)
        #    print(point.combinedFriction)
        #    print(point.combinedRestitution)
        #    print(point.appliedImpulse)
    def drawPoint(self,point):
        render.drawLine([point[0]-1,point[1],point[2]],[point[0]+1,point[1],point[2]],[1,0,0])
        render.drawLine([point[0],point[1]-1,point[2]],[point[0],point[1]+1,point[2]],[0,1,0])
        render.drawLine([point[0],point[1],point[2]-1],[point[0],point[1],point[2]+1],[1,0,1])

    def drawTraces(self):
        if len(self.flightData['position'])>=2:
            for i in range(0,len(self.flightData['position'])-1):
                position = self.flightData['position'][i]
                a = self.flightData['position'][i]
                b = self.flightData['position'][i+1]
                value = self.flightData['throttlePercent'][i]
                render.drawLine(a,b,[1,1-value,1-value])
                #self.drawPoint(a)
            #self.drawPoint(b)


    def start(self, args):
        self.lastPlayerPos = None
        self.entrance = None
        self.object["checkpoint"] = True
        self.object['isLapTimer'] = args['Lap Timer']
        self.collision = None
        self.object.collisionCallbacks = [self.oncollision]
        self.flightData = {"position":[],"throttlePercent":[]}
        self.timeline = {}

        #print(self.object.collisionCallbacks)
        #print("start "+str(self.object.name))

    def markLapEvent(self):
        flowState.debug("markLapEvent()")
        quadCamera = logic.flowState.getPlayer().object['quadCamera']
        vtx = quadCamera['vtx']
        vtxFrequency =vtx.getFrequency()
        gatePass = {"channel":vtxFrequency, "time":time.time()}
        clientNetwork = flowState.getNetworkClient()
        if(clientNetwork == None):
            clientID = None
        else:
            clientID = clientNetwork.clientID
        if(flowState.getRaceState().holeshotComplete):
            eventType = FSNObjects.PlayerEvent.EVENT_LAP
        else:
            eventType = FSNObjects.PlayerEvent.EVENT_HOLE_SHOT
        gatePassEvent = FSNObjects.PlayerEvent(eventType,clientID,gatePass)
        flowState.getRaceState().addTimelineEvent(gatePassEvent)

    def markCheckpointCollectionEvent(self):
        quadCamera = logic.flowState.getPlayer().object['quadCamera']
        vtx = quadCamera['vtx']
        vtxFrequency =vtx.getFrequency()
        gatePass = {"channel":vtxFrequency, "time":time.time()}
        clientNetwork = flowState.getNetworkClient()
        if(clientNetwork == None):
            clientID = None
        else:
            clientID = clientNetwork.clientID
        gatePassEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.EVENT_CHECKPOINT_COLLECT,clientID,gatePass)
        flowState.getRaceState().addTimelineEvent(gatePassEvent)


    def getEntryAngle(self, v1, v2, acute):
        angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        return angle

    def setCheckpointVisibility(self,enabled=False):
        if self.object.visible!=enabled:
            self.object.visible = enabled
            if(enabled):
                flowState.debug("checkpoint:"+str(self.object['metadata']['checkpoint order'])+" activated")
                self.enableCollision(self.object)
                self.flightData = {"position":[],"throttlePercent":[]}
            else:
                flowState.debug("checkpoint:"+str(self.object['metadata']['checkpoint order'])+" deactivated")
                self.disableCollision(self.object)

    def disableCollision(self,obj):
        mask = 4
        obj.collisionGroup = mask

    def enableCollision(self,obj):
        mask = 2#bytearray(mask)
        obj.collisionGroup = mask

    def playSound(self):
        sound = aud.Factory.file(bge.logic.expandPath('//sounds/checkpoint.wav'))
        scene = bge.logic.getCurrentScene()

        sound_device = aud.device()
        sound_device.distance_model = aud.AUD_DISTANCE_MODEL_LINEAR
        sound_device.listener_location = logic.player.worldPosition
        sound_device.listener_velocity = logic.player.getLinearVelocity(True)
        sound_device.volume = 0.5
        sound_handle = sound_device.play(sound)
        #sound_handle.volume = 0.5
        sound_handle.relative = False
        sound_handle.location = self.object.worldPosition
        sound_handle.velocity = self.object.getLinearVelocity()
        sound_handle.distance_maximum = 100
        sound_handle.distance_reference = 1

    def getNormalVect(self, vect):
        max = 0
        for i in vect:
            if abs(i) > max:
                max = i
        normal = []
        for i in range(0,len(vect)):
            normal.append(vect[i]/max)
        return normal
    def update(self):
        self.entrance = self.object.children[0]
        nextCheckpoint = logic.flowState.getRaceState().getNextCheckpoint()
        hitCheckpointNumber = self.object['metadata']['checkpoint order']
        if(flowState.getGameMode()!=flowState.GAME_MODE_EDITOR):
            playerChannel = flowState.getRFEnvironment().getCurrentVRX().getFrequency()
            playerFinishedRacing = flowState.getRaceState().channelHasFinished(playerChannel)
            if(nextCheckpoint==hitCheckpointNumber) and (playerFinishedRacing is False):

                self.setCheckpointVisibility(True)
                if self.lastPlayerPos!=None:
                    pa = self.lastPlayerPos
                    pb = flowState.getPlayer().object.position
                    cm = 2
                    ray = flowState.getPlayer().object.rayCast(objto=pb, objfrom=pa, dist=0, prop="checkpoint", face=False, xray=True, poly=0,mask=cm)
                    hitObject, hitPoint, hitNormal = ray
                    #colHitObject, colPoint, colNormal, colPoints = self.collision
                    #render.drawLine(pa,pb,[0,0,0,1])
                    self.object['checked'] = True
                    if(hitObject==self.object or ((self.collision!=None) and (self.collision==logic.flowState.getPlayer().object))):
                        if(self.collision!=None):
                            flowState.debug("checkpoint:"+str(self.object['metadata']['checkpoint order'])+" collision"+ str(self.collision))
                        else:
                            flowState.debug("checkpoint:"+str(self.object['metadata']['checkpoint order'])+" ray hit"+ str(hitObject))

                        o = self.object.getVectTo(self.entrance.position)[1]
                        #print(o)
                        v = flowState.getPlayer().object.getLinearVelocity(False)

                        difAngle = m.degrees(self.getEntryAngle(v,o,True))
                        if(difAngle>90):
                            self.lastPlayerPos = copy.deepcopy(flowState.getPlayer().object.position)
                            #if logic.flowState.track['lastCheckpoint']==hitCheckpointNumber:
                            #    logic.flowState.track['nextCheckpoint'] = 1
                            #else:
                            #    logic.flowState.track['nextCheckpoint']+=1
                            flowState.getRaceState().incrementCheckpoint()
                            startTime = time.perf_counter()
                            self.playSound()
                            endTime = time.perf_counter()
                            flowState.debug("checkpoint:"+str(hitCheckpointNumber)+" collected")
                            self.markCheckpointCollectionEvent()
                            if('lap timer' in self.object['metadata']):
                                if(self.object['metadata']['lap timer']):
                                    self.markLapEvent()
                        else:
                            flowState.debug("checkpoint:"+str(hitCheckpointNumber)+" angle ("+str(difAngle)+") exceeds 90 "+str(hitCheckpointNumber))
                            #print(difAngle)
            else:
                self.setCheckpointVisibility(False)
                if(flowState.getGraphicsSettings().raceLine):
                    self.drawTraces()
            if self.lastPlayerPos==None:
                self.lastPlayerPos = copy.deepcopy(flowState.getPlayer().object.position)
            if(flowState.getPlayer().object.getDistanceTo(self.lastPlayerPos) > 1):
                self.lastPlayerPos = copy.deepcopy(flowState.getPlayer().object.position)
                if(nextCheckpoint==hitCheckpointNumber):
                    self.flightData['position'].append(copy.deepcopy(flowState.getPlayer().object.position))
                    self.flightData['throttlePercent'].append(logic.throttlePercent)
        self.collision = None
