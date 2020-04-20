import bge
import copy
import time
from collections import OrderedDict

raceband = [5658,5695,5732,5769,5806,5843,5880,5917]
((abs(5658-5917))/25)+1
if not hasattr(bge, "__component__"):
    render = bge.render
    logic = bge.logic
    flowState = logic.flowState

class VTX(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Power Output (mw)", 25),
        ("Pit Mode",False),
        ("Frequency", raceband[0])
    ])

    def start(self, args):
        flowState.debug("vtx: start("+str(args)+")")
        self.power = args['Power Output (mw)']
        self.pitMode = int(args['Pit Mode'] == True)
        self.frequency = args['Frequency']
        self.signalStrength = 0
        self.object['vtx'] = self
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
        return self.frequency

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
        return self.pitMode

    def setPitMode(self,pitMode):
        self.pitMode = int(pitMode == True)
        flowState.debug("vtx: setPidMode("+str(self.pitMode)+")")

    def update(self):
        pass
