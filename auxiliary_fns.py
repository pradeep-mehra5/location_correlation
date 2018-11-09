from math import radians, cos, sin, asin , sqrt
import datetime


#function to calculate distance between two points represented
# by their coordinates
def getDistance(long1 , lat1 ,long2, lat2):
    E_RADIUS = 6371000
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    delta_long = long2 - long1
    delta_lat = lat2 - lat1
    a = (sin(delta_lat/2) ** 2) + cos(lat1) * cos(lat2)* sin(delta_long/2) ** 2
    c = 2 * asin(sqrt(a))
    distance = E_RADIUS * c
    return distance


#function to calculate coordinates of the stay point as a
#  mean of the coordinates of gps points in the stay point
def getMeanCoordinates(gpsPoints):
    lon,lat = 0.0,0.0
    num_of_points = len(gpsPoints)
    for point in gpsPoints:
        fields = point.rstrip().split(',')
        lon += float(fields[0])
        lat += float(fields[1])
    return (lon/num_of_points , lat/num_of_points)


#function to get location , i.e. mean point of a cluster of stay points
def getLocationFromSPs(cluster):
    lon,lat = 0.0,0.0
    num_of_points = len(cluster)
    for point in cluster:
        lon += point[0]
        lat += point[1]
    return (lon/num_of_points , lat/num_of_points)

#function to get the timestamp from datetime
def getTimeStamp(dtime):
    date,time = dtime.split(',')
    yyyy,mm,dd = list(map(int,date.split('-')))
    hours,min,secs = list((map(int,time.split(':'))))
    t = datetime.datetime()
    return t.timestamp(yyyy,mm,dd,hours,min,secs)