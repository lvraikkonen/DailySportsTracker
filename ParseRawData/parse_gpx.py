# GPX (GPS eXchange Format) is a XML based file format for GPS track logs.

import time
from lxml import objectify

class GpxParser:

    def __init__(self, gpx_file):
        tree = objectify.parse(gpx_file)
        self.root = tree.getroot()
        self.track = self.root.trk
        self.allPositionData = self.allPositionDim()
    
    def allPositionDim(self):
        positions = {}
        track = self.root.trk
        for t in track:
            for point in t.trkseg.trkpt:

                timestamp = point.time.text
                lat = point.attrib['lat']
                lon = point.attrib['lon']
                alt = float(point.ele.pyval)

                positions[timestamp] = (lat,lon, alt)
        return positions
