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

	caters = []
	Caters = []

	for name in open("ship.list", "r").readlines():
		Caters.append(Ship(name.split("/")))
		caters.append(name.split("/")[0])

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

	return routes, DeadEnd, caters, Caters
#=============================================================

#=============================================================
#------------------   U P D A T E   --------------------------
#-------------------------------------------------------------
def upd(count = 1) :
	for i in range(count):
		data = Scrap.scrape_all_ships(caters)
		if data:
			for cater in Caters :
				msg = cater.msgupdate(data[cater.name], DeadEnd)
				if (msg != "PASS") :
					Tweet.post(Xml.getmsg(msg).format(cater.nick))

#=============================================================

#=============================================================
#---------------   W H A T  R O U T E   ----------------------
#-------------------------------------------------------------
def whatroute():
	for cater in Caters:
		if (cater.status == ship_status.ONLINE) :
			
#			if (cater.deadend(DeadEnd)):
#				continue

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

	size = len(Caters)
	index = range(size)
	for i in range(size):
		j = randint(i, size - 1)
		index[i], index[j] = index[j], index[i]

	for i in range(size):
		cater = Caters[index[i]]
		if (cater.status != ship_status.ONLINE) :
			continue
		
		if (cater.route != None) :
			route = routes[cater.route]
			msg = cater.msg()
			if (msg != "PASS") :
				pier = route.destination(cater)
				if (pier != None):
					pier = pier.name
				else:
					pier = MN.UNKNOWN
				Tweet.post(Xml.getmsg(msg).format(cater.nick, pier, route.name))

		upd()
		whatroute()
		sleep()
#=============================================================

#=============================================================
#---------------------  S L E E P  ---------------------------
#-------------------------------------------------------------
def sleep():
	time.sleep (MN.DELAY) #MN.DELAY min delay
#=============================================================

routes, DeadEnd, caters, Caters = start()

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
while True:
	try:
		print strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
		upd()
		whatroute()
		sendmsg()
		sleep()
	except(KeyboardInterrupt):
		sys.exit()
	except:
		print "Error:", sys.exc_info()[0]