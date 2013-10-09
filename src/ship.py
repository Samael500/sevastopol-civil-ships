from coordinates import Coordinates
from scrapper import Scrapper
from enum import Enum
from magic_numbers import MN

ship_status = Enum("ONLINE", "OFFLINE", "INDEADEND")
message = Enum("HELLO", "GOODBYE", "PASS", "STAND", "UNDERWAY")

class Ship:
    '''
    A Ship class
    '''
    def __init__(self, name, speed=None, course=None, coordinates=None):
        # TODO: Add last_update time
        if isinstance(name, list):
            self.name = name[0]
            self.nick = unicode(name[1], "UTF-8")[:-1] # \n Kill
        else:
            self.name = self.nick = name

        self.coordinates = coordinates
        self.speed = speed
        self.status = None#ship_status.OFFLINE
        
        self.lastpos = []
        self.lastpierindex = None
        self.route = None

        self.alive = False
        self.printedpos = None

    def reset(self):
        #self.coordinates = None
        #self.course = None
        #self.speed = None       
        
        self.lastpos = []
        self.lastpierindex = None
        self.route = None
        
        #self.status = ship_status.OFFLINE

    def msg(self):
        res = message.PASS
        #print self
        if self.alive and (self.status == ship_status.ONLINE) :
            self.printedpos = self.coordinates
            if (self.speed < MN.STOP):
                res = message.STAND
            else :
                res = message.UNDERWAY

        return message.reverse_mapping[res]

    def msgupdate(self, data, zone):
        res = message.PASS

        A = self.status
        #aCoord = self.coordinates

        self.update(data)
        self.deadend(zone)

        B = self.status
        #bCoord = self.coordinates

        if self.printedpos and self.coordinates:
            self.alive = ((self.printedpos - self.coordinates).length() > MN.DELTA)
        else:
            self.alive = ((not self.printedpos) and (self.coordinates))

        #if aCoord and bCoord:
        #    print self.name, aCoord, bCoord, self.alive

        if (A == ship_status.ONLINE) :
            if (B == ship_status.ONLINE) :
                res = message.PASS
            elif (B == ship_status.OFFLINE) or (B == ship_status.INDEADEND) :
                res = message.GOODBYE

        elif (A == ship_status.OFFLINE) :
            if (B == ship_status.ONLINE) :
                res = message.HELLO
            elif (B == ship_status.OFFLINE) or (B == ship_status.INDEADEND) :
                res = message.PASS

        elif (A == ship_status.INDEADEND) :
            if (B == ship_status.ONLINE) :
                res = message.HELLO
            elif (B == ship_status.OFFLINE) :
                res = message.GOODBYE
            elif (B == ship_status.INDEADEND) :
                res = message.PASS

        return message.reverse_mapping[res]

    def update(self, data):
        if data:
            if (self.coordinates) and (self.speed > MN.STOP) :
                if not (self.lastpos.count(self.coordinates)) :
                    self.lastpos.append(self.coordinates)

            if len(self.lastpos)>MN.LASTPOSLEN:
                self.lastpos.pop(0)# = self.lastpos[-MN.LASTPOSLEN:]

            self.speed = data[0]
            self.course = data[1]
            self.coordinates = Coordinates(data[2][0], data[2][1])
            self.status = ship_status.ONLINE
        else:
            self.reset()
            status = ship_status.OFFLINE

    def update_from_ais(self):
        scrapper = Scrapper()
        data = scrapper.scrape_ship(self.name)
        return self.update(data)

    def __str__(self):
        if self.status == ship_status.ONLINE:
            res = "name: {0}; speed: {1}; course: {2}; coordinates: {3}; route: {4};".format(self.name, self.speed, self.course, self.coordinates, self.route)
        else:
            res = "name: {0}; ais status: {1}".format(self.name, self.ais_status())
        return res


    def ais_status(self):
        return ship_status.reverse_mapping[self.status]

    def angle (self, point):
        '''
        Easy use for Coordinates.angle()
        '''
        return self.coordinates.angle(self.course, point)

    def viewangle(self, point):
        return self.angle(point) < MN.VIEWANGLE

    def collinear(self, point):
        '''
        Easy use for Coordinates.collinear()
        '''
        return self.coordinates.collinear(self.course, point)

    def length(self, point):
        '''
        Easy use for Coordinates.length()
        '''
        return (self.coordinates - point).length()

    def deadend(self, zone):
        if self.status == ship_status.OFFLINE or not(self.status):
            return False

        if (zone.area.is_inside(self.coordinates)):
            if (self.speed < MN.STOP) or (self.length(zone.mark) < MN.DEADEND) (self.viewangle(zone.mark)):
                self.status = ship_status.INDEADEND
                self.reset()
                return True

        return False