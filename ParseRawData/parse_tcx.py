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
        self.lst_hrData = self.allHRRateDim()
        self.lst_posData = self.allPositionDim()
        self.lst_altData = self.allAltitudeDim()
    
    ############################################ Private Methods ######################################
    # get HeartRateBpm each TrackPoint
    # !!sometimes for one Trackpoint may miss HRRate data
    def hr_values(self):
        return [int(x.text) for x in self.root.xpath('//ns:HeartRateBpm/ns:Value', namespaces={'ns': namespace})]
    
    # get Altitude Meters each TrackPoint
    def altitude_points(self):
        return [float(x) for x in self.root.xpath('//ns:AltitudeMeters', namespaces={'ns': namespace})]
    
    # get Timestamp each TrackPoint
    def time_values(self):
        return [x.text for x in self.root.xpath('//ns:Time', namespaces={'ns': namespace})]
    
    ######################################### Properties ##############################################
    # latitude of start point of workout
    @property
    def latitude(self):
        return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees.pyval
    
    # longitude of start point of workout
    @property
    def longitude(self):
        return self.activity.Lap.Track.Trackpoint.Position.LongitudeDegrees.pyval
    
    @property
    def activity_type(self):
        return self.activity.attrib['Sport'].lower()
    
    @property
    def start_time(self):
        """The first Trackpoint timestamp of first Lap"""
        return self.activity.Lap[0].Track.Trackpoint[0].Time.pyval
    
    @property
    def finish_time(self):
        """The last Trackpoint timestamp of last Lap"""
        return self.activity.Lap[-1].Track.Trackpoint[-1].Time.pyval
    
    @property
    def distance(self):
        # find all distance value at each Trackpoint
        # <DistanceMeters> is cumulative value
        lst_curDist = self.root.findall('.//ns:DistanceMeters', namespaces={'ns': namespace})
        if lst_curDist:
            # get the last distance value
            return int(lst_curDist[-1].pyval)
        return 0
    
    @property
    def distance_unit(self):
        return "meters"
    
    @property
    def calorie_unit(self):
        return "kcal"
    
    @property
    def duration(self):
        # return duration value in seconds
        """return sum of Duration for each lap"""
        total_duration_seconds = sum(lap.TotalTimeSeconds for lap in self.activity.Lap)
        m, s = divmod(total_duration_seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)
    
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
    
    # get all (time, distance, HRRate) tuple for each trackpoint
    def allHRRateDim(self):
        time_distance_HR = []
        activity = self.root.Activities.Activity
        for lap in activity.Lap:
            for track in lap.Track:
                for point in track.Trackpoint:
                    # timestamp
                    timestamp = point.Time.text
                    # cummulative distance
                    dist = point.DistanceMeters.pyval
                    # heart rate
                    has_HRAttr = hasattr(point,'HeartRateBpm')
                    if has_HRAttr:
                        heart = int(point.HeartRateBpm.Value)
                    else:
                        heart = None
                    
                    time_distance_HR.append((timestamp, dist, heart))
        return time_distance_HR

    # get all (time, distance, (latitude, longitude)) for each trackpoint
    def allPositionDim(self):
        time_distance_position = []
        activity = self.root.Activities.Activity
        for lap in activity.Lap:
            for track in lap.Track:
                for point in track.Trackpoint:
                    # timestamp
                    timestamp = point.Time.text
                    # cummulative distance
                    dist = point.DistanceMeters.pyval
                    # (latitude, longtitude)
                    lat = point.Position.LatitudeDegrees.pyval
                    lon = point.Position.LongitudeDegrees.pyval

                    time_distance_position.append((timestamp, dist, (lat, lon)))
        return time_distance_position

    # get all (time, distance, altitude) for each trackpoint
    def allAltitudeDim(self):
        time_distance_alt = []
        activity = self.root.Activities.Activity
        for lap in activity.Lap:
            for track in lap.Track:
                for point in track.Trackpoint:
                    # timestamp
                    timestamp = point.Time.text
                    # cummulative distance
                    dist = point.DistanceMeters.pyval

                    # altitude
                    alt = float(point.AltitudeMeters)

                    time_distance_alt.append((timestamp, dist, alt))
        return time_distance_alt
    
    # get all (time, distance, pace) for each trackpoint
    def allPaceSpeedDim(self):
        pass