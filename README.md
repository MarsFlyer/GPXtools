# GPX Tools by MarsFlyer

##  gpxStops
I wanted to see how long and where I had stopped, particularly on long rides, but couldn't find any way to do that using the usual websites or GPX tools.

- The gpxpy library is used to read the track, the code looks for stops longer than a set number of seconds, and gaps in the track greater than a set number of metres.

- The geopy library is used to find a place name for the lattitude & longtitude. As this can be long and/or repetitive, only distinguishing elements of the place name are used. You may want to adjust these rules depending on naming conventions in your country.

- The ratelimit library is used to throttle calls to the openOpenStreetMap's Geocoding reverse lookup service.

usage:
```
python3 gpxStops.py '../Original/TRACK.gpx'
```

example output:

This is from the classic overnight ride from London to the Suffolk coast.
```
python3 gpxStops.py '../Original/2025-07 Dunwich_Dynamo.gpx'
Start: 2025-07-12 19:24:17+01:00
2025-07-12 21:21:59+01:00 24 minutes at 23.4 miles. lat,lon: 51.737576,0.2649 location: Clatterford End, Fyfield, Essex
2025-07-12 23:21:39+01:00 18 minutes at 44.1 miles. lat,lon: 51.968327,0.450285 location: Bridge Street, Finchingfield, Essex
2025-07-13 00:51:58+01:00 31 minutes at 62.5 miles. lat,lon: 52.03899,0.726502 location: Gregory Street, Sudbury, Suffolk
Distance missed: 3.2 miles at lat,lon: 52.067115,0.787675 location: B1115, Great Waldingfield, Babergh, Suffolk
2025-07-13 02:39:19+01:00 26 minutes at 77.7 miles. lat,lon: 52.150351,1.059195 location: Coddenham Road, Mid Suffolk, Suffolk
2025-07-13 05:33:06+01:00 22 minutes at 107.7 miles. lat,lon: 52.270813,1.567975 location: Westleton, East Suffolk, Suffolk
End: 2025-07-13 06:10:43+01:00 duration: 10:46:26 stopped: 2:02:21
```

## Virtual python config:
```
python3 -m venv ../venv
source ../venv/bin/activate
which pip
python3 -m pip install gpxpy
python3 -m pip install geopy
python3 -m pip install ratelimit
pip list
deactivate
```