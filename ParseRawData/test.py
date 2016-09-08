from xml.etree.ElementTree import fromstring
from time import strptime, strftime
import time
from lxml import objectify
import sys
import re

namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'

def parsetcx(file):
    """
    parsetcx
    parses tcx data, returning a list of all Trackpoints where each
    point is a tuple of 
      (activity, lap, timestamp, seconds, lat, long, alt, dist, heart, cad)
    xml is a string of tcx data
    """
    tree = objectify.parse(file)
    root = tree.getroot()
    activity = root.Activities.Activity

    lapnum=1
    points=[]
    activity_type = activity.attrib['Sport'].lower()

    for lap in activity.Lap:
        for point in lap.Track.Trackpoint:

            # timestamp
            timestamp = point.Time.text

            # cummulative distance
            dist = point.DistanceMeters.pyval
                
            # latitude and longitude
            
            lat = point.Position.LatitudeDegrees.pyval
            lon = point.Position.LongitudeDegrees.pyval

            # altitude
            alt = float(point.AltitudeMeters)
            
            # heart rate
            has_HRData = hasattr(point,'HeartRateBpm')
            if has_HRData:
                heart = int(point.HeartRateBpm.Value)
            else:
                heart = None


            # append to list of points
            points.append((activity_type,
                           lapnum,
                           timestamp, 
                           lat,
                           lon,
                           alt,
                           dist,
                           heart))
            print timestamp

        # next lap
        lapnum+=1

    return points

data = './SampleData/run-20160624T055729.tcx'

istream = open('./SampleData/run-20160624T055729.tcx','r')

# read xml contents
points = parsetcx(istream)