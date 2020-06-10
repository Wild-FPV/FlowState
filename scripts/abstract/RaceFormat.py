class RaceFormat:
    FORMAT_FASTEST_CONSECUTIVE = 0
    FORMAT_FIRST_TO_LAPS = 1
    FORMAT_MOST_LAPS = 2
    DEFAULT_FORMAT_PRIORITY = [FORMAT_MOST_LAPS,FORMAT_FIRST_TO_LAPS,FORMAT_FASTEST_CONSECUTIVE]
    def __init__(self,formatPriority=None,timeLimit=120,lapLimit=None,consecutiveLapCount=1):
        if formatPriority is None:
            self.formatPriority = DEFAULT_FORMAT_PRIORITY
        else:
            self.formatPriority = formatPriority
        self.timeLimit = timeLimit
        self.lapLimit = lapLimit
        self.consecutiveLapCount = consecutiveLapCount
