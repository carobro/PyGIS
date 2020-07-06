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



def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)

def calculateAverages(owl):

    avgDuration = getDurationAverage(owl1.tracks)
    avgStart = getStartAverage(owl1.tracks)
    avgEnd = getEndAverage(owl1.tracks)

    return [avgDuration,avgStart,avgEnd]

def getDurationAverage(tracks):

    avgTracks = owl1.tracks
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

def sortOutTrack(track):

    endtime = None
    # set start position 
    start = Point([52.2,3.3],"2012")  
    # create buffer around point (10m) 
    buffer = start.createBuffer(10)
    watching = False
    for point in track:
        if(pointInBuffer(point,buffer)):
            if(watching):
                if(tenMinutesPassed):
                    print("End of hunting found at %s" % point.time )
                    endtime = point
                    break
            else:
                watching = True

def pointInPolygon(point,polygon):
    

    return True
#owl_ids = ["3893"]
# owl_ids = ["1750", "1751", "1753", "1754", "1292", "3893", "3892", "3894", "3895", "3896","3897", "3899", "3898", "4043", "4044", "4045", "4046", "5158", "5159", "4846", "4848"]
owl_ids = ["3894","4045", "4046", "5158", "5159", "4846", "4848"]
driver = ogr.GetDriverByName('ESRI Shapefile')
owls = []
analysis_dir = os.path.join('/home','eric','Documents','PyGIS','analysis')
csv_file = os.path.join(analysis_dir,'results.csv')

for owl in owl_ids:
    print("Now checking Owl with ID %s" % owl)
    # load data directory & shapefile
    data_dir = os.path.join('/home', 'eric', 'Documents',
                            'PyGIS', 'movebank', 'singleOwls', owl)
    shapefile = os.path.join(data_dir,'%s.shp' % owl)
    data_source = driver.Open(shapefile, 0)
    layer = data_source.GetLayer(0)
    owl_tracks = []
    start = None
    points = []
    # iterate each point in the shapefile
    for feat in layer:
        # variable creation for comparisons below
        #2014-05-25 23:33:07

        timestamp = dateparser.parse(feat.GetField('timestamp'))
        if (feat.GetField('timestamp') == '2016-04-20 19:00:23'):
            print("break")
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
    ### 
    owl1 = Owl(owl,owl_tracks)
    owls.append(owl1)
    print("Hunting detection done")
    print("Calculating averages")
    analysis = calculateAverages(owl1)
    print("...Done!")
    print("")
    print("Writing to csv...")
    with open(csv_file,'a',newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow([owl1.id,analysis[0],analysis[1],analysis[2]])
        print("New line added")
        print("")

