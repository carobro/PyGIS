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

#owl_ids = ["3893"]
owl_ids = ["1750", "1751", "1753", "1754", "1292", "3893", "3892", "3894", "3895", "3896","3897", "3899", "3898", "4043", "4044", "4045", "4046", "5158", "5159", "4846", "4848"]

driver = ogr.GetDriverByName('ESRI Shapefile')
analysis_dir = os.path.join('/home','eric','Documents','PyGIS','analysis')
csv_file = os.path.join(analysis_dir,'results.csv')



def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)

def calculateAverages(owl):

    avgDuration = getDurationAverage(owl.tracks)
    avgStart = getStartAverage(owl.tracks)
    avgEnd = getEndAverage(owl.tracks)

    return [avgDuration,avgStart,avgEnd]

def getDurationAverage(tracks):

    avgTracks = tracks
    sum_duration = 0
    for track in avgTracks:
        sum_duration+=track.getDuration()
    avgDuration = sum_duration / len(avgTracks)
    avgDuration = datetime.timedelta(seconds=avgDuration)
    return chop_microseconds(avgDuration)

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

def divideIntoTracks(layer):

    owl_tracks = []
    start = None
    points = []

    for feat in layer:

        timestamp = dateparser.parse(feat.GetField('timestamp'))

        hour = float(timestamp.strftime("%H"))
        date = float(timestamp.strftime("%d"))
        p1 = Point([feat.GetField('lat'),feat.GetField('long')],timestamp)
        # if feat is after 9am
        if(hour > 9):
            # if no start is(i.e. beginning of the loop) set start of track
            if(not(start)):
                start = dateparser.parse(feat.GetField('timestamp'))
                points.append(p1)
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
                start = dateparser.parse(feat.GetField('timestamp'))
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

def sortOutTrack(track):

    endtime = None
    # set start position 
    start = track.points[0]
    startIndex = len(track.points)-1
    # create buffer around point (10m) 
    watching = False

    for index,point in enumerate(track.points):
        hour = float(point.time.strftime("%H"))
        if(not(hour>0 and hour<6)):
            continue
        if(getDistance(start,point) < 20):
            if(watching):
                duration = point.time - start.time
                duration = duration.total_seconds()
                if(duration>1200):
                #    print("End of hunting found at %s" % point.time)
                    startIndex = index
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
    

    newTrack = Track(track.start,track.points[:startIndex])
    return newTrack

### distance formula for python 
### provided by:https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude 
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
        # iterate each point in the shapefile
        print("Dividing shapefile into individual tracks")
        owl_tracks = divideIntoTracks(layer)

        owl1 = Owl(owl,owl_tracks)
        owls.append(owl1)
        print("Calculating averages")
        analysis = calculateAverages(owl1)
        print("...Done!")
        print("")
        print("Writing to csv...")
        with open(csv_file,'a',newline='') as csvfile:
            writer = csv.writer(csvfile,delimiter=',')
            newrow = [owl1.id,analysis[0],analysis[1],analysis[2]]
            writer.writerow(newrow)
            print("...new line added: %s" % newrow)
            print("")

if __name__ == "__main__":
    __main__()