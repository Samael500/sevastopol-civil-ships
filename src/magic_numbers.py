class MN:
    STOP = 0.55 #minimal cignificant speed khot

    LASTPOSLEN = 10 #length of lastpos
    
    TRUEPOS = LASTPOSLEN + 5 #the ship is 100% on the route

    MAX = 100500 #some very large number
    
    VIEWANGLE = 80 #angle at which it is considered that the boat went to target

    DELAY = 60 #time to sleep

    DELTA = 0.0025 #distans to determinate next pier

    DEADEND = 0.0090 #distans to deadend place

    UNKNOWN = "UNKNOWN" #unicode("Неизвестности", "UTF-8") #if pier is None

    STAT = 1 #statistic hour delay

    STAT2 = 15 #statistic minute start

    ITERATION = 10 #number of new massages try
