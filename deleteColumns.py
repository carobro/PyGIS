import gdal
import ogr
import os
import osr

#############
data_dir = os.path.join('C:\\', 'Users', 'celeb', \
'Desktop', 'Uni', 'Master', 'Python_in_GIS', \
'movebank', 'movebank', 'eagle_owl', 'Eagle owl Reinhard Vohwinkel MPIO')

# Path to the shapefile
shape_file = os.path.join(data_dir, 'points.shp')

# load the shapefile
layer = iface.addVectorLayer(shape_file, "shape:", "ogr")
if not layer:
    print("Shapefile failed to load!")

# Check for editing rights (capabilities)
caps = layer.dataProvider().capabilities()
print(caps)
caps_string = layer.dataProvider().capabilitiesString()
print(caps_string)


# Remove here the fields which are not necessary
# 
if caps & QgsVectorDataProvider.DeleteAttributes:
    res = layer.dataProvider().deleteAttributes([3, 4, 5, 6, 7, 9, 11, 16, 17, 18, 22, 26, 27])

# update to propagate the changes  
layer.updateFields()    
print("done")