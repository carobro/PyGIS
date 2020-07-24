from osgeo import ogr
import os

# Get a Layer
data_dir = os.path.join('C:\\', 'Users', 'mirje','OneDrive','Desktop')
inShapefile = os.path.join(data_dir, 'new','reprojected', 'repro.shp')
inDriver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = inDriver.Open(inShapefile, 0)
inLayer = inDataSource.GetLayer()


# Collect all Geometry
geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
for feature in inLayer:

    ident = feature.GetField('tag_ident')
    if ident == "1292":
       geomcol.AddGeometry(feature.GetGeometryRef())

# Calculate convex hull

convexhull = geomcol.ConvexHull()

# Save extent to a new Shapefile

outShapefile= os.path.join (data_dir, 'points_convexhull.shp')
outDriver = ogr.GetDriverByName("ESRI Shapefile")

# Remove output shapefile if it already exists
if os.path.exists(outShapefile):
    outDriver.DeleteDataSource(outShapefile)

# Create the output shapefile
outDataSource = outDriver.CreateDataSource(outShapefile)
outLayer = outDataSource.CreateLayer("states_convexhull", geom_type=ogr.wkbPolygon)

# Add an ID field
idField = ogr.FieldDefn("id", ogr.OFTInteger)
outLayer.CreateField(idField)

new_field = ogr.FieldDefn("Area", ogr.OFTReal)
new_field.SetWidth(32)
new_field.SetPrecision(10) #added line to set precision
outLayer.CreateField(new_field)

# Create the feature and set values
featureDefn = outLayer.GetLayerDefn()
feature = ogr.Feature(featureDefn)
feature.SetGeometry(convexhull)
feature.SetField("id", 1)
outLayer.CreateFeature(feature)

geom = feature.GetGeometryRef()
area = geom.GetArea() 
print (area)
feature.SetField("Area", area)
outLayer.SetFeature(feature)
feature = None



# Save and close DataSource
inDataSource = None
outDataSource = None
