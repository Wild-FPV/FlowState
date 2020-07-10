import bge.logic as logic
import math
import random
import copy
import bge.render as render
import time
import statistics
import FSNClient
import FSNObjects
import mathutils

flowState = logic.flowState
cont = logic.getCurrentController()
own = cont.owner
logic.player = own
droneSettings = logic.flowState.getDroneSettings()
radioSettings = logic.flowState.getRadioSettings()
scene = logic.getCurrentScene()
mass = own.mass
gravity = 98*mass
camera = scene.objects['cameraMain']
own['quadCamera'] = camera
game = scene.objects['Game']

try:
    logic.lastLogicTic
except:
    logic.lastLogicTic = float(time.perf_counter())
    print("creating time")
frameTime = float(time.perf_counter())-logic.lastLogicTic
logic.lastLogicTic = float(time.perf_counter())

if(logic.getAverageFrameRate()!=0):
    dm = frameTime*60
else:
    dm = 1
if(dm>1):
    dm = 1
def getAngularAcceleration():
    av = own.getAngularVelocity(True)

    if "init" in own:
        lastAv = own['lastAngularVel']
        own['angularAcc'] = getArrayProduct([av[0]-lastAv[0],av[1]-lastAv[1],av[2]-lastAv[2]])
        own['lastAngularVel'] = own.getAngularVelocity(True)

def setupLaunchPads():
    flowState.log("reconstructing RF environment")
    launchPads = logic.flowState.trackState.launchPads
    playerVideoChannel = flowState.getDroneSettings().videoChannel

    #set all the track launch pads to be video receivers. we may create a dedicated ground station object for this in the future
    for i in range(0,len(flowState.getRFEnvironment().getReceivers())):
        flowState.log("setting channel for vrx "+str(i))
        if(i==8):
            break
        receiver = flowState.getRFEnvironment().getReceivers()[i]
        receiver.setChannel(i)
        launchPad = launchPads[i]
        flowState.log("channel = "+str(receiver.getFrequency()))

def initAllThings():
    flowState.debug(flowState)
    logic.player['camera'] = scene.objects['cameraMain']
    flowState.getRaceState().incrementCheckpoint()

    #logic.setPhysicsTicRate(120)
    #logic.setLogicTicRate(120)
    #print("max logic ticks per frame: "+str(logic.getMaxLogicFrame()))
    #print("logic ticks per second: "+str(logic.getLogicTicRate()))
    #print("max physics ticks per frame: "+str(logic.getMaxPhysicsFrame()))
    #logic.setLogicTicRate(60)

    flowState.debug("physics ticks per second: "+str(logic.getPhysicsTicRate()))
    logic.ghosts = []
    av = own.getAngularVelocity(True)
    own['airSpeedDiff'] = 0
    own['lastAirSpeedDiff'] = 0
    own['lastAngularVel'] = av
    own['angularAcc'] = 0
    own['settled'] = False
    own['settleStartTime'] = time.perf_counter()
    flowState.debug("SETTLE TIME IS "+str(own['settleStartTime']))
    own['settleDuration'] = 0
    own['settleFrameRates'] = []
    logic.player['camera']['vtx'].setChannel(flowState.getInitialVTXChannel())
    flowState.getRFEnvironment().getCurrentVRX().setChannel(flowState.getInitialVTXChannel())
    respawn()
    flowState.resetRaceState()
    own['rxPosition'] = copy.deepcopy(logic.flowState.trackState.launchPads[0].position) #needs to be removed now that we have RFEnvironment
    own['rxPosition'][2]+=100
    own['lastArmState'] = False
    own.mass = droneSettings.weight/1000
    logic.countingDown = True
    logic.countdown = -1
    logic.maxGForce = 0
    logic.finishedLastLap = False
    logic.flowState.setNotification({'Text':""})
    #own['rxPosition'] = [-2279.73,-30.8,90]
    #try:
    #    del game['shaderInit']
    #except:
    #    pass
    graphicsSettings = flowState.getGraphicsSettings()
    shaders = graphicsSettings.shaders
    if shaders:
        logic.player['camera'].lens= 5.823523998260498
    else:
        logic.player['camera'].lens= 10
    flowState.debug("init")

def respawn():
    #if(flowState.getGameMode()==flowState.GAME_MODE_SINGLE_PLAYER):
        #flowState.resetRFEnvironment() #we only need to reset the RF environment in single player since ghosts get deleted

    #fix the quad
    own['damage'] = 0
    own['oporational'] = True
    own['vtxOporational'] = True

    #make sure the quad isn't moving
    own.setLinearVelocity([0,0,0],True)
    own.setAngularVelocity([0,0,0],True)
    own['lastAv'] = [0,0,0]
    if 'lastVel' in own:
        own['lastVel'] = [0,0,0]

    #put the quad on the launch pad
    flowState.debug("GOT LAUNCH PADS: "+str(logic.flowState.trackState.launchPads))
    flowState.debug(len(logic.flowState.trackState.launchPads)-1)

    launchPadNo = 0
    try:
        flowState.debug("GOT LAUNCH PADS: "+str(launchPadNo))
        rx = flowState.getRFEnvironment().getReceiver()
        flowState.debug("rx = "+str(rx))
        launchPadNo = rx.getChannel()#random.randint(0,len(logic.flowState.trackState.launchPads)-1)
        flowState.debug("SET LAUNCH PAD NO!!!!"+str(launchPadNo))
    except Exception as e:
        flowState.error(e)

    try:
        launchPos = copy.deepcopy(logic.flowState.trackState.launchPads[launchPadNo].position)
        launchOri = copy.deepcopy(logic.flowState.trackState.launchPads[launchPadNo].orientation)
        own['launchPosition'] = [launchPos[0],launchPos[1],launchPos[2]+1]
        own.position = own['launchPosition']
        own.orientation = launchOri
        flowState.debug(logic.flowState.trackState.launchPads)
        flowState.debug("SPAWNING!!!"+str(launchPadNo)+", "+str(launchPos))
    except:
        own['launchPosition'] = [0,0,0]
        own.position = [0,0,0]
        print("we don't have launch pads yet")

def resetGame():
    scene.active_camera = camera
    setCameraAngle(flowState.getDroneSettings().cameraTilt)

    for ghost in logic.ghosts:
        ghost['obj']['fpvCamera'].endObject()
        ghost['obj']['spectatorCamera'].endObject()
        ghost['obj'].endObject()
    logic.ghosts = []
    own['canReset'] = False
    initAllThings()

def getArrayProduct(array):
    a = array[0]
    b = array[1]
    c = array[2]
    return math.sqrt((a**2)+(b**2)+(c**2))

def getAcc():
    lv = own.getLinearVelocity(True)
    try:
        own['acc'] = (abs(own['lastVel']-getArrayProduct(lv)))
        try:
            if own['settled']:
                elapsedTime = 1/logic.getAverageFrameRate()
                force = ((abs(own['lastVel']-getArrayProduct(lv))/elapsedTime)/100)+1
                #print("force: "+str(force)+"\nelapsedTimie: "+str(elapsedTime))
                if own['armed']:
                    if logic.maxGForce < force:
                        logic.maxGForce = force
                else:
                    logic.maxGForce = 0
                logic.gForce = force
        except Exception as e:
            flowState.error(e)
            own['armed'] = False
            logic.gForce = 0
            logic.maxGForce = 0

        own['airSpeedDiff'] = (own['lastAirSpeedDiff']-lv[2])*0.01
        own['lastVel'] = getArrayProduct(lv)
    except Exception as e:
        try:
            own['lastVel'] = getArrayProduct(lv)
            own['acc'] = abs(own['lastVel']-getArrayProduct(lv))
            own['lastAirSpeedDiff'] = lv[2]
        except Exception as e:
            flowState.error(e)

def getStickPercentage(min,max,value):
    resolution = abs(min)+abs(max)
    percent = abs(((value-min)/resolution))
    (0+(100/2))/100.0
    return percent

def setup():
    setCameraAngle(droneSettings.cameraTilt)
    if(logic.flowState.mapLoadStage == flowState.MAP_LOAD_STAGE_DONE):
        if 'setup' not in own:
            flowState.debug("Joystick.setup: we aren't setup yet!")
            own['setup'] = True
            own['canReset'] = False
            setupLaunchPads()
            initAllThings()


def setCameraAngle(angle):
    if("initOri" not in camera): #let's take note of the initial camera orientation if this is our first time (0 degrees)
        cox,coy,coz = mathutils.Matrix.to_euler(camera.localOrientation)
        camera['initOri'] = [cox,coy,coz]
    #let's do the fancy math to set the camera orientation
    angle = (angle/180)*math.pi
    initOri = camera['initOri']
    newCameraOri = [initOri[0]+angle,initOri[1],initOri[2]]
    camera.localOrientation = newCameraOri

def getSwitchValue(switchPercent,switchSetpoint,inverted):
    #if(switchInverted):
    #    switch = switchPercent>switchSetpoint
    #else:
    #    switch = switchPercent<switchSetpoint
    if(not inverted):
        switch = switchPercent>switchSetpoint
    else:
        switch = (1-switchPercent)>switchSetpoint
    return switch

def getRXVector(scale,rxPos):
    vectTo = own.getVectTo(rxPos)
    v = vectTo[1]
    vs = abs(v[0])+abs(v[1])+abs(v[2])
    vect = [(v[0]/vs)*scale,(v[1]/vs)*scale,(v[2]/vs)*scale]
    return vect

def applyVideoStatic():
    if(flowState.getRFEnvironment().getCurrentVRX()!=None):
        rxInterference = flowState.getRFEnvironment().getCurrentVRX().snr
    else:
        rxInterference = 0.1

    game['rfNoise'] = 100/rxInterference
    #game['rfNoise'] = (groundBreakup*interference+game['eNoise'])+(rxInterference*100000)#((distance/txPower)*.01*groundBreakup*interference+game['eNoise'])+rxInterference
    #game['rfNoise'] = ((distance/txPower)*groundBreakup*interference+game['eNoise'])#+rxInterference

def killVideo():
    pass
    #game['rfNoise'] = 100

def stickInputToDPS(rcData, superRate=70, rcRate=90, rcExpo=0.0, superExpoActive=True):
    #0.27
    inputValue = rcCommand(rcData, rcRate, rcExpo)
    angleRate = None
    if (superExpoActive):
        rcFactor = abs(inputValue) / (500 * rcRate / 100)
        rcFactor = 1 / (1 - rcFactor * superRate / 100)
        angleRate = rcFactor * 27 * inputValue / 16
    else:
        angleRate = (superRate + 27) * inputValue / 16
    #angleRate = constrain(angleRate, -8190, 8190); // Rate limit protection
    return angleRate/230

def rcCommand(rcData, rcRate, rcExpo):
    midRc = 1500
    tmp = min(abs(rcData - midRc), 500) / 100
    #tmp = abs(rcData)/100
    result = ((2500 + rcExpo * (tmp * tmp - 25)) * tmp * rcRate / 2500)
    if (rcData < midRc):
        result = -result
    return result

def forceAboveGround():
    if own.position[2] <0:
        p = own.position
        own.position = [p[0],p[1],0.1]

def main():
    forceAboveGround()
    #print("perf: "+str(1.0/frameTime))
    #print("afps: "+str(logic.getAverageFrameRate()))

    #Do the things and the stuff
    joy = cont.sensors["Joystick"]
    propRay = cont.sensors["Ray"]
    axis = joy.axisValues
    #print(axis)
    #xbox controllers....
    if(radioSettings.dedicatedThrottleStick == False):
        axis[radioSettings.throttleChannel] -= (radioSettings.maxThrottle-radioSettings.minThrottle)/2
    if(axis != []): #if a radio is connected

        #stick offsets
        own['channel0'] = axis[0]
        own['channel1'] = axis[1]
        own['channel2'] = axis[2]
        own['channel3'] = axis[3]
        axis[radioSettings.rollChannel]+=radioSettings.rollOffset
        axis[radioSettings.yawChannel]+=radioSettings.yawOffset
        axis[radioSettings.pitchChannel]+=radioSettings.pitchOffset

        values = []
        center = 7000
        sensativity = .0008
        for value in axis:
            values.append((value-center)*sensativity)


        throttleInverted = -(int(radioSettings.throttleInverted)-0.5)*2
        yawInverted = -(int(radioSettings.yawInverted)-0.5)*2
        pitchInverted = -(int(radioSettings.pitchInverted)-0.5)*2
        rollnverted = -(int(radioSettings.rollInverted)-0.5)*2
        armInverted = -(int(radioSettings.armInverted)-0.5)*2
        resetInverted = -(int(radioSettings.resetInverted)-0.5)*2

        throttle = (axis[radioSettings.throttleChannel-1])*throttleInverted
        yaw = axis[radioSettings.yawChannel-1]*yawInverted
        pitch = axis[radioSettings.pitchChannel-1]*pitchInverted
        roll = axis[radioSettings.rollChannel-1]*rollnverted
        armSwitch = axis[radioSettings.armChannel-1]*armInverted
        resetSwitch = axis[radioSettings.resetChannel-1]*resetInverted

        throttlePercent = (getStickPercentage(radioSettings.minThrottle,radioSettings.maxThrottle,throttle))
        yawPercent = getStickPercentage(radioSettings.minYaw,radioSettings.maxYaw,yaw)
        pitchPercent = getStickPercentage(radioSettings.minPitch,radioSettings.maxPitch,pitch)
        rollPercent = getStickPercentage(radioSettings.minRoll,radioSettings.maxRoll,roll)
        armPercent = getStickPercentage(radioSettings.minArm,radioSettings.maxArm,armSwitch)
        resetPercent = getStickPercentage(radioSettings.minReset,radioSettings.maxReset,resetSwitch)
        armed = getSwitchValue(armPercent,radioSettings.armSetpoint,radioSettings.armInverted)
        reset = getSwitchValue(resetPercent,radioSettings.resetSetpoint,radioSettings.resetInverted)
        logic.throttlePercent = throttlePercent

    else: #if no radio is connected
        throttlePercent = 0
        yawPercent = 0
        pitchPercent = 0
        rollPercent = 0
        armed = False
        reset = False

    own['armed'] = armed
    if(own['armed'] != own['lastArmState']):
        own['lastArmState'] = own['armed']

    rotationActuator = cont.actuators["movement"]

    #apply rotational force
    PE = droneSettings.pitchExpo
    RE = droneSettings.rollExpo
    YE = droneSettings.yawExpo
    pp = (pitchPercent-.5)*2
    rp = (rollPercent-.5)*2
    yp = (yawPercent-.5)*2
    logic.errorLog = str(axis)
    ps = 1
    rs = 1
    ys = 1
    if(pp<0):
        ps = -1
    if(rp<0):
        rs = -1
    if(yp<0):
        ys = -1

    dps = 0.0174533
    RE = 1
    EXPO = 0
    #pitchForce = -(((abs(pp)*g['pitchRate']*85)**(RE))*ps)/foo
    #roleForce = (((abs(rp)*g['rollRate']*85)**(RE))*rs)/foo
    #yawForce = -(((abs(yp)*g['yawRate']*85)**(RE))*ys)/foo

    #-(abs(pp)*ps*dps*(g['pitchRate']*200))**((1+RE)*.82515)
    #print(abs(rp))
    #print((abs(rp)*rs*dps*(g['roleRate']*200)))
    #ps*pow((abs(pp)*(g['pitchRate']*200)),abs(pp)+2.2)*.434588)
    a = .48
    b = .834
    #pitchForce = -ps*pow((abs(pp)*(g['pitchRate']*200)),(abs(pp)*(PE)*a)+b)*dps
    #roleForce = rs*pow((abs(rp)*(g['rollRate']*200)),(abs(rp)*(RE)*a)+b)*dps
    #yawForce = -ys*pow((abs(yp)*(g['yawRate']*200)),(abs(yp)*(YE)*a)+b)*dps

    pitchForce = -stickInputToDPS((pitchPercent*1000)+1000,droneSettings.pitchSuperRate,droneSettings.pitchRate,droneSettings.pitchExpo,True)
    roleForce = stickInputToDPS((rollPercent*1000)+1000,droneSettings.rollSuperRate,droneSettings.rollRate,droneSettings.rollExpo,True)
    yawForce = -stickInputToDPS((yawPercent*1000)+1000,droneSettings.yawSuperRate,droneSettings.yawRate,droneSettings.yawExpo,True)
    getAngularAcceleration()
    getAcc()
    if armed:
        if (own['oporational'] == True)&armed:
            if own['settled']:
                if(flowState.getGameMode()==flowState.GAME_MODE_SINGLE_PLAYER) or (flowState.getGameMode()==flowState.GAME_MODE_TEAM_RACE):
                    #WAYS YOU CAN KILL YOUR QUAD
                    if (own['acc'] > 150):
                        flowState.log("You exploded your quad")
                        own['oporational'] = False
                        own['vtxOporational'] = False

                    if (own['acc'] > 60):
                        if(cont.sensors['PropStrike'].positive):
                            flowState.log("Rotational prop strike")
                            own['damage'] += own['acc']*0.004

                    if (own['damage'] > 2.5):
                        flowState.log("Blown power train")
                        own['oporational'] = False

    #some boolean math to determin if the vtx is working and on
    vtxPitMode = not int(own['vtxOporational'] & armed)
    if(bool(vtxPitMode)!=bool(camera['vtx'].getPitMode())):
        camera['vtx'].setPitMode(vtxPitMode)

    lv = own.getLinearVelocity(True)
    applyVideoStatic()
    if(own['oporational']):

        if(armed):
            try:
                if own['airSpeedDiff'] < 0:
                    own['airSpeedDiff'] = 0
                propwash = math.pow((((own['airSpeedDiff']*.3)+(((own['damage']-0.1)*.5))*2)*.1145),1.5)*((throttlePercent*10)+.4)
                if propwash > 0.08:
                  propwash = 0.08

            except:
                propwash = 0




            #print(thrust)
            lvl = own.localLinearVelocity

            av = own.getAngularVelocity(True)

            #if(propRay.positive==False):
            #if(not cont.sensors['PropStrike'].positive):
            rx = (random.randrange(0,200)-100)/300
            ry = (random.randrange(0,200)-100)/300
            rz = (random.randrange(0,200)-100)/300
            pwrx = (rx*propwash/(1+propwash*1.00005))*28
            pwry = (ry*propwash/(1+propwash*1.00005))*28
            pwrz = (rz*propwash/(1+propwash*1.00005))*28

            angularAcc = own['angularAcc']

            #AIR DAMPENING
            #FD = .99978 #use for X
            #FD = .99996 #use for true Z
            tdm = .9 #totalDragMultiplier
            sdm = 0.92 #sideDragMultiplier
            fdm = 0.9 #frontalDragMultiplier
            tdm = 1.3 #topDragMultiplier

            tdm = 0.0 #totalDragMultiplier
            sdm = 1 #sideDragMultiplier
            fdm = 1 #frontalDragMultiplier
            tdm = 1 #topDragMultiplier

            qd = [0.013014*dm*tdm*sdm,0.0111121*dm*fdm*tdm,0.0071081*dm*tdm] #air drag
            qd = [tdm,tdm,tdm]
            #own.setLinearVelocity([lv[0]/(1+qd[0]),lv[1]/(1+qd[1]),lv[2]/(1+qd[2])],True)
            #own.setLinearVelocity([lv[0]/(1+qd[0]),lv[1]/(1+qd[1]),lv[2]],True)
            #print(dm)
            st = 1*dm #how quick can the motor/pid orient the quad
            lav = own.getAngularVelocity(True)
            xav = (((pitchForce)*st)+(lav[0]*(1-st)))+pwrx
            yav = ((roleForce)*st)+(lav[1]*(1-st))+pwry
            zav = yawForce+pwrz
            #maxAngularAcceleration = 6
            #maxAngularAccelerationYaw = 6
            #xavDiff = pitchForce-lav[0]
            #yavDiff = roleForce-lav[1]
            #zavDiff = yawForce-lav[2]
            #print(str(xavDiff)+":"+str(yavDiff))
            #if abs(xavDiff) > maxAngularAcceleration:
            #    sign = ((1 if xavDiff < 0 else 0)-.5)*2
            #    xav = ((pitchForce+pwrx)*(0.5*dm))+(lav[0]*(1-(0.5*dm)))
            #    #print("x "+str(xavDiff))
            #if abs(yavDiff) > maxAngularAcceleration:
            #    sign = ((1 if yavDiff < 0 else 0)-.5)*2
            #    yav = ((roleForce+pwry)*(0.5*dm))+(lav[1]*(1-(0.5*dm)))
            #    #print("y "+str(yavDiff))
            #if abs(zavDiff) > maxAngularAccelerationYaw:
            #    sign = ((1 if zavDiff < 0 else 0)-.5)*2
            #    zav = ((yawForce+pwrz)*(0.5*dm))+(lav[2]*(1-(0.5*dm)))
            #    #print("z "+str(zavDiff))
            own.setAngularVelocity([xav,yav,zav], True)
                #if av [2] <0:
                    #own.setAngularVelocity([av[0],av[1],0],False)
            #thrust = thrust/((propwash*0.89)+1)
            #maxRPM = g['rpm']#29.7230769
            motorKV = droneSettings.motorKV
            cellCount = droneSettings.batteryCellCount
            cellVoltage = 4.2
            maxRPM = motorKV*cellCount*cellVoltage
            propAdvance = 5

            maxThrust = droneSettings.thrust/10
            propLoad = (((lvl[0]*.8)+(lvl[1]*.8)+(lvl[2]*1.2))*1000)/maxRPM
            #propLoad = (lvl[2]*10000)/maxRPM
            propAgressiveness = 1.4
            propThrottleCurve = 1

            currentRPM = maxRPM*throttlePercent
            #propLoad = lvl[2]*currentRPM/maxRPM



            #thrust = ((throttlePercent**propThrottleCurve)*.85)*(maxThrust-((propLoad**propThrottleCurve)/((maxSpeed**propThrottleCurve)/maxThrust)))
            thrustSetpoint = throttlePercent#+(abs(yawPercent-.5)*.25)
            if(thrustSetpoint>1):
                thrustSetpoint = 1

            staticThrust = ((thrustSetpoint**propThrottleCurve))*maxThrust#*1000)#-(currentSpeed/maxSpeed)

            staticThrust = (thrustSetpoint**propThrottleCurve)*droneSettings.thrust

            thrust = (staticThrust/10)-(propLoad)-(propwash*100)
            #thrust = staticThrust-(propLoad)-(propwash*100)
            if(thrust<0):
                thrust = 0
            try:
                thrust = thrust.real
            except:
                pass
            propPitch = 4.6
            propSize = 5
            newtonToKg = 0.101971621
            motorNumber = 4
            currentRPM = throttlePercent*maxRPM
            #thrust = 100*((4.392399*(10**-8))*currentRPM*((propSize**3.5)/math.sqrt(propPitch))*((4.23333*(10**-4))*currentRPM*propPitch-(currentSpeed/10)))*newtonToKg*motorNumber

            #if(thrust<0):
            #    thrust = 0
            if 'lastThrust' in own:
                thrust = (thrust*st)+(own['lastThrust']*(1-st))
            own['lastThrust'] = thrust

            if flowState.getRaceState().raceStartTime < time.time(): #player shouldn't be able to take off if the race hasn't started
                own.applyForce([0,0,thrust],True)
            else:
                launchBoundry = 2
                maxX = own['launchPosition'][0]+(launchBoundry/2)
                minX = own['launchPosition'][0]-(launchBoundry/2)
                maxY = own['launchPosition'][1]+(launchBoundry/2)
                minY = own['launchPosition'][1]-(launchBoundry/2)
                minZ = own['launchPosition'][2]-0.5
                if(own.position[0]>maxX):
                    own.position[0] = maxX
                if(own.position[0]<minX):
                    own.position[0] = minX
                if(own.position[1]>maxY):
                    own.position[1] = maxY
                if(own.position[1]<minY):
                    own.position[1] = minY
                if(own.position[2]<minZ):
                    own.position[2] = minZ
                v = own.getLinearVelocity()
                own.setLinearVelocity([0,v[1],v[2]],True)

            if(droneSettings.autoLevel):
                maxAngle = 100
                #own.setAngularVelocity([0,0,0], True)
                own.angularVelocity[0] = 0
                own.angularVelocity[1] = 0
                x = (pitchPercent-0.5)*250.0
                y = (rollPercent-0.5)*250.0
                z = (1)*maxAngle
                levelTotal = abs(x)+abs(y)+abs(z)
                x/=levelTotal
                y/=levelTotal
                z/=levelTotal
                #own.alignAxisToVect(setOrientation, 2, 0.94)
                own.orientation = [-x,y,own.orientation.to_euler().z]

    else:
        thrust = 0
    if(not own['vtxOporational']):
        killVideo()

    if(reset == False)&(own['canReset']==False):
        own['canReset'] = True
    if((reset)&own['canReset']):
        if(flowState.getGameMode()==flowState.GAME_MODE_SINGLE_PLAYER):
            flowState.log("resetting single player game")
            resetGame()
        if(flowState.getGameMode()==flowState.GAME_MODE_MULTIPLAYER):
            flowState.log("reset")
            respawn()
            #resetEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_RESET,flowState.getNetworkClient().clientID,{"reset":time.time()+10})
            #flowState.getNetworkClient().sendEvent(resetEvent)
            #resetGame()
            own['canReset'] = False
        if(flowState.getGameMode()==flowState.GAME_MODE_TEAM_RACE):
            flowState.log("resetting team race")
            #resetEvent = FSNObjects.PlayerEvent(FSNObjects.PlayerEvent.PLAYER_MESSAGE,flowState.getNetworkClient().clientID,"reset")
            #flowState.getNetworkClient().sendEvent(resetEvent)
            #print("sending reset message")
            own['canReset'] = False
            respawn()


    own['lastAv'] = own.getAngularVelocity(True)
    #if(logic.getAverageFrameRate()>60):
    #    logic.setTimeScale(1)
own.applyForce([0,0,-98*own.mass],False)
def settle():
    logic.setTimeScale(droneSettings.timeScale/100.0)
    own['settled'] = True
    logic.isSettled = True
    flowState.log("SETTLING!!!!!!!")
def isSettled(): #TO-DO get rid of all the settingling logic. The launch pads should be more stable now
    if not own['settled']:
        #logic.setTimeScale(0.001)
        if(flowState.getGameMode()==flowState.GAME_MODE_SINGLE_PLAYER):
            logic.isSettled = False
            fps = logic.getAverageFrameRate()
            avgFPSList = own['settleFrameRates']
            avgFPSList.append(fps)
            deviation = 100
            if(len(avgFPSList)>1):
                deviation = statistics.stdev(avgFPSList)
            if len(avgFPSList)>100:
                if deviation < 300:
                    settle()
            else:

                own.setLinearVelocity([0,0,0],True)
                own.position = own['launchPosition']
            if len(avgFPSList)>1000:
                del avgFPSList[0]
                settle()
                flowState.log("WARNING!!!: FPS did not become stable after 2000 frames. Expect physics instability...")
                flowState.log("standard deviation: "+str(deviation))
        else: #we are in multiplayer and should wait a fixed time
            if ((time.perf_counter()-own['settleStartTime'])>3):
                settle()
                flowState.log("settling due to time expiration in multiplayer")
    #else:
    #    #if(logic.finishedLastLap):
    #    #    logic.setTimeScale(0.001)
    #    #    #own.setLinearVelocity([0,0,0],True)

if (logic.flowState.mapLoadStage == flowState.MAP_LOAD_STAGE_DONE):
    setup()
    if(own['setup']):
        if(own.sensors['clock'].positive):
            main()
        isSettled()
if(own.sensors['Message'].positive):
    resetGame()
