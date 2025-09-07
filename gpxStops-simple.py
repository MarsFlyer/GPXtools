# Read a GPX and find the significant time gaps
# Show the date & time (when stopped), duration and location (lat,lon can be pasted into Google maps' search).

import gpxpy.gpx
import datetime
import sys

# Settings
secondsGap = 120 # seconds
distanceGap = 100 # metres
unitsDivider = 1609 # metres per mile
units = 'miles'

# Get GPX file name and option from arguments
file = '../original/2019-07 Dunwich_Dynamo.gpx'

# Get GPX file and parse it
gpx_file = open(file, 'r')
gpx = gpxpy.parse(gpx_file)
point_data = gpx.get_points_data()

i = -1
stopped = None
for track in gpx.tracks:
    for segment in track.segments:
        timeLast = None
        for point in segment.points:
            i += 1
            if i==0:
                timeFirst = point.time
                print('Start: {0}'.format(point.time.astimezone()))
            timeThis = point.time
            if timeLast == None:
                timeLast = point.time
                continue
            interval = timeThis - timeLast
            # print('Interval: ',interval)
            if interval.seconds > secondsGap:
                if stopped == None:
                    stopped = interval
                else:
                    stopped += interval
                distance = point_data[i].distance_from_start
                print('{0} {1} minutes at {4:0.1f} {5}. lat,lon: {2},{3}'.format(timeLast.astimezone(), int(interval.seconds/60), pointLast.latitude, pointLast.longitude, distance/unitsDivider, units))
                distanceLast = point_data[i-1].distance_from_start
                if distance - distanceLast > distanceGap:
                    print('Distance missed: {0:0.1f} {1} at lat,lon: {2},{3}'.format((distance-distanceLast)/unitsDivider, units, point.latitude, point.longitude))
            pointLast= point
            timeLast = point.time
            # print('Time {0} at ({1},{2})'.format(point.time, point.latitude, point.longitude))
            # if i > 10:
            #     break
    interval = (timeLast - timeFirst)
    print('End: {0} duration: {1} stopped: {2}'.format(timeLast.astimezone(), interval, stopped))
