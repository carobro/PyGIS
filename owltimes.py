import gdal
import ogr
import os
import osr
import dateparser
import csv
import datetime
from Owl import Owl
from Track import Track
from Point import Point
from math import sin, cos, sqrt, atan2, radians

####---- CONFIG-------#####
owl_ids = ["1750", "1751", "1753", "1754", "1292", "3893", "3892", "3894", "3895", "3896","3897", "3899", "3898", "4043", "4044", "4045", "4046", "5158", "5159", "4846", "4848"]
#owl_ids = ["5158"]

driver = ogr.GetDriverByName('ESRI Shapefile')
analysis_dir = os.path.join('/home','eric','Documents','PyGIS','analysis')
csv_file = os.path.join(analysis_dir,'resultsStartBuffer.csv')

#### hour at when tracks shall be analysed
start_hour = 16
### distance in m with which the buffer shall be created
buffer_distance = 20

### idle time for the owls, after that time(in seconds) the owl is being marked as not hunting anymore 
### 600 seconds = 10 minutes 
idle_time = 1200
####---- CONFIG-------#####



### cut microseconds for readability
def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)

def calculateAverages(owl):

    avgDuration = getDurationAverage(owl.tracks)
    avgStart = getStartAverage(owl.tracks)
    avgEnd = getEndAverage(owl.tracks)

    return [avgDuration,avgStart,avgEnd]


# get averages of the duration of one owl
def getDurationAverage(tracks):

    avgTracks = tracks
    sum_duration = 0
    for track in avgTracks:
        sum_duration+=track.getDuration()
    avgDuration = sum_duration / len(avgTracks)
    avgDuration = datetime.timedelta(seconds=avgDuration)
    return chop_microseconds(avgDuration)

# get average start time of one owl
def getStartAverage(tracks):
    sumSeconds = 0 
    ## start average
    for track in tracks:
        hour = float(track.getStart().strftime("%H"))
        minutes = float(track.getStart().strftime("%M"))
        seconds = float(track.getStart().strftime("%S"))

        total_seconds_start = (hour * 60 * 60) + (minutes * 60) + seconds
        sumSeconds+=total_seconds_start

    avgStart = sumSeconds/len(tracks)
    avgStart = datetime.timedelta(seconds=avgStart)
    return chop_microseconds(avgStart)

# get average end time of one owl
def getEndAverage(tracks):
    sumSeconds = 0 
    for track in tracks:
        hour = float(track.getEnd().strftime("%H"))
        minutes = float(track.getEnd().strftime("%M"))
        seconds = float(track.getEnd().strftime("%S"))

        total_seconds_end = (hour * 60 * 60) + (minutes * 60) + seconds
        sumSeconds += total_seconds_end

    avgEnd = sumSeconds/len(tracks)
    avgEnd = datetime.timedelta(seconds = avgEnd) 

    return chop_microseconds(avgEnd) 

# divide the shapefile of one owl to individual hunting tracks
# owls hunt are active from dawn till early morning 
# with this criteria individual hunting days can be detected and seperated 
def divideIntoTracks(layer):

    owl_tracks = []
    start = None
    points = []

    for feat in layer:
        timestamp = dateparser.parse(feat.GetField('timestamp'))

        hour = float(timestamp.strftime("%H"))
        minute = float(timestamp.strftime("%M"))
        date = float(timestamp.strftime("%d"))
        p1 = Point([feat.GetField('lat'),feat.GetField('long')],timestamp)
        # if feat is after 9am
        if(hour > 9):
            # if no start is(i.e. beginning of the loop) set start of track
            if(not(start)):
                if(hour >= start_hour):
                    start = dateparser.parse(feat.GetField('timestamp'))
                    points.append(p1)
                    continue
                else:
                    continue
            # if feat is after 9am and one day after start: a new track begins
            # append owl_track to track collection and set a new start
            if(timestamp.date() == start.date()+datetime.timedelta(1)):
                t1 = Track(start, points)
                t1 = sortOutTrack(t1)
                owl_tracks.append(t1)
                # reset variables
                start = None
                points = []
                #start = dateparser.parse(feat.GetField('timestamp'))
                continue
        # if feat is on the same date and after the start add it to the track
        if(date == float(start.strftime("%d"))):
            points.append(p1)
            continue
        # if feat is before nine and one day after the start add it to the track
        if(float(timestamp.strftime("%H")) < 9):
            if(timestamp.date() == start.date()+datetime.timedelta(1)):
                points.append(p1)
                continue
    return owl_tracks

# Filter a track when a owl stopped hunting 
# 2 criteria apply for if an owl is active or not:
#           - has not moved for more than 20meters  for a duration of 20 minutes
# this threshold can be edited in the config variable part of this script above 
def sortOutTrack(track):

    endtime = None
    # set start position 

    # if no start and end are found take the whole track
    start = track.points[0]
    endIndex = len(track.points)-1
    startIndex = 0
    watching = False

    for index,point in enumerate(track.points):
        hour = float(point.time.strftime("%H"))
        ### track has to end somewhere in this time frame
        if(not(hour>0 and hour<6)):
            continue
        if(getDistance(start,point) < buffer_distance):
            if(watching):
                duration = point.time - start.time
                duration = duration.total_seconds()
                if(duration>idle_time):
                #    print("End of hunting found at %s" % point.time)
                    endIndex = index
                    start = track.points[0]
                    watching = False
                    break
                # else:
        # print("found point inside 10m radius; continue watching")
            else:
                # print("start watching")
                watching = True
                continue
        else:
            if(watching):
                #print("covered more than 10m; aborting watching")
                start = point
                watching = False
    

    for index,point in enumerate(track.points):
        hour = float(point.time.strftime("%H"))
        #print("Now looking at point: %s" % point.time)
        if(not(hour>16 and hour<21)):
            continue
        if(getDistance(start,point) > buffer_distance):
            startIndex = index
            print("Owls has moved outside the buffer distance at %s" % point.time)
            break
        else:
            start = point
            continue 


    newTrack = Track(track.start,track.points[startIndex:endIndex])
    return newTrack


### distance formula for python 
### provided by:https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude 
### not adjusted for earth's curvature, but can be neglected as measured distances are in a very small range (approx. 0 - 100m)
def getDistance(start,end):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(start.coordinates[0])
    lon1 = radians(start.coordinates[1])
    lat2 = radians(end.coordinates[0])
    lon2 = radians(end.coordinates[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    #print("Result:", distance)

    # multiply by 1000 to get meters
    return distance*1000


def __main__():
    owls = []
    ### loop over every shapefile available
    for owl in owl_ids:
        print("Now checking Owl with ID %s" % owl)
        print("")
        # load data directory & shapefile dynamically
        data_dir = os.path.join('/home', 'eric', 'Documents',
                                'PyGIS', 'movebank', 'singleOwls', owl)
        shapefile = os.path.join(data_dir,'%s.shp' % owl)
        data_source = driver.Open(shapefile, 0)
        layer = data_source.GetLayer(0)
        owltype = layer[0].GetField('Owl_Type')
        # iterate each point in the shapefile
        print("Dividing shapefile into individual tracks")
        owl_tracks = divideIntoTracks(layer)

        owl1 = Owl(owl,owl_tracks,owltype)
        owls.append(owl1)
        print("Calculating averages")
        analysis = calculateAverages(owl1)
        print("...Done!")
        print("")
        print("Writing to csv...")
        with open(csv_file,'a',newline='') as csvfile:
            writer = csv.writer(csvfile,delimiter=',')
            newrow = [owl1.id,analysis[0],analysis[1],analysis[2],owl1.owltype]
            writer.writerow(newrow)
            print("...new line added: %s" % newrow)
            print("")

if __name__ == "__main__":
    __main__()