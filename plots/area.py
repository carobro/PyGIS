import matplotlib.pyplot as plt
import ogr
import os
import gdal
import osr
import numpy as np
from copy import copy
import matplotlib.colors as colors

data_dir2 = os.path.join('C:\\', 'Users', 'caro1', 'Downloads', \
                        'cnvarear', 'convexat')
##urban
in_path   = os.path.join(data_dir2, '4848', 'points_convexhull.shp')
in_path2  = os.path.join(data_dir2, '5158', 'points_convexhull.shp')
in_path3  = os.path.join(data_dir2, '3892', 'points_convexhull.shp')
in_path4  = os.path.join(data_dir2, '4046', 'points_convexhull.shp')
in_path5  = os.path.join(data_dir2, '4043', 'points_convexhull.shp')
in_path6  = os.path.join(data_dir2, '3893', 'points_convexhull.shp')
in_path7  = os.path.join(data_dir2, '1750', 'points_convexhull.shp')
in_path8  = os.path.join(data_dir2, '1751', 'points_convexhull.shp')
in_path9  = os.path.join(data_dir2, '3899', 'points_convexhull.shp')
in_path10 = os.path.join(data_dir2, '1753', 'points_convexhull.shp')
in_path11 = os.path.join(data_dir2, '1754', 'points_convexhull.shp')
in_path12 = os.path.join(data_dir2, '5159', 'points_convexhull.shp')
in_path13 = os.path.join(data_dir2, '4044', 'points_convexhull.shp')
in_path14 = os.path.join(data_dir2, '4045', 'points_convexhull.shp')


## rural
in_path15 = os.path.join(data_dir2, '3897', 'points_convexhull.shp')
in_path16 = os.path.join(data_dir2, '4846', 'points_convexhull.shp')
in_path17 = os.path.join(data_dir2, '3896', 'points_convexhull.shp')
in_path18 = os.path.join(data_dir2, '3898', 'points_convexhull.shp')
in_path19 = os.path.join(data_dir2, '3894', 'points_convexhull.shp')
in_path20 = os.path.join(data_dir2, '1292', 'points_convexhull.shp')
in_path21 = os.path.join(data_dir2, '3895', 'points_convexhull.shp')

u = []
r = []
u = [in_path,in_path2,in_path3, in_path4, in_path5,in_path6,
    in_path7, in_path8, in_path9, in_path10, in_path11, in_path12,in_path13, in_path14]

r = [in_path15,in_path16,in_path17,in_path18,in_path19,in_path20,in_path21]


j = 0
area_u = []
area_r = []
for i,j in zip(u,r):
    # Get the correct driver and open file for reading
    driver = ogr.GetDriverByName('ESRI Shapefile')
    track = driver.Open(i, 0)
    track2 = driver.Open(j, 0)
    # Get the layer
    layer = track.GetLayer(0)
    layer2 = track2.GetLayer(0)
    # Access single features in the places layer
    # Get the values from the Area Attribute
    for feat,feat2 in zip(layer,layer2):
        print(feat.GetField('Area'))
        size = feat.GetField('Area')/1000000
        size2 = feat2.GetField('Area')/1000000
    area_u.append(size)
    area_r.append(size2)
        
print(area_u)
print(area_r)

## statistics
mean_u = round(sum(area_u)/len(area_u), 3)
print("Mean urban area is:")
print(mean_u)
mean_r = round(sum(area_r)/len(area_r), 3)
print("Mean rural area is:")
print(mean_r)

# Make out boxplot
plt.boxplot([area_u, area_r], labels=["Urban", "Rural"])
plt.suptitle('Owl Hunting Area')
plt.xlabel("Owl types")
plt.ylabel("square kilometre")


plt.show()

