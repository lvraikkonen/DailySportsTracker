# GPX (GPS eXchange Format) is a XML based file format for GPS track logs.
# I use gpx-py to parse gpx file
# From: https://github.com/tkrajina/gpxpy

import gpxpy
import matplotlib.pyplot as plt

import time
from lxml import objectify

# my parser
import parse_gpx

# gpx_file = open('./SampleData/run-20160624T055729.gpx', 'r')
# gpx = gpxpy.parse(gpx_file)

gpx = parse_gpx.GpxParser('./SampleData/run-20160624T055729.gpx')


# tree = objectify.parse('./SampleData/run-20160624T055729.gpx')
# root = tree.getroot()
# track = root.trk
# positions = {}
# for t in track:
#     for seg in t.trkseg:

#         timestamp = seg.trkpt.time.text
#         lat = seg.trkpt.attrib['lat']
#         lon = seg.trkpt.attrib['lon']
#         alt = float(seg.trkpt.ele.pyval)

#         positions[timestamp] = (lat,lon, alt)

pos = gpx.allPositionData