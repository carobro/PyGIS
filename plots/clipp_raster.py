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
in_fn = os.path.join(data_dir, 'viirs_npp.tif')

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
convexhulls = [in_path,in_path2,in_path3,in_path4,in_path5,in_path6]

# open the raster and read out the data in a numpy array
rast_data_source = gdal.Open(in_fn)
# To translate coordinates to raster indices
gt = rast_data_source.GetGeoTransform()
inv_gt = gdal.InvGeoTransform(gt)

# Get the correct driver for the gps track
driver = ogr.GetDriverByName('ESRI Shapefile')
index = 0
for i in convexhulls:
    # 0 means read-only. 1 means writeable.
    vect_data_source = driver.Open(i, 0) 

    # Get the Layer class object
    layer = vect_data_source.GetLayer(0)

    # Determine the spatial extent of the track
    # is a list with x_left, x_right, y_bottom, y_top
    extent = layer.GetExtent()
    print('vector extent is', extent)

    # Decide on the size of the buffer around the track
    buffer = 0.002
    x1, y1= gdal.ApplyGeoTransform(inv_gt, extent[0] - buffer, 
                                                extent[2] - buffer)
    x2, y2= gdal.ApplyGeoTransform(inv_gt, extent[1] + buffer, 
                                                extent[3] + buffer)
                                                
    # round these indices, (especially when not using a buffer)
    # y indices increase from top to bottom!!
    #print('column numbers are', x1, x2, y1, y2)
    x1 = int(round(x1))
    y1 = int(round(y1))
    x2 = int(round(x2))
    y2 = int(round(y2))
    print(x1,x2,y1,y2)
    #print('column numbers are', x1, x2, y1, y2)
    # calculate how many rows and columns the ranges cover
    out_columns = x2 - x1
    # y indices increase from top to bottom!!
    out_rows = y1 - y2
    print('output raster extent:', out_columns, out_rows)

    out_fn = os.path.join(data_dir, 'clipped' , 'test' + str(index) + '.tif')
    index = index + 1
    # Create empty output raster (clipped size)
    out_driver = gdal.GetDriverByName('GTiff')
    print(out_driver)
    # Rasters can be overwritten
    # We cannot delete if output file already exists
    out_ds = out_driver.Create(out_fn, out_columns, out_rows, 1) # 1 = one band
    print(out_ds)
    wkt = rast_data_source.GetProjection()
    out_ds.SetProjection(wkt)
    out_gt = list(gt)
    out_gt[0] = extent[0] - buffer
    out_gt[3] = extent[3] + buffer
    out_ds.SetGeoTransform(out_gt)

    # Get data from the source raster and write to the new one
    in_band = rast_data_source.GetRasterBand(1)
    out_band = out_ds.GetRasterBand(1)
    # Read only the part we need
    data = in_band.ReadAsArray(x1, y2, out_columns, out_rows)
    out_band.WriteArray(data)
    out_ds.FlushCache()

print('done')