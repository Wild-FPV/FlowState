import bge
import time
from scripts.abstract.RaceFormat import RaceFormat
import FSNObjects
import copy
logic = bge.logic
render = bge.render
DEFAULT_BAND = {5658:{},5695:{},5732:{},5769:{},5806:{},5843:{},5880:{},5917:{}}
DEFAULT_FINISHED_CHANNELS = {5658:False,5695:False,5732:False,5769:False,5806:False,5843:False,5880:False,5917:False}
## TODO: we need to consider creating an update method that gets called once per game frame and updates the result of the methods
## otherwise we may run into performance issues with many objects calling these methods multiple times per frame
class RaceState:
    def __init__(self,flowState,formatPriority,timeLimit=120,lapLimit=9999,consecutiveLapCount=1,channelFrequencies=None,raceStartTime=None):
        flowState.debug("RaceState.init()")
        self.flowState = flowState
        self.raceFormat = RaceFormat(formatPriority,timeLimit,lapLimit,consecutiveLapCount)

        self.completedLaps = 0
        self.lastLapTime = None
        self.bestLapDuration = None
        self.holeshotDuration = None
        if channelFrequencies is None:
            self.channelTimelines = copy.deepcopy(DEFAULT_BAND)
        else:
            self.channelTimelines = channelFrequencies
        self.finishedChannels = copy.deepcopy(DEFAULT_FINISHED_CHANNELS)
        logic.countingDown = False
        self.holeshotComplete = False
        self.currentCheckpoint = 1

        countdownTime = self.flowState._countdownTime
        if(self.flowState.getGameMode()!=self.flowState.GAME_MODE_SINGLE_PLAYER):
            countdownTime = 10
        if(raceStartTime==None):
            self.raceStartTime = time.time()+self.flowState._countdownTime
        else:
            self.raceStartTime = raceStartTime

    def getRaceFormat(self):
        return self.raceFormat

    def raceCompleted(self):
        completed = False

        #if any of the frequencies have reached the time limit, the race is complete
        for channelIndex in self.channelTimelines:
            lapCount = self.getChannelLapCount(channelIndex)
            if lapCount >= self.raceFormat.lapLimit:
                completed = True
                break

        #if the time limit has expired, the race is complete
        if time.time()-self.raceStartTime >= self.raceFormat.timeLimit:
            completed = True

        return completed

    def setRaceFormat(self,raceFormat):
        self.raceFormat = raceFormat

    def incrementCheckpoint(self):
        if(self.currentCheckpoint>=self.flowState.trackState.getLastCheckpoint()):
            self.currentCheckpoint = 1
        else:
            self.currentCheckpoint+=1

    def getLastCheckpoint(self):
        return self.flowState.trackState.getLastCheckpoint()

    def getNextCheckpoint(self):
        return self.currentCheckpoint

    def getRaceTime(self):
        remainingTime = self.raceFormat.timeLimit-(time.time()-self.raceStartTime)
        if(remainingTime<0):
            remainingTime = 0
        return remainingTime

    def getChannelLastLapTime(self,channel):
        lapTimes = self.getChannelLapTimes(channel)
        if(lapTimes!=[]):
            lastLap = lapTimes[-1]
        else:
            lastLap = None
        return lastLap

    def getChannelTimeOfLastLap(self,channel):
        timeline = self.channelTimelines[channel]
        timeOfLastLap = None
        for key in timeline:
            timerEvent = timeline[key]
            if(timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_LAP) or (timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_HOLE_SHOT) or (timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_RACE_FINISH):

                if(timeOfLastLap==None) or (timerEvent.extra['time']>timeOfLastLap):
                    timeOfLastLap = timerEvent.extra['time']
        if(timeOfLastLap==None): #if the player didn't get any laps, consider the last lap ended at the tone
            return self.raceStartTime+self.raceFormat.timeLimit
        else:
            return timeOfLastLap

    def getChannelRaceCompletionTime(self,channel):
        return self.getChannelTimeOfLastLap(channel)-(self.raceStartTime)

    def getChannelLapTimes(self,channel):
        gatePassTimes = []
        lapTimes = []
        timeline = self.channelTimelines[channel]
        #create a list of lap pass times
        for key in timeline:
            timerEvent = timeline[key]
            if(timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_LAP) or (timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_HOLE_SHOT) or (timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_RACE_FINISH):
                gatePassTimes.append(timerEvent.extra['time'])

        if(len(gatePassTimes) >= 2): #if there aren't more than two passes, we don't yet have a completed lap
            #create a list of lap times based on the times the laps occured
            for i in range(0,len(gatePassTimes)-1):
                lapStartTime = gatePassTimes[i]
                lapEndTime = gatePassTimes[i+1]
                duration = lapEndTime-lapStartTime
                lapTimes.append(duration)
            return lapTimes
        else:
            return []

    def getChannelBestLapTime(self,channel):
        lapTimes = self.getChannelLapTimes(channel)
        if(lapTimes==[]):
            return None
        else:
            return min(lapTimes)

    def getChannelHoleShot(self,channel):
        timeline = self.channelTimelines[channel]
        holeShotTime = None
        for key in timeline:
            timerEvent = timeline[key]
            if(timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_HOLE_SHOT):
                holeShotTime = timerEvent.extra['time']-self.raceStartTime
                break
        return holeShotTime

    def getChannelFastestConcecutiveTime(self,channel,x):
        timeline = self.channelTimelines[channel]
        lapPasses = []
        lapDurations = []
        xConsecutiveTimes = []

        #create a list of lap pass times
        for key in timeline:
            timerEvent = timeline[key]
            if(timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_LAP) or (timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_HOLE_SHOT) or (timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_RACE_FINISH):
                lapPasses.append(timerEvent.extra['time'])

        #we need to handle when the players hasn't completed enough laps to qualify in the format
        if(len(lapPasses)>x):
            #create a list of lap durations based on the times the laps occured
            for i in range(0,len(lapPasses)-1):
                lapStartTime = lapPasses[i]
                lapEndTime = lapPasses[i+1]
                duration = lapEndTime-lapStartTime
                lapDurations.append(duration)
            #create a list of x consecutive times
            for i in range(0,len(lapDurations)-x+1):
                currentConsecutiveDuration = 0
                for j in range(0,x):
                    currentConsecutiveDuration += lapDurations[j+i]
                xConsecutiveTimes.append(currentConsecutiveDuration)
            return min(xConsecutiveTimes) #out of all the consecutive lap times, return the lowest one
        else:
            return None

    def getChannelLapCount(self,channel):
        laps = self.getChannelLapTimes(channel)
        return len(laps)

    def channelHasFinished(self, channel): #THIS ISN"T WORKING!!!!!! WE NEED TO FIX ITTTTTT!!!!!!!!!
        channelDone = False
        if(channel in self.channelTimelines):
            timeline = self.channelTimelines[channel]
            for key in timeline:
                timerEvent = timeline[key]
                if(timerEvent.eventType==FSNObjects.PlayerEvent.EVENT_RACE_FINISH):
                    channelDone = True
                #self.flowState.debug(timerEvent.eventType)
            return channelDone
        else:
            return False

    def addTimelineEvent(self,event,replicateNetwork=True):
        channel = event.extra['channel']
        #only log the event in the timeline if the player hasn't already completed the race
        if(not self.channelHasFinished(channel)):
            eventTime = time.time()

            #if the player logs a lap after the race is completed, mark their race as complete
            if(event.eventType==FSNObjects.PlayerEvent.EVENT_LAP):

                #instances in which the player is finishing the race
                if(self.raceCompleted()): #if the race has ended via time expiration, or another player reaching the lap limit
                    event.eventType = FSNObjects.PlayerEvent.EVENT_RACE_FINISH
                if(self.getChannelLapCount(channel)==self.raceFormat.lapLimit-1): #if the player is finishing their final lap
                    event.eventType = FSNObjects.PlayerEvent.EVENT_RACE_FINISH

            if(event.eventType==FSNObjects.PlayerEvent.EVENT_HOLE_SHOT):
                if(self.holeshotComplete==True):
                    event.eventType = FSNObjects.PlayerEvent.EVENT_LAP
                else:
                    self.holeshotComplete = True
            self.channelTimelines[channel][eventTime] = event

        #if we are in multiplayer, let other players know that this event has occured
        if(self.flowState.getGameMode()!=self.flowState.GAME_MODE_SINGLE_PLAYER) and (replicateNetwork):
            self.flowState.getNetworkClient().sendEvent(event)

        return self.channelTimelines

    def updateLaps(self):
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

    def getPlayerRanks(self):
        channelScores = []
        for channelNumber in self.channelTimelines:
            timeline = self.channelTimelines[channelNumber]
            lapCount = self.getChannelLapCount(channelNumber)
            lastLapTime = self.getChannelRaceCompletionTime(channelNumber)
            fastestXCon = self.getChannelFastestConcecutiveTime(channelNumber,self.raceFormat.consecutiveLapCount)
            if(lastLapTime!=None): #since we sort by least to greatest this must be negative since lower lap times are better
                lastLapTime = -lastLapTime
            else:
                lastLapTime = -float('inf')#self.raceFormat.timeLimit

            if(fastestXCon!=None): #since we sort by least to greatest this must be negative since lower lap times are better
                fastestXCon = -fastestXCon
            else:
                fastestXCon = -float('inf')#self.raceFormat.timeLimit

            channelScores.append({"channel":channelNumber,RaceFormat.FORMAT_MOST_LAPS:lapCount,RaceFormat.FORMAT_FIRST_TO_LAPS:lastLapTime,RaceFormat.FORMAT_FASTEST_CONSECUTIVE:fastestXCon}) #let's create a dictionary object to represent all the ways a player can perform

        orderedTimelineDicts = sorted(channelScores, reverse=True, key = lambda i: (i[self.raceFormat.formatPriority[0]], i[self.raceFormat.formatPriority[1]], i[self.raceFormat.formatPriority[2]]))
        #orderedTimelineDicts = sorted(channelScores, reverse=True, key = lambda i: (i[self.raceFormat.FORMAT_MOST_LAPS], i[self.raceFormat.FORMAT_FIRST_TO_LAPS], i[self.raceFormat.FORMAT_FASTEST_CONSECUTIVE]))
        channelRanks = []
        for timeline in orderedTimelineDicts:
            channelRanks.append(timeline['channel'])
        return channelRanks
