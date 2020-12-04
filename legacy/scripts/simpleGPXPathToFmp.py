#import bge
import xml.etree.ElementTree as ET
#logic = bge.logic
#flowState = logic.flowState
import ast
import os
import math
import re
#cont = logic.getCurrentController()
#owner = cont.owner
blendPath = ".."+os.sep#logic.expandPath("//")

#asset keys
ASSET_MGP_GATE = "asset MGP gate"
ASSET_MGP_GATE_DOUBLE = "asset MGP gate double"
ASSET_MGP_GATE_LARGE = "asset MGP gate large"
ASSET_MGP_GATE_HANGING_LARGE = "asset MGP gate hanging large"
ASSET_MGP_GATE_HIGH_LARGE = "asset MGP gate high large"
ASSET_MGP_GATE_DOUBLE_LARGE = "asset MGP gate double large"
ASSET_MGP_LADDER_LARGE = "asset MGP ladder large"
ASSET_MGP_GATE_ANGLED_DIVE_LARGE = "asset MGP gate angled dive large"
ASSET_MGP_GATE_DIVE_LARGE = "asset MGP gate dive large"
ASSET_MGP_HURDLE = "asset MGP hurdle"
ASSET_MGP_HURDLE_LARGE = "asset MGP hurdle large"
ASSET_MGP_FLAG = "asset MGP flag"
ASSET_MGP_POLE = "asset pole"
ASSET_LUMENIER_GATE_LARGE = "asset lumenier gate large"
ASSET_TABLE = "asset table"
ASSET_LAUNCH_PAD = "asset launch pad"
ASSET_CONE = "asset cone"
ASSET_START_FINISH = "asset start finish"
ASSET_CHECKPOINT = "asset checkpoint square"
ASSET_CONCRETE_BLOCK = "asset concrete block"
ASSET_PINE_TREE_TALL = "asset pine tree 12m"
ASSETS = [ASSET_MGP_GATE,ASSET_MGP_GATE_DOUBLE,ASSET_MGP_GATE_LARGE,ASSET_MGP_GATE_HANGING_LARGE,ASSET_MGP_GATE_HIGH_LARGE,ASSET_MGP_GATE_DOUBLE_LARGE,ASSET_MGP_LADDER_LARGE,ASSET_MGP_GATE_ANGLED_DIVE_LARGE,ASSET_MGP_GATE_DIVE_LARGE,ASSET_MGP_HURDLE,ASSET_MGP_HURDLE_LARGE,ASSET_MGP_FLAG,ASSET_MGP_POLE,ASSET_LUMENIER_GATE_LARGE,ASSET_TABLE,ASSET_LAUNCH_PAD,ASSET_CONE,ASSET_CONCRETE_BLOCK,ASSET_PINE_TREE_TALL,ASSET_START_FINISH,ASSET_CHECKPOINT]

def saveMapFile(content):
    f = open(blendPath+"maps"+os.sep+'importedMap.fmp','w')
    f.write(str(content))
    f.close()

def readXMLFile(fileName):
    fileName = blendPath+"maps"+os.sep+"import"+os.sep+fileName
    print("loading map: "+fileName)
    content = ET.parse(fileName).getroot()
    stripNs(content)
    print("map load complete...")
    return content

def gpsCoordToGrid(gpsCoord,centerCoord,minElevation):
    offset = [gpsCoord[0]-centerCoord[0],gpsCoord[1]-centerCoord[1]]
    offset = [math.radians(offset[0]),math.radians(offset[1])]
    x = -offset[0]*6367448.681507829
    y = (math.cos(offset[0])*offset[1])*(40075017/6.28319)
    z = gpsCoord[2]-minElevation
    print("z = "+str(z))
    return [x*10,y*10,z*10]

def getClosestAssetName(name):
    assetTokens = {}
    for i in range(0,len(ASSETS)):
        asset = ASSETS[i]
        assetTokens[asset] = {'name':asset,'score':0,'index':i,'tokens':asset.split()}
    nameTokens = name.split()
    print("finding closest match for "+str(name))
    for asset in assetTokens:
        tokenWeight = 1.0/len(assetTokens[asset]['tokens'])

        for i in range(0,len(assetTokens[asset]['tokens'])):
            token = assetTokens[asset]['tokens'][i]
            for j in range(0,len(nameTokens)):
                nameToken = nameTokens[j]
                if token.lower() in nameToken.lower():
                    assetTokens[asset]['score']+=tokenWeight
        #print("- "+str(asset)+": "+str(assetTokens[asset]['score']))
    match = {'score':0,'name':"asset pole"}
    for asset in assetTokens:
        #print("- "+str(asset)+": "+str(assetTokens[asset]['score']))
        if assetTokens[asset]['score']> match['score']:
            match = assetTokens[asset]

    return match['name']

def stripNs(el):
  '''Recursively search this element tree, removing namespaces.'''
  if el.tag.startswith("{"):
    el.tag = el.tag.split('}', 1)[1]  # strip namespace
  for k in el.attrib.keys():
    if k.startswith("{"):
      k2 = k.split('}', 1)[1]
      el.attrib[k2] = el.attrib[k]
      del el.attrib[k]
  for child in el:
    stripNs(child)

def main():
    gpxFileName = "track.gpx"
    gpxNode = readXMLFile(gpxFileName)
    map = {'assets': []}
    #{'n': 'asset launch pad', 'p': [-0.0, 275.0, 0.0], 'o': [-0.0, -0.0, -88.0], 's': [1.0, 1.0, 1.0], 'm': {'id': 2}}
    #xmlns = "{http://www.topografix.com/GPX/1/1}"

    avgPosition = [0,0]
    minElevation = None
    for child in gpxNode:
        print "child", child.tag, child.attrib
        for hyperChild in child:
            print "hyper child", hyperChild.tag, hyperChild.attrib

    print("looking up tracks under "+str(gpxNode))
    track = gpxNode.find('trk')
    print("adding track: "+str(track))
    for trackSegment in track.findall('trkseg'):
        for trackPoint in trackSegment.findall('trkpt'):
            lat = float(trackPoint.get('lat'))
            lon = float(trackPoint.get('lon'))
            ele = float(trackPoint.find('ele').text)

            name = ASSET_CONCRETE_BLOCK#str(waypoint.findall('name')[0].text)
            #extensions = waypoint.findall('extensions')[0]
            compass = 0#float(extensions.findall('compass')[0].text)
            print("wpt")
            print("- latitude: "+str(lat))
            print("- longitude: "+str(lon))
            print("- elevation: "+str(ele))
            print("- name: "+str(name))
            print("- compass: "+str(compass))
            asset = {}
            asset['n'] = name
            asset['p'] = [0,0,0]
            asset['lat'] = lat
            asset['lon'] = lon
            asset['ele'] = ele
            asset['o'] = [0,0,compass+90]
            map['assets'].append(asset)
            avgPosition[0]=avgPosition[0]+lat
            avgPosition[1]=avgPosition[1]+lon
            if minElevation == None:
                minElevation = ele
            else:
                if(ele<minElevation):
                    minElevation = ele

    totalPoints = len(map['assets'])
    avgPosition[0] = avgPosition[0]/totalPoints
    avgPosition[1] = avgPosition[1]/totalPoints
    print("avg position is "+str(avgPosition))

    for asset in map['assets']:
        asset['p'] = gpsCoordToGrid([asset['lat'],asset['lon'],asset['ele']],avgPosition,minElevation)
        asset['n'] = getClosestAssetName(asset['n'])
        print("placing "+str(asset['n'])+" "+str(asset))
    print("saving map...")
    saveMapFile(map)
    print("map saved")
    print("sucess!")
    print("minElevation = "+str(minElevation))

main()
