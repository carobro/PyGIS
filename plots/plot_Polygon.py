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
in_fn = os.path.join(data_dir, 'clipped', 'test0.tif')
in_fn1 = os.path.join(data_dir, 'clipped', 'test1.tif')
in_fn2 = os.path.join(data_dir, 'clipped', 'test2.tif')
in_fn3 = os.path.join(data_dir, 'clipped', 'test3.tif')
in_fn4 = os.path.join(data_dir, 'clipped', 'test4.tif')
in_fn5 = os.path.join(data_dir, 'clipped', 'test5.tif')

rasters = []
rasters = [in_fn,in_fn1,in_fn2,in_fn3,in_fn4,in_fn5]

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
    
print(max)
print(miy)

#############
# Reading a shapefile
##urban
in_path = os.path.join('C:\\', 'Users', 'caro1', \
'Downloads', 'pig_proj', 'convexat', '4848', 'points_convexhull.shp')

in_path2 = os.path.join('C:\\', 'Users', 'caro1', \
'Downloads', 'pig_proj', 'convexat', '5158', 'points_convexhull.shp')

in_path3 = os.path.join('C:\\', 'Users', 'caro1', \
'Downloads', 'pig_proj', 'convexat', '3892', 'points_convexhull.shp')

## rural
in_path4 = os.path.join('C:\\', 'Users', 'caro1', \
'Downloads', 'pig_proj', 'convexat', '3897', 'points_convexhull.shp')

in_path5 = os.path.join('C:\\', 'Users', 'caro1', \
'Downloads', 'pig_proj', 'convexat', '4846', 'points_convexhull.shp')

in_path6 = os.path.join('C:\\', 'Users', 'caro1', \
'Downloads', 'pig_proj', 'convexat', '1292', 'points_convexhull.shp')

convexhulls = []
convexhulls = [in_path,in_path2,in_path3,in_path4,in_path5,in_path6]

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
    index = 0
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
    
palette = copy(plt.cm.inferno)
palette.set_over('y', 1.0)
palette.set_under('k', 0.0)
palette.set_bad('w', 1.0)

# Create the plot
f, ((ax0, ax1), (ax2, ax3), (ax4, ax5)) = plt.subplots(3, 2)
# use imshow to plot the raster with the correct coordinates
im = ax0.imshow(dataset[0], cmap=palette,
                aspect='auto',origin='lower',
                interpolation='bilinear',
                extent=(mix[0], max[0], miy[0], may[0]))
ax0.plot(xcoords[0], ycoords[0], 'r-')
ax1.imshow(dataset[1], cmap=palette,
                aspect='auto', origin='lower',
                interpolation='bilinear',
                extent=(mix[1], max[1], miy[1], may[1]))
ax1.plot(xcoords[1], ycoords[1], 'r-')
ax2.imshow(dataset[2], cmap=palette,
                aspect='auto', origin='lower',
                interpolation='bilinear',
                extent=(mix[2], max[2], miy[2], may[2]))
ax2.plot(xcoords[2], ycoords[2], 'r-')
ax3.imshow(dataset[3], cmap=palette,
                aspect='auto', origin='lower',
                interpolation='bilinear',
                extent=(mix[3], max[3], miy[3], may[3]))
ax3.plot(xcoords[3], ycoords[3], 'r-')
ax4.imshow(dataset[4], cmap=palette,
                aspect='auto', origin='lower',
                interpolation='bilinear',
                extent=(mix[4], max[4], miy[4], may[4]))
ax4.plot(xcoords[4], ycoords[4], 'r-')
ax5.imshow(dataset[5], cmap=palette,
                aspect='auto', origin='lower',
                interpolation='bilinear',
                extent=(mix[5], max[5], miy[5], may[5]))
ax5.plot(xcoords[5], ycoords[5], 'r-')
# add the legend
f.subplots_adjust(right=0.8)
cbar_ax = f.add_axes([0.85, 0.15, 0.05, 0.7])
f.colorbar(im, cax=cbar_ax)
f.suptitle('Owl Hunting Areas')
ax0.set_title('urban')
ax1.set_title('rural')

## Make the axes' units equal
#plt.axis('equal')
plt.show()





