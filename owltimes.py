import gdal
import ogr
import os
import osr
import dateparser
from Owl import Owl

owl_ids = ["1750","1751","1753","1754","1292","3893","3892","3894","3895","3896","3897","3899","3898","4043","4044","4045","4046","5158","5159","4846","4848"]

# load data directory & shapefile
data_dir = os.path.join('/home', 'eric', 'Documents',
                        'PyGIS', 'movebank', 'singleOwls', '3899')
driver = ogr.GetDriverByName('ESRI Shapefile')
### for performance reasons only a shapefile with points from owl 3899 is used 
shapefile = os.path.join(data_dir, '3899.shp')
data_source = driver.Open(shapefile, 0)
# layer creation
layer = data_source.GetLayer(0)
feature_count = layer.GetFeatureCount()
# array of dicts, each entry is one day/night cycle of owl movement
owl_tracks = []
### sinle owl track to be added to array above
owl_track = []
### variable which indicates start of the currently looked at track
start = None
### iterate each point in the shapefile
for feat in layer:
    ### variable creation for comparisons below 
    timestamp = dateparser.parse(feat.GetField('timestamp'))
    hour = float(timestamp.strftime("%H"))
    date = float(timestamp.strftime("%d"))
    ## if feat is after 9am 
    if(hour > 9):
        ## if no start is(i.e. beginning of the loop) set start of track
        if(not(start)):
            start = dateparser.parse(feat.GetField('timestamp'))
            owl_track.append(feat.GetField('timestamp'))
            continue
        ## if feat is after 9am and one day after start: a new track begins
        ## append owl_track to track collection and set a new start
        if(date == float(start.strftime("%d"))+1):
            owl_tracks.append(owl_track)
            owl_track = [feat.GetField('timestamp')]
            owl1 = Owl("3899",owl_tracks)
            start = dateparser.parse(feat.GetField('timestamp'))
            continue
    ## if feat is on the same date and after the start add it to the track
    if(date == float(start.strftime("%d"))):
        owl_track.append(feat.GetField('timestamp'))
        continue
    ## if feat is before nine and one day after the start add it to the track
    if(float(timestamp.strftime("%H")) < 9):
        if(date == float(start.strftime("%d"))+1):
            owl_track.append(feat.GetField('timestamp'))
            continue

# attribute info
attributes = layer.GetLayerDefn()
