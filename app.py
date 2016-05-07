# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

TODO:
    1. Add Kalman Filter and Moving Average to the rssi
    2. Transmit values to backend (HTTP or WebSocket?)


"""

import serial
import time
import math
from kalman import Kalman

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
    s = serial.Serial("/dev/ttyS2", 9600)
    s.write("AT+ROLE1")
    time.sleep(1)
    s.write("AT+IMME1")
    time.sleep(1)
    print "Setup complete"

def loop():
    s.write("AT+DISI?")
    result = s.read(8)
    print result
    if result == "OK+DISC:":
        beacon = s.read(70)
        rssi = int(beacon.split(":")[-1])
        # Measured 1m rssi is the last two bytes of p3
        #txPower = beacon.split(":")[-3][-2]
        print beacon
        print "RSSI is {}".format(int(rssi))
        distance = calculateDistance(rssi)
        distance2 = get_range(rssi)
        print "Distance1 is {}".format(distance)
        print "Distance2 is {}".format(distance2)

    time.sleep(1)

if __name__ == '__main__':
    setup()
    while True:
        loop()
