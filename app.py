# -*- coding: utf-8 -*-

import serial
import time
import math
import json
import requests as r
from kalman import Kalman

URL = "https://cAUrbKXQ8qfg59UhwAMS8C4H2L4t5hbNlHdI0Qbu:javascript-key=seN49Lww6i0Wk6Am0hy4qwmfLWaBer9o0gfQXc5Q@api.parse.com/1/classes/Activity"
#PET_ID = '1E0822ACC5'
PET_ID = '1234FA01C5'
kf = Kalman(R=0.01, Q=3)

def get_range(rssi):
    txPower = -59

    ratio_db = txPower - rssi
    ratio_linear = math.pow(10, ratio_db / 10)

    r = math.sqrt(ratio_linear)
    return r

def calculateDistance(rssi):
    txPower = -59

    if(rssi == 0):
        return -1.0

    ratio = rssi*1.0/txPower
    print "ratio is {}".format(ratio)
    if(ratio < 1.0):
        return math.pow(ratio, 10)
    else:
        distance = (0.89976)*math.pow(ratio,7.7095) + 0.111
        return distance


def setup():
    global s
    global s2
    s = serial.Serial("/dev/ttyS2", 9600, timeout=1)
    s2 = serial.Serial("/dev/ttyS0", 9600)
    s.write("AT+ROLE1")
    time.sleep(1)
    s.write("AT+IMME1")
    time.sleep(1)
    print "Setup complete"

def loop():
    s.write("AT+DISI?")
    result = s.read(8)
    weight = s2.readline()
    try:
        weight = abs(float(weight))
    except:
        print("Invalid wright received")
    print result
    print weight

    if result == "OK+DISC:":
        beacon = s.read(70)
        rssi = int(beacon.split(":")[-1])
        pet_id = beacon.split(":")[2]
        # Measured 1m rssi is the last two bytes of p3
        #txPower = beacon.split(":")[-3][-2]
        print beacon
        print "RSSI is {}".format(int(rssi))
        distance = calculateDistance(rssi)
        distance2 = get_range(rssi)
        if distance < 5 and pet_id == PET_ID:
            print "posting to Parse"
	    payload = {
                   "weight": float(weight),
                   "pet": {
                           "__type": "Pointer",
                           "className": "Pet",
                           "objectId": pet_id 
                   },
                   "food": {
                           "__type": "Pointer",
                           "className": "Food",
                           "objectId": "zU2FF9wWs9"
                   }
            }
            print("posting {}".format(payload))
            res = r.post(URL, data=json.dumps(payload))
            print res.text
        print "Distance1 is {}".format(distance)
        print "Distance2 is {}".format(distance2)

    time.sleep(1)

if __name__ == '__main__':
    setup()
    while True:
        loop()
