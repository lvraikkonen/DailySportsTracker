# Training Center XML (TCX) is a data exchange format introduced in 2007 as part of Garmin's Training Center product.
# TCX provides standards for 
#     transferring heart rate
#   , running cadence
#   , bicycle cadence
#   , calories in the detailed track.
# It also provides summary data in the form of laps

import time
from lxml import objectify

namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'

class TcxParser:

    def __init__(self, tcx_file):
        tree = objectify.parse(tcx_file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity
    
    ############################################ Private Methods ######################################
    # get HeartRateBpm each TrackPoint
    def hr_values(self):
        return [int(x.text) for x in self.root.xpath('//ns:HeartRateBpm/ns:Value', namespaces={'ns': namespace})]
    
    # get Altitude Meters each TrackPoint
    def altitude_points(self):
        return [float(x) for x in self.root.xpath('//ns:AltitudeMeters', namespaces={'ns': namespace})]
    
    # get Timestamp each TrackPoint
    def time_values(self):
        return [x.text for x in self.root.xpath('//ns:Time', namespaces={'ns': namespace})]
    
    ######################################### Properties ##############################################
    @property
    def latitude(self):
        return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees.pyval
    
    @property
    def longitude(self):
        return self.activity.Lap.Track.Trackpoint.Position.LongitudeDegrees.pyval
    
    @property
    def activity_type(self):
        return self.activity.attrib['Sport'].lower()
    
    @property
    def finish_time(self):
        """The last Trackpoint timestamp of last Lap"""
        return self.activity.Lap[-1].Track.Trackpoint[-1].Time.pyval
    
    @property
    def distance(self):
        # find all distance value at each Trackpoint
        # <DistanceMeters> is cumulative value
        lst_curDist = self.root.findall('.//ns:DistanceMeters')
        if lst_curDist:
            # get the last distance value
            return lst_curDist[-1]
        return 0
    
    @property
    def distance_unit(self):
        return "meters"
    
    @property
    def duration(self):
        # return duration value in seconds
        """return sum of Duration for each lap"""
        return sum(lap.TotalTimeSeconds for lap in self.activity.Lap)
    
    @property
    def calories(self):
        """return sum of Calories for each lap"""
        return sum(lap.Calories for lap in self.activity.Lap)
    
    @property
    def hr_avg(self):
        """Average heart rate of the workout"""
        hr_data = self.hr_values()
        return sum(hr_data)/len(hr_data)

    @property
    def hr_max(self):
        """Minimum heart rate of the workout"""
        return max(self.hr_values())

    @property
    def hr_min(self):
        """Minimum heart rate of the workout"""
        return min(self.hr_values())

    @property
    def pace(self):
        """Average pace (mm:ss/km for the workout"""
        secs_per_km = self.duration/(self.distance/1000)
        return time.strftime('%M:%S', time.gmtime(secs_per_km))

    @property
    def altitude_avg(self):
        """Average altitude for the workout"""
        altitude_data = self.altitude_points()
        return sum(altitude_data)/len(altitude_data)

    @property
    def altitude_max(self):
        """Max altitude for the workout"""
        altitude_data = self.altitude_points()
        return max(altitude_data)

    @property
    def altitude_min(self):
        """Min altitude for the workout"""
        altitude_data = self.altitude_points()
        return min(altitude_data)

    @property
    def ascent(self):
        """Returns ascent of workout in meters"""
        total_ascent = 0.0
        altitude_data = self.altitude_points()
        for i in range(len(altitude_data) - 1):
            diff = altitude_data[i+1] - altitude_data[i]
            if diff > 0.0:
                total_ascent += diff
        return total_ascent

    @property
    def descent(self):
        """Returns descent of workout in meters"""
        total_descent = 0.0
        altitude_data = self.altitude_points()
        for i in range(len(altitude_data) - 1):
            diff = altitude_data[i+1] - altitude_data[i]
            if diff < 0.0:
                total_descent += abs(diff)
        return total_descent