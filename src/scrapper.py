import urllib2
from bs4 import BeautifulSoup
import re

from coordinates import Coordinates

class Scrapper:
    '''
    Scrapper class.
    '''
    def __init__(self):
        pass

    def scrape_ship(self, ship_name):
        '''
        Scrape ship data from AIS.
        return ( speed, course, (latitude, longitude) )
        if error occured return None
        '''
        res = None
        search_name = self._get_search_name(ship_name)
        url = r"http://www.marinetraffic.com/ais/index/ships/range/port_id:883/ship_type:6/shipname:{0}".format(search_name)
        try:
            soup = BeautifulSoup(urllib2.urlopen(url).read())
            row = soup.find("a",class_="data",text=ship_name).find_parent("tr").find_all("td")
        except (AttributeError, urllib2.URLError):
            row = None
        if row != None:
            res = self._get_data(row)
        return res

    def scrape_all_ships(self, ship_names):
        # TODO: Optimize parsing to reduce the number of processed items
        '''
        Scrape ships from array ship_name.
        return hash { name1 : (speed, course, (latitude, longitude) ), ...}
        if error occured while procssing http connection or html parsing return empty hash.
        if error occured while processing ship, than ship is not included in the result.
        '''
        url = r"http://www.marinetraffic.com/ais/index/ships/range/port_id:883/ship_type:6/per_page:0"
        data = []
        res = {}
        
        #for name in ship_names:
        #    res[name] = None

        try:
            soup = BeautifulSoup(urllib2.urlopen(url).read())
            raw_data = soup.find_all("a")
            for row in raw_data:
                if row.text in ship_names:
                    data.append( (row.text.encode("UTF-8","ignore"), row.find_parent("tr").find_all("td") ) )
        except :#(AttributeError, urllib2.URLError):
            data = None
        if data != None:
            for row in data:
                #print row[1][3]
                coord = self._get_data(row[1])
                if coord != None:
                    res[row[0]] = coord
        return res

    def _get_search_name(self, ship_name):
        '''
        Format ship name for the search.
        return string
        '''
        return '+'.join( ship_name.split(' ') )

    def _get_data(self, row):
        '''
        Get data from raw data row.
        row is <tr> element from website wraped with bs4.
        return ( speed, course, (latitude, longitude) )
        if error occured return none
        '''
        res = None
        try:
            raw_speed = row[7].find("span").encode("UTF-8")
            pattern = re.compile(r"[0-9\.]+")
            speed = float(pattern.search(raw_speed).group(0))

            raw_course = row[3].find("div").encode("UTF-8")
            pattern = re.compile(r'rotate\(([0-9]+)deg\)')
            course = float(pattern.search(raw_course).group(1))
            #print course
            #raw_input()

            raw_position = row[9].find("a")["href"]
            pattern = re.compile(r"centerx:([0-9\.]+)/centery:([0-9\.]+)")
            m = pattern.search(raw_position)
            longitude = float(m.group(1))
            latitude = float(m.group(2))

            res = ( speed, course, (latitude, longitude) )
            #print speed, course, latitude, longitude
            #raw_input()
        except (AttributeError):
            res = None
        finally:
            return res
