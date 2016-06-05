#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

import os
from gps import *
import time
import threading
import random
import requests
import spidev

spi = spidev.SpiDev()
spi.max_speed_hz = 5000
spi.mode = 0b01
spi.open(bus, device)



BIN_ID = 2
DEBUG = True

gpsd = None  # seting the global variable

os.system('clear')  # clear the terminal (optional)



def getTeam():
    if DEBUG:
        return random.randint(1, 4)
    else:
        return spi.get(1)

def getPower():
    if DEBUG:
        return random.randint(1, 4)
    else:
        return spi.get(2)

def getPIR():
    if DEBUG:
        return random.randint(1, 4)
    else:
        return spi.get(3)

def getColour():
    if DEBUG:
        return random.randint(1, 4)
    else:
        return spi.get(4)

def getBinCap():
    if DEBUG:
        return random.randint(1, 4)
    else:
        return spi.get(5)

def getSolar():
    if DEBUG:
        return random.randint(1, 4)
    else:
        return spi.get(6)




class GpsPoller(threading.Thread):
    """
    gps poller running gps thread
    """
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd  # bring it in scope
        gpsd = gps(mode=WATCH_ENABLE)  # starting the stream of info
        self.current_value = None
        self.running = True  # setting the thread running to true

    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()  # this will continue to loop and grab EACH set of gpsd info to clear the buffer


if __name__ == '__main__':
    gpsp = GpsPoller()
    gpsp.start()# create the thread
    time_now = time.strftime("%c")
    time.sleep(2)
    lat = gpsd.fix.latitude
    lng = gpsd.fix.longitude
    print('latitude    ', gpsd.fix.latitude)
    print('longitude   ', gpsd.fix.longitude)


    bin_id = BIN_ID
    payload = {'points': [
        {
            'bin_id': bin_id,
            'lat': lat,
            'lng': lng,
            'time': time_now,
            'team': getTeam(),
            'powerLevel': getPower(),
            'pirValue': getPIR(),
            'colourValue': getColour(),
            'binCapacity': getBinCap(),
            'solarValue': getSolar()
        }
    ]


    }
    gpsp.running = False
    gpsp.join()
    print(payload)
    r = requests.post('https://binmonsters.xyz/bins', json=payload)
    print(r.status_code)
    print(r.text)




    print("Done.\nExiting.")