## author: Carolin Bronowicz, Aysel Tandik
## PIG course 2020
## Group 6

import matplotlib.pyplot as plt
import ogr
import os
import gdal
import osr
import numpy as np
from copy import copy
import matplotlib.colors as colors

# path to the raster
data_dir = os.path.join('C:\\', 'Users', 'caro1', 'Documents')
in_fn  = os.path.join(data_dir, 'clipped', 'test0.tif')
in_fn2 = os.path.join(data_dir, 'clipped', 'test1.tif')
in_fn3 = os.path.join(data_dir, 'clipped', 'test2.tif')
in_fn4 = os.path.join(data_dir, 'clipped', 'test3.tif')
in_fn5 = os.path.join(data_dir, 'clipped', 'test4.tif')
in_fn6 = os.path.join(data_dir, 'clipped', 'test5.tif')

rasters = []
rasters = [in_fn,in_fn4,in_fn2,in_fn5,in_fn3,in_fn6]

dataset = []
max = []
mix = []
may = []
miy = []
for i in rasters:
    # open the raster and read out the data in a numpy array
    rast_data_source = gdal.Open(i)
    in_band = rast_data_source.GetRasterBand(1)
    data = in_band.ReadAsArray()

    geoTransform = rast_data_source.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]

    maxx = minx + geoTransform[1] * \
           rast_data_source.RasterXSize
    miny = maxy + geoTransform[5] * \
           rast_data_source.RasterYSize

    x = np.linspace(minx, maxx, 500)
    y = np.linspace(miny, maxy, 500)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-X**2 - Y**2)
    Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
    Z = (Z1 - Z2) * 2
    Zm = np.ma.masked_where(data > 5, data)
    
    dataset.append(Zm)
    max.append(maxx)
    mix.append(minx)
    may.append(maxy)
    miy.append(miny)

##########################################################
# Reading a shapefile
data_dir2 = os.path.join('C:\\', 'Users', 'caro1', 'Downloads', \
                        'pig_proj', 'convexat')
##urban
in_path  = os.path.join(data_dir2, '4848', 'points_convexhull.shp')
in_path2 = os.path.join(data_dir2, '5158', 'points_convexhull.shp')
in_path3 = os.path.join(data_dir2, '3892', 'points_convexhull.shp')

## rural
in_path4 = os.path.join(data_dir2, '3897', 'points_convexhull.shp')
in_path5 = os.path.join(data_dir2, '4846', 'points_convexhull.shp')
in_path6 = os.path.join(data_dir2, '3896', 'points_convexhull.shp')

convexhulls = []
convexhulls = [in_path,in_path4,in_path2,in_path5,in_path3,in_path6]

j = 0
arr = []
xcoords = []
ycoords = []
for i in convexhulls:
    # Get the correct driver and open file for reading
    driver = ogr.GetDriverByName('ESRI Shapefile')
    track = driver.Open(i, 0)
    # Get the layer
    layer = track.GetLayer(0)
    # Access single features in the places layer
    # And plot them
    for feat in layer:
        pt = feat.geometry()
    #index = 0
    x = []
    y = []
    for coord in pt:
        index = 0
        while coord.GetX(index):
            x.append(coord.GetX(index))
            y.append(coord.GetY(index))
            index = index + 1
    xcoords.append(x)
    ycoords.append(y)

# Create the plot
f, ((ax0, ax1), (ax2, ax3), (ax4, ax5)) = plt.subplots(3, 2)
# use imshow to plot the raster with the correct coordinates
palette = copy(plt.cm.inferno)
palette.set_over('y', 1.0)
palette.set_under('k', 0.0)
palette.set_bad('w', 1.0)

for k in range(0,6):
    im = locals()['ax' + str(k)].imshow(dataset[k], cmap=palette,
                aspect='auto',origin='lower',
                interpolation='bilinear',
                extent=(mix[k], max[k], miy[k], may[k]))
    locals()['ax' + str(k)].plot(xcoords[k], ycoords[k], 'r-')

## add the legend
f.subplots_adjust(right=0.8)
cbar_ax = f.add_axes([0.85, 0.15, 0.05, 0.7])
f.colorbar(im, cax=cbar_ax)

f.suptitle('Owl Hunting Areas')
ax0.set_title('urban')
ax1.set_title('rural')

## Make the axes' units equal
plt.axis('on')
plt.show()


