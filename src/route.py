from area import Area
from pier import Pier
from ship import Ship
from magic_numbers import MN

class Route:
    '''
    A Route class
    '''
    def __init__(self, name, bay=None, piers=None) :
        self.name = name
        self.bay = bay
        self.piers = piers

    def __init__(self, parser, piers=None) :
        '''
        Parser (str, Area)
        '''
        self.name = parser[0]
        self.bay = parser[1]
        self.piers = piers

    def __str__(self):
        return "route: {0};".format(self.name)

    def verification(self, ship) :
        '''
        Checks Is the ship on the route
        '''
        if not self.bay.is_inside(ship.coordinates):
            return None
        else:
            count = 1

        if (ship.speed < MN.STOP):
            for pier in self.piers:
                if pier.area.is_inside(ship.coordinates):
                    return MN.TRUEPOS

        for point in ship.lastpos:
            count += self.bay.is_inside(point)

        return count

    def next(self, index, count = 1):
        return (index + count) % len(self.piers)

    def prev(self, index, count = 1):
        return (len(self.piers) + index - count) % len(self.piers)

    def destination(self, ship) :
        '''
        Returns pier destination route
        '''
        if not self.bay.is_inside(ship.coordinates):
            return None

        if (ship.speed < MN.STOP):
            x = [0, ship.lastpierindex] [ship.lastpierindex != None]
            for i in range(len(self.piers)):
                pier = self.piers[self.next(x,i)]
                if pier.area.is_inside(ship.coordinates):
                    ship.lastpierindex = self.next(x,i)
                    return pier

        if (ship.lastpierindex != None):
            if ship.viewangle(self.piers[self.next(ship.lastpierindex)].mark):
                return self.piers[self.next(ship.lastpierindex)]
            elif ((self.piers[ship.lastpierindex].mark - ship.coordinates).length() < MN.DELTA):
                return self.piers[self.next(ship.lastpierindex)]
            #elif ship.viewangle(self.piers[self.prev(ship.lastpierindex)].mark):
            #    return self.piers[ self.prev(ship.lastpierindex) ]
            #else:
            #    if (ship.collinear(self.piers[self.next(ship.lastpierindex)].mark)):
            #        ship.lastpierindex = self.next(ship.lastpierindex)
            #        return self.destination(ship)
                #elif (ship.collinear(self.piers[self.prev(ship.lastpierindex)].mark)):
                #    ship.lastpierindex = self.prev(ship.lastpierindex)
                #    return self.destination(ship)
                #return self.piers[(ship.lastpierindex + 1) % len(self.piers)]


        dest = ang = MN.MAX
        res = None#self.piers[0]#

        for pier in self.piers:
            foo = ship.angle(pier.mark)
            #print foo#, pier
            if foo < ang : #ship.viewangle(pier.mark) :
                #boo = ship.length(pier.mark)
                if (foo < ang):
                #if (boo < dest):
                    #dest = foo
                    ang = foo
                    res = pier

        return res