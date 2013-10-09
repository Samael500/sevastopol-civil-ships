class MN:
    STOP = 0.55 #minimal cignificant speed khot

    LASTPOSLEN = 10 #length of lastpos
    
    TRUEPOS = LASTPOSLEN + 5 #the ship is 100% on the route

    MAX = 100500 #some very large number
    
    VIEWANGLE = 60 #angle at which it is considered that the boat went to target

    DELAY = 60 #time to sleep

    DELTA = 0.0015 #distans to determinate next pier

    DEADEND = 0.0090 #distans to deadend place

    UNKNOWN = "Неизвестности" #if pier is None
