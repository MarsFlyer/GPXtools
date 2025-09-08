# Read a GPX and find the significant time gaps
# Show the date & time (when stopped), duration and location (lat,lon can be pasted into Google maps' search).
# Also show any distance gaps e.g. when you forget to restart your tracking after a stop.
# Use geopy to reverse lookup the location of the stop using the OpenStreetMap's Nominatim.
# New check for low speed stops, where the track wasn't paused.
# TODO get seconds from an argument - particularly useful for short rides where you want to know about shorter stops.
# TODO combine stops where there's no significant distance between them.

import gpxpy.gpx
import datetime
import sys
from geopy.geocoders import Nominatim
from ratelimit import limits, sleep_and_retry

# Settings
secondsGap = 120 # seconds
speedLow = 0.5 # metres per second. 1 m/s = 3.6 km/s
distanceGap = 100 # metres
locationGap = 500 # metres
unitsDivider = 1609 # metres per mile
units = 'miles'
url = 'https://www.google.com/maps/place/'

# Get GPX file name and option from arguments
file = sys.argv[1]
getLocations = True
if  len(sys.argv) > 2:
    if sys.argv[2].lower() in ("false", "no", "0"):
        getLocations = False

# This throttles rqeuests to this the free service. Max of once every 2 seconds.
@sleep_and_retry
@limits(calls=1, period=2)
def getLocation(lat, lon):
    if getLocations == False:
        return ''
    try:
        # print('Reverse lookup' + str(lat) + ',' + str(lon))
        location = geolocator.reverse(str(lat) + ',' + str(lon))
    except Exception as e:
        # print('location not found')
        return 'not found ' + str(e)
    address = location.raw['address']
    # print(address)
    # print('')

    # Use a shortened address to remove unecessary detail e.g. exact address & country
    parts = []
    start = True
    more = True
    last = ''
    if start and 'road' in address:
        part = address['road']
        if part != last:
            parts.append(part)
        # start = False
        last = part
    if start and 'hamlet' in address:
        part = address['hamlet']
        if part != last:
            parts.append(part)
        # start = False
        last = part
    if more and 'village' in address:
        part = address['village']
        if part != last:
            parts.append(part)
        # more = False
        last = part
    if more and 'suburb' in address:
        part = address['suburb']
        if part != last:
            parts.append(part)
        more = False
        last = part
    if more and 'town' in address:
        part = address['town']
        if part != last:
            parts.append(part)
        more = False
        last = part
    if 'city_district' in address:
        part = address['city_district']
        if part != last:
            parts.append(part)
        more = False
        last = part
    if more and 'city' in address:
        part = address['city']
        if part != last:
            parts.append(part)
        more = False
        last = part
    if 'county' in address:
        parts.append(address['county'])
    name = ", ".join(parts)
    return name

# Initialize Nominatim API 
geolocator = Nominatim(user_agent="my_geopy_app")
# Test a location
# location = getLocation(52.108352,0.924454)
# print(location)
# exit()

# Get GPX file and parse it
gpx_file = open(file, 'r')
gpx = gpxpy.parse(gpx_file)
point_data = gpx.get_points_data()

i = -1
stopped = None
location = ''
speed = 0
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
                pointLast = point
                timeLast = point.time
                continue
            interval = timeThis - timeLast
            speed = point.speed_between(pointLast)
            # print('Interval: ',interval)
            if interval.seconds > secondsGap and speed > speedLow:
                if stopped == None:
                    stopped = interval
                else:
                    stopped += interval
                distance = point_data[i].distance_from_start
                if getLocations:
                    location = getLocation(pointLast.latitude, pointLast.longitude)
                if interval.seconds > 60:
                    stop = '{0} minutes'.format(int(interval.seconds/60))
                else:
                    stop = '{0} seconds'.format(int(interval.seconds))
                # Example: YYYY-MM-DD HH:MM:SS+HH:MM n minutes at 1.2 miles. Location: Village, Town, County https://www.google.com/maps/place/51.123456,-0.123456
                print('{0} {1} at {4:0.1f} {5}. Location: {6} {7}{2},{3}'.format(timeLast.astimezone(), stop, pointLast.latitude, pointLast.longitude, distance/unitsDivider, units, location, url))
                distanceLast = point_data[i-1].distance_from_start
                if distance - distanceLast > distanceGap:
                    location = '^'
                    if getLocations and (distance - distanceLast > locationGap):
                        location = getLocation(point.latitude, point.longitude)
                    print('Distance missed: {0:0.1f} {1} at lat,lon: {2},{3} location: {4}'.format((distance-distanceLast)/unitsDivider, units, point.latitude, point.longitude, location))
            # print('{0} speed {1}'.format(i, speed))
            pointLast = point
            if speed > speedLow:
                timeLast = point.time
            # else:
            #     print('{0} time {2} speed {1} last {3}'.format(i, speed, point.time, timeLast))
            # print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
            # if i > 10:
            #     break
    interval = (timeLast - timeFirst)
    print('End: {0} duration: {1} stopped: {2}'.format(timeLast.astimezone(), interval, stopped))
