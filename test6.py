#=============================================================
from src import *
#-------------------------------------------------------------
import time
from time import strftime
from random import randint
import sys
#=============================================================
Scrap = Scrapper()
Xml = XmlParser()
Tweet = Twitter()
#=============================================================

#=============================================================
#--------------------   S T A R T   --------------------------
#-------------------------------------------------------------
def start():
    routes = [
    Route(Xml.parse("Bay\\Gorod - Severnaja.kml")),
    Route(Xml.parse("Bay\\Artbuhta - Severnaja.kml")),
    Route(Xml.parse("Bay\\Artbuhta - Radiogorka.kml")),
    Route(Xml.parse("Bay\\Gorod - Gollandija - Inkerman.kml")),
    Route(Xml.parse("Bay\\Gorod - Avlita.kml"))
    ]

    caters = {}
    Caters = []

    for name in open("ship.list", "r").readlines():
        Caters.append(Ship(name.split("/")))
        caters[name.split("/")[0]] = False

    Piers = {}
    for name in open("pier.list", "r").readlines():
        p  = name.split("/")
        Piers[unicode(p[0], "UTF-8")] = unicode(p[1], "UTF-8")

    A1 = Pier(Xml.parse_pier("Bay\\Grafskaja pristan.kml"));
    A2 = Pier(Xml.parse_pier("Bay\\Severnaja kater.kml"));

    B1 = Pier(Xml.parse_pier("Bay\\Art buhta parom.kml"));
    B2 = Pier(Xml.parse_pier("Bay\\Severnaja parom.kml"));

    C1 = Pier(Xml.parse_pier("Bay\\Art buhta kater.kml"));
    C2 = Pier(Xml.parse_pier("Bay\\Radiogorka.kml"));

    D1 = Pier(Xml.parse_pier("Bay\\Pirs u porta.kml"));
    D2 = Pier(Xml.parse_pier("Bay\\Apolonovka.kml"));
    D3 = Pier(Xml.parse_pier("Bay\\Gollandija.kml"));
    D4 = Pier(Xml.parse_pier("Bay\\Ugolnaja.kml"));
    D5 = Pier(Xml.parse_pier("Bay\\Inkerman - 1.kml"));
    D6 = Pier(Xml.parse_pier("Bay\\Inkerman - 2.kml"));

    E1 = D1
    E2 = D2
    E3 = Pier(Xml.parse_pier("Bay\\Avlita.kml"));

    DeadEnd = Pier(Xml.parse_pier("Bay\\Dead end.kml"));

    routes[0].piers = [A1, A2]
    routes[1].piers = [B1, B2]
    routes[2].piers = [C1, C2]
    routes[3].piers = [D1, D2, D3, D4, D5, D6, D4, D3, D2]
    routes[4].piers = [E1, E2, E3, E2]

    return routes, DeadEnd, caters, Caters, Piers
#=============================================================

#=============================================================
#------------------   U P D A T E   --------------------------
#-------------------------------------------------------------
def upd(count = 1) :
    global arrived
    global departed
    for i in range(count):
        data = Scrap.scrape_all_ships(caters)
        if data:
            for cater in Caters :
                if cater.name in data:
                    d = data[cater.name]
                else:
                    d = None
                msg = cater.msgupdate(d, DeadEnd)
                if (msg != "PASS") :
                    Tweet.post(Xml.getmsg(msg).format(cater.nick))
                    print cater
                    if (msg == "HELLO") :
                        caters[cater.name] = True
                        arrived += 1
                    if (msg == "GOODBYE") :
                        caters[cater.name] = True
                        departed += 1

#=============================================================

#=============================================================
#---------------   W H A T  R O U T E   ----------------------
#-------------------------------------------------------------
def whatroute():
    for cater in Caters:
        if (cater.status == ship_status.ONLINE) :
            
#           if (cater.deadend(DeadEnd)):
#               continue

            counter = []
            for route in routes:
                counter.append(route.verification(cater))
            maxpos = max(counter)
            
            if (not maxpos):
                cater.route = None
                continue

            if (cater.route == maxpos):
                continue
            
            cater.route = counter.index(maxpos)
#=============================================================

#=============================================================
#------------   S E N D   M E S S A G E S  -------------------
#-------------------------------------------------------------
def sendmsg():
    suwrs()
    
    size = len(Caters)
    index = range(size)
    for i in range(size):
        j = randint(i, size - 1)
        index[i], index[j] = index[j], index[i]

    for i in range(size):
        cater = Caters[index[i]]

        if (cater.status != ship_status.ONLINE) :
            continue

        print cater
        #for key in Piers:
        #    print key, Piers[key]
                
        if (cater.route != None) :
            route = routes[cater.route]
            msg = cater.msg()
            if (msg != "PASS") :
                pier = route.destination(cater)
                if (pier != None):
                    pier = pier.name
                else:
                    pier = MN.UNKNOWN
                Tweet.post(Xml.getmsg(msg).format(cater.nick, Piers[pier], route.name))

            if (msg == "UNDERWAY") :
                caters[cater.name] = True

            suwrs()
#=============================================================

#=============================================================
#---------------------  S L E E P  ---------------------------
#-------------------------------------------------------------
def sleep():
    #return
    time.sleep (MN.DELAY) #MN.DELAY min delay
#=============================================================

#=============================================================
#---------------------  S U W R S  ---------------------------
# --- sleep  to   delay --------------------------------------
# --- update  positions --------------------------------------
# --- route determinate --------------------------------------
# --- statistic   print --------------------------------------
#-------------------------------------------------------------
def suwrs():
    sleep()
    upd()
    whatroute()
    statistic()
#=============================================================

#=============================================================
#-----------------  S T A T I S T I C  -----------------------
#-------------------------------------------------------------
def statistic():
    global stat
    global arrived
    global departed

    if ( abs(time.localtime().tm_hour - stat) < MN.STAT) or (time.localtime().tm_min > MN.STAT2):
        return

    moored = 0
    underway = 0
    online = 0
    dead = 0

    underwayall = 0

    for cater in caters:
        underwayall += caters[cater]
        caters[cater] = False

    for cater in Caters:
        if (cater.status == ship_status.INDEADEND) :
            dead += 1

        if (cater.status == ship_status.ONLINE) :
            online += 1
            if (cater.speed < MN.STOP) :
                moored += 1
                print "MOORED:", cater
            else :
                underway += 1
                print "UNDERWAY:", cater

    msg = "STAT"
    Tweet.post(Xml.getmsg(msg).format(online, underway, moored, arrived, departed, underwayall, strftime("%d/%m/%y %H:%M", time.localtime()), "\n"))

    stat = time.localtime().tm_hour
    arrived = departed = 0
#=============================================================

routes, DeadEnd, caters, Caters, Piers = start()

#from src.coordinates import Coordinates
#A = Coordinates(44.617080, 33.528040)
#B = Coordinates(44.617467, 33.526974)
#C = Coordinates(44.617290, 33.529030)

#print A - B
#print B - A
#0.00113407451254

#a=(A-B).length()
#b=(B-C).length()

#print a
#print b
#print b-a
#for i in range(5):
#while True:
#   sendmsg()

stat = time.localtime().tm_hour# - 1
arrived = departed = 0
#sendmsg()

while True:
    try:
        print strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        sendmsg()
    except(KeyboardInterrupt):
        sys.exit()
    except Exception as e:
        print "Error:", e.message