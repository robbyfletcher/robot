# Required Libraries
import threading
import serial
import numpy as np
# import astar

# Visualization Libraries
from bokeh.client import push_session
from bokeh.plotting import figure, curdoc

# Testing Libraries
import time
import random
import sys

print("Initializing..")


MAP_SIZE_X = 3084
MAP_SIZE_Y = 6168

origin = [MAP_SIZE_X, MAP_SIZE_Y]
location = origin

viz = 0

if (len(sys.argv) > 1):
    viz = int(sys.argv[-1])

ser = serial.Serial('/dev/tty.usbmodem1411', 9600)
time.sleep(1)

robotMap = np.zeros(shape=(MAP_SIZE_X * 2, MAP_SIZE_Y * 2))

trans = [[-1, -.7071, 0, .7071, 1], [ 0,  .7071, 1, .7071, 0]]

if (viz == 1):
    x = []
    y = []

    p = figure()
    c = p.circle(x, y, size=5, color="red", alpha=0.1)
    o = p.circle(origin[0], origin[1], size=25, color="purple")

    # open a session to keep our local document in sync with server
    session = push_session(curdoc())


def ultrasonic():
    ser.write(b'n')
    while (ser.inWaiting() == 0):
        continue
    s = ser.readline()
    if (viz == 0):
        print(s)
    s = s[1:-3].split('|')

    obstacles = []
    for i in range(5):
        obstacles.append([int(location[0] + int(s[i]) * trans[0][i]),
                          int(location[1] + int(s[i]) * trans[1][i])])

    for i in range(5):
        robotMap[obstacles[i][0]][obstacles[i][1]] += 1
        if (viz == 1):
            c.data_source.data["x"] = c.data_source.data["x"] + [obstacles[i][0]]
            c.data_source.data["y"] = c.data_source.data["y"] + [obstacles[i][1]]

    if (viz == 2):
        print(robotMap)
        print(chr(27) + "[2J")

# def camera():

print("Ready to go!")

if (viz == 1):
    curdoc().add_periodic_callback(ultrasonic, 5000)
    #
    session.show() # open the document in a browser
    #
    session.loop_until_closed() # run forever

while(1):
    ultrasonic()
