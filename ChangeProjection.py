import gdal
import ogr
import os
import osr

# Get a Layer
data_dir = os.path.join('C:\\', 'Users', 'caro1','Downloads','movebank', 'movebank')
inShapefile = os.path.join(data_dir, 'eagle_owl','basemap_102013.shp')
driver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = driver.Open(inShapefile, 0)
layer = inDataSource.GetLayer()

spatialRef = layer.GetSpatialRef()
print(spatialRef)
# input SpatialReference
inSpatialRef = osr.SpatialReference()
inSpatialRef.ImportFromEPSG(4326)

# output SpatialReference
sr = osr.SpatialReference()
sr.ImportFromEPSG(102013)

# create the CoordinateTransformation
transform = osr.CoordinateTransformation(inSpatialRef, sr)
print(transform)


out_fn = os.path.join(data_dir, 'eagle_owl', 'basemap_102013.shp')
# Delete if output file already exists
# We can use the same driver
if os.path.exists(out_fn):
    print('exists, deleting')
    driver.DeleteDataSource(out_fn)
out_ds = driver.CreateDataSource(out_fn)
if out_ds is None:
    print('Could not create %s' % (out_fn))

# Create the shapefile layer WITH THE SR
out_lyr = out_ds.CreateLayer('track_points', sr, 
                             ogr.wkbPoint)

out_lyr.CreateFields(layer.schema)
out_defn = out_lyr.GetLayerDefn()
out_feat = ogr.Feature(out_defn)
# Loop over all features and change their spatial ref
for in_feat in layer:
    geom = in_feat.geometry()
    geom.Transform(transform)
    out_feat.SetGeometry(geom)
    # Make sure to also include the attributes in the new file
    for i in range(in_feat.GetFieldCount()):
        value = in_feat.GetField(i)
        out_feat.SetField(i, value)
    out_lyr.CreateFeature(out_feat)

del out_ds

print('done')