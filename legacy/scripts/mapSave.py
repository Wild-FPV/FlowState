import bge.logic as logic
import math
import random
import copy
import bge.render as render
import numpy
import os
flowState = logic.flowState
cont = logic.getCurrentController()
own = cont.owner
scene = logic.getCurrentScene()
blendPath = logic.expandPath("//")
def main():
    map = {"assets":[]}
    for object in scene.objects:
        if "asset" in object and "solid" in object:
            if object.position[2] > -1:
                print("saving "+str(object))
                asset = object
                o = asset.orientation.to_euler()
                o = [math.degrees(o[0]),math.degrees(o[1]),math.degrees(o[2])]
                m = {}
                if('metadata' in object):
                    m = object['metadata']
                    print("saving metadata "+str(m))
                map['assets'].append({"n":asset.name,"p":list(asset.position),"o":o,"s":list(asset.localScale),"m":m})
            else:
                print("deleting object placed below ground")
                object.endObject()

    saveMapToFile(map,flowState.getSelectedMap())

def saveMapToFile(map,fileName):
    fileName = blendPath+"maps"+os.sep+fileName
    logic.flowState.log("saving map: "+fileName)
    print("saving map to: "+fileName)
    try:
        with open(fileName, 'w+') as saveFile:
            saveFile.write(str(map))
            saveFile.close()
    except Exception as e:
        logic.flowState.log("map save error: "+str(e))
    logic.flowState.log("map save complete: "+fileName)

main()
