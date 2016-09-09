# GPX (GPS eXchange Format) is a XML based file format for GPS track logs.
# I use gpx-py to parse gpx file
# From: https://github.com/tkrajina/gpxpy

import gpxpy
import matplotlib.pyplot as plt

# import time
# from lxml import objectify

# my parser
# import parse_gpx

gpx_file = open('./SampleData/run-20160624T055729.gpx', 'r')

def readgpx(file):
    gpx = gpxpy.parse(file)
    mv = gpx.get_moving_data()
    dat= {'moving_time':mv.moving_time,'stopped_time':mv.stopped_time,'moving_distance':mv.moving_distance,'stopped_distance':mv.stopped_distance,'max_speed':mv.max_speed}
    dat['total_duration']=(gpx.get_duration())
    dat['id']=str(gpx_file)
    updown=gpx.get_uphill_downhill()
    dat['uphill']=(updown.uphill)
    dat['downhill']=(updown.downhill)
    timebound=gpx.get_time_bounds()
    dat['start_time']=(timebound.start_time)
    dat['end_time']=(timebound.end_time)
    p=gpx.get_points_data()[0]
    # start point
    dat['lat']=p.point.latitude
    dat['lng']=p.point.longitude

    return dat

data = readgpx(gpx_file)
# gpx = parse_gpx.GpxParser('./SampleData/run-20160624T055729.gpx')


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

# pos = gpx.allPositionData