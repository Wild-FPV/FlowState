import bge
import copy
import time
from collections import OrderedDict

partTypes = ["Frame","Motor","VTX Antenna","Camera","Propeller"]
frameParts = {"Zypher Frame":"part zypher frame","Switchback Frame":"part switchback frame","Generic Frame":"part generic X frame"}#{"Zypher Frame":"part zypher frame","Generic Frame":"part generic X frame"}
motorParts = {"2205 Motor":"part motor 2205"}
vtxAntennaParts = {"Lumenier AXII":"part antenna vtx lolipop"}
cameraParts = {"Micro Camera":"part camera micro"}
propellerParts = {"Generic Propeller":"part generic propeller"}


if not hasattr(bge, "__component__"):
    render = bge.render
    logic = bge.logic
    try:
        flowState = logic.flowState
    except Exception as e:
        print("FPVModel: "+str(e))
        from scripts.abstract.FlowState import FlowState
        logic.flowState = FlowState()
        flowState = logic.flowState

    parts = {}
    parts.update(frameParts)
    parts.update(motorParts)
    parts.update(vtxAntennaParts)
    parts.update(cameraParts)
    parts.update(propellerParts )

class FPVModel(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Frame", {"Zypher Frame","Switchback Frame","Generic Frame"}),
        ("Motor", {"2205 Motor"}),
        ("VTX Antenna",{"Lumenier AXII"}),
        ("Camera",{"Micro Camera"}),
        ("Propeller",{"Generic Propeller"})
    ])

    def start(self, args):
        flowState.log("fpvModel: start("+str(args)+")")
        self._raceband = {1:5658,2:5695,3:5732,4:5769,5:5806,6:5843,7:5880,8:5917}
        self.vtxFrequency = self._raceband[1]
        self.vtxPower = 0
        self.trail = []
        self.lastUpdateTime = time.time()

        self.frame = args['Frame']
        self.motors = args['Motor']
        self.vtxAntenna = args['VTX Antenna']

        quadObject = self.spawnPart(self.frame,self.object)

        self.cameras = {"spectate":[],"fpv":[]}
        for child in self.object.children:
            if type(child).__name__ == "KX_Camera":
                self.cameras['spectate'].append(child)
                self.object['spectatorCamera'] = child
                child.removeParent()

        children = quadObject.children

        for child in children:
            if "spawn" in child:
                if child['spawn'] in partTypes:
                    partType = child['spawn']
                    spawnedPart = self.spawnPart(args[partType],child)
                    if(partType=="Camera"):
                        self.object['fpvCamera'] = spawnedPart.children[0]
        self.object['fpvModel'] = self

    def spawnPart(self,partName,spawnObject):
        newPart = self.addObject(parts[partName])
        newPart.position = spawnObject.position
        newPart.orientation = spawnObject.orientation
        newPart.setParent(spawnObject)
        return newPart

    def addObject(self,object):
        scene = logic.getCurrentScene()
        newObject = scene.addObject(object)
        return newObject

    def getFPVCameras(self):
        return self.cameras["fpv"]

    def setCamera(self,newCamera):
        scene = logic.getCurrentScene()
        scene.active_camera = newCamera

    def update(self):
        pass
