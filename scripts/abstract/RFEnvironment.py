import bge
logic = bge.logic
render = bge.render
#this class keeps track of all the emitters and recievers in our radio frequency environment
class RFEnvironment:
    def __init__(self,flowState):
        flowState.log("RFEnvironment.init()")
        self.emitters = []
        self.receivers = []
        self.currentRXIndex = 0
        self.flowState = flowState

    def printRFState(self):
        rfState = {"receivers":[],"emitters":[]}
        print("current RX index = "+str(self.currentRXIndex))
        for rx in self.receivers:
            item = {"frequency":rx.getFrequency()}
            rfState['receivers'].append(item)
        for em in self.emitters:
            item = {"frequency":em.getFrequency(), "pitMode":em.getPitMode(), "power":em.getPower()}
            rfState['emitters'].append(item)
        print("RF environment = "+str(rfState))

    def addEmitter(self,emitter):
        self.flowState.log("RFEnvironment.addEmitter()")
        self.emitters.append(emitter)

    def removeEmitter(self,emitter):
        self.flowState.log("RFEnvironment.removeEmitter()")
        self.emitters = [value for value in self.emitters if value != emitter] #removes all matching occurances of the rf emitter

    def addReceiver(self,receiver):
        self.flowState.debug("RFEnvironment.addReceiver()")
        self.receivers.append(receiver)

    def removeReceiver(self,receiver):
        self.flowState.log("RFEnvironment.removeReceiver()")
        self.receivers = [value for value in self.receivers if value != receiver] #removes all matching occurances of the rf receiver

    def getReceivers(self):
        return self.receivers

    def getReceiver(self):
        try:
            rx = self.receivers[self.currentRXIndex]
        except:
            rx = None
        return rx

    def getRFPenetration(self): #we need to start using some of this old code again in our RF calculations
        hitList = []

        lastHitPos = own.position
        for interference in range(1,100):
            hit = scene.active_camera.rayCast(own['rxPosition'], lastHitPos, 0.0, "", 0, 0, 0)
            hitPos = hit[1]
            if(hitPos == None):
                hitList.append(own['rxPosition'])
                break
            else:
                if(own.getDistanceTo(hitPos)<2):
                    hitList.append(own['rxPosition'])
                    break
                vScale = 2
                rxVect = getRXVector(vScale,own['rxPosition'])
                hitPos = [hitPos[0]+rxVect[0],hitPos[1]+rxVect[1],hitPos[2]+rxVect[2]]
                hitList.append(hitPos)
            lastHitPos = hitPos
        interference *= .1
        groundBreakup = (12-own.position[2])*0.3
        if(groundBreakup<1):
          groundBreakup = 1
        if(interference<1):
          interference = 1

    def update(self, noiseFloor):
        if(noiseFloor<1):
            noiseFloor = 1
        if(self.receivers!=[]):
            rx = self.receivers[self.currentRXIndex] #let's get the rx the user is viewing
            signalStrength = noiseFloor
            strongestEmitter = None
            strongestSignalStrength = 0
            interference = noiseFloor #we will use this to find out how much of the received signal is intentional or interference
            for vtx in self.emitters:
                try:
                    disonance = ((abs(vtx.getFrequency()-rx.getFrequency())*1)**2)+1 #let's get a number between 1 and ~11 to represent how far detuned our vrx is from our vtx
                    rxPos = rx.object.position
                    rxPos = [rxPos[0],rxPos[1],rxPos[2]+100]
                    distance = vtx.object.getDistanceTo(rxPos)+0.1 #let's get the distance between the vtx and the vrx (but don't let it be 0)
                    pitModePower = (1-vtx.getPitMode())
                    signalStrength = (vtx.getPower()*pitModePower)/((distance/1000)**2)/disonance #let's use the inverse square law to determine the signal strength, then device it by the disonance of the channels.

                    #print("signal strength:"+str(signalStrength)+", disonance: "+str(disonance)+", power: "+str(vtx.power)+", channel: "+str(vtx.channel)+", pit mode: "+str(vtx.pitMode))
                    if(signalStrength>strongestSignalStrength):
                        #let's note the emitter with the strongest signal as well as the value of that siganl strength
                        strongestEmitter = vtx
                        strongestSignalStrength = signalStrength
                        vtx.signalStrength = signalStrength

                    interference += signalStrength
                except:
                    self.flowState.error("failed to calculate vtx signal")
                    self.emitters.remove(vtx)
                    break
            pstr = ""
            for vtx in self.receivers:
                #pr = "(power = "+str(vtx.getPower())
                fr = "(frequency = "+str(vtx.getFrequency())+"), "
                #pstr+= pr
                pstr+=fr

            #print(pstr)
            if(strongestEmitter!=None):
                interference -= strongestSignalStrength #we don't want to count the current image as interference
                if(interference<=0):
                    interference = 0.1
                #print(strongestSignalStrength)
                snr = strongestSignalStrength/interference
                if snr <= 0: #don't let snr = 0
                    snr = 0.1
                rx.snr = snr
                self.setCamera(strongestEmitter.object)
                render.drawLine(rx.object.position,vtx.object.position,[1,1,1])
                #self.flowState.log("emitters: "+str(self.emitters))
            else: #there are no RF emitters
                rx.snr = 0.1
                #print("no RF emitters!!!")
    def getCurrentVRX(self):
        vrx = None
        if(self.receivers!=[]):
            vrx = self.receivers[self.currentRXIndex]
        return vrx

    def setCamera(self,newCamera):
        scene = logic.getCurrentScene()
        activeCamera = scene.active_camera
        if(activeCamera!=newCamera):
            self.flowState.debug("switching to camera "+str(newCamera))
            scene.active_camera = newCamera
