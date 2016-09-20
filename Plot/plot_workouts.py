# plot Altitude data
import sys
sys.path.append("..")

import ParseRawData.parse_tcx as pt
import matplotlib.pyplot as pp
import matplotlib.dates
import matplotlib as mpl
import numpy as np
from scipy import stats as st
import datetime

workout_raw_file = '../SampleData/run-20160624T055729.tcx'

workout = pt.TcxParser(workout_raw_file)

print "Activity Type: " + workout.activity_type
print "Duration: " + str(workout.duration)
print "Complete at: " + workout.finish_time
print "Distance: " + str(workout.distance)
print "Distance Unit: " + workout.distance_unit

def plot_alt_distance(workout):
    pp.figure()
    distArray = []
    altArray = []

    for item in workout.allAltitudeDim():
        _, dist, alt = item
        distArray.append(dist)
        altArray.append(alt)
    
    pp.plot(distArray, altArray)
    pp.show()

def plot_HR_distance(workout):
    pp.figure()
    distArray = []
    HRArray = []

    for item in workout.allHRRateDim():
        _, dist, hr = item
        distArray.append(dist)
        HRArray.append(hr)
    
    pp.plot(distArray, HRArray)
    pp.show()

plot_alt_distance(workout)
plot_HR_distance(workout)