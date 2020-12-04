import bge
import copy
import time
from collections import OrderedDict

if not hasattr(bge, "__component__"):
    global render
    render = bge.render
    logic = bge.logic

partTypes = ["Frame","Motor","VTX Antenna","Camera"]
parts = {"Zypher Frame":"part zypher frame","Generic Frame":"part generic X frame","2205 Motor":"part motor 2205","Lumenier AXII":"part antenna vtx lolipop","Micro Camera":"part camera micro"}
    
class QuadFrame(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Frame", {"Zypher Frame"}),
        ("Motor", {"2205 Motor"}),
        ("VTX Antenna",{"Lumenier AXII"}),
        ("Camera",{"Micro Camera"})
    ])

    def start(self, args):
        self.trail = []
        self.lastUpdateTime = time.time()
        
        self.frame = args['Frame']
        self.motors = args['Motor']
        self.vtxAntenna = args['VTX Antenna']
        
        quadObject = self.spawnPart(self.frame,self.object)
        
        children = quadObject.children
        
        for child in children:
            if "spawn" in child:
                if child['spawn'] in partTypes:
                    partType = child['spawn']
                    self.spawnPart(args[partType],child)
        
    def spawnPart(self,partName,spawnObject):
        scene = logic.getCurrentScene()
        newPart = scene.addObject(parts[partName])
        newPart.position = spawnObject.position
        newPart.setParent(spawnObject)
        return newPart
        
    def update(self):
        a = 1