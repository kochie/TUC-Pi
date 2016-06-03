#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

import os
from gps import *
from time import *
import time
import threading
import json
import random
import requests

gpsd = None  # seting the global variable

os.system('clear')  # clear the terminal (optional)

def getCap(debug=True):
    if debug:
        return random.random()


def getPow(debug=True):
    if debug:
        return random.random()



class GpsPoller(threading.Thread):
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
    data = {
        'capacity': getCap(),
        'power': getPow(),
        'team': {
            'red': 1,
            'green': 2,
            'blue': 3,
            'yellow': 4
        }
    }
    bin_id = 2
    payload = {'points':[
        {
            'bin_id': bin_id,
            'data': data,
            'lat': lat,
            'lng': lng,
            'time': time_now
        }
    ]


    }
    gpsp.running = False
    gpsp.join()
    r = requests.post('https://binmonsters.xyz/bins', json=payload)
    print(r.status_code)
    print(r.text)




    print("Done.\nExiting.")