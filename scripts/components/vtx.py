import bge
import copy
import time
from collections import OrderedDict

raceband = [5658,5695,5732,5769,5806,5843,5880,5917]
((abs(5658-5917))/25)+1
if not hasattr(bge, "__component__"):
    render = bge.render
    logic = bge.logic
    try:
        flowState = logic.flowState
    except Exception as e:
        print("VTX: "+str(e))
        from scripts.abstract.FlowState import FlowState
        logic.flowState = FlowState()
        flowState = logic.flowState

class VTX(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Power Output (mw)", 25),
        ("Pit Mode",False),
        ("Frequency", raceband[0]),
        ("Pilot Tag", "")
    ])

    def start(self, args):
        flowState.debug("vtx: start("+str(args)+")")
        self.power = args['Power Output (mw)']
        self.pitMode = int(args['Pit Mode'] == True)
        self.frequency = args['Frequency']
        self.signalStrength = 0
        self.object['vtx'] = self
        self.spectating = False
        self.pilotTag = args['Pilot Tag'].upper()
        flowState.addRFEmitter(self)

    def getChannel(self):
        for channel in range(0,len(raceband)):
            frequency = raceband[channel]
            if(frequency==self.frequency):
                break
        #print("got channel "+str(channel))
        #print("we are on frequency "+str(frequency))
        return channel

    def setChannel(self,channelNumber):
        if(channelNumber>7):
            channelNumber = 7
        if(channelNumber<0):
            channelNumber = 0
        self.frequency = raceband[channelNumber]

    def getFrequency(self):
        f = self.frequency
        if(self.spectating):
            f = 0
        return f

    def getPilotTag(self):
        return self.pilotTag

    def setPilotTag(self,newPilotTag):
        self.pilotTag = newPilotTag.upper()

    def setFrequency(self,frequency):
        self.frequency = frequency

    def getPower(self):
        return self.power

    def setPower(self,power):
        if(power>1000):
            power = 1000
        if(power<0):
            power = 0
        self.power = power

    def getPitMode(self):
        pitted = False
        if(self.pitMode):
            pitted = True
        if(self.spectating):
            pitted = True
        return pitted

    def setPitMode(self,pitMode):
        self.pitMode = int(pitMode == True)

    def update(self):
        if("spectate" in self.object):
            self.spectating = self.object['spectate']
