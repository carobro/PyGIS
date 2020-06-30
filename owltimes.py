import gdal
import ogr
import os
import osr
import dateparser
from Owl import Owl
from Track import Track
from Point import Point



owl_ids = ["1750", "1751", "1753", "1754", "1292", "3893", "3892", "3894", "3895", "3896",
           "3897", "3899", "3898", "4043", "4044", "4045", "4046", "5158", "5159", "4846", "4848"]
driver = ogr.GetDriverByName('ESRI Shapefile')
owls = []
for owl in owl_ids:
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
            if(date == float(start.strftime("%d"))+1):
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
            if(date == float(start.strftime("%d"))+1):
                points.append(p1)
                continue
    ### 
    owl1 = Owl(owl,owl_tracks)
    owls.append(owl1)
