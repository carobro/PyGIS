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

# Adding the owltype field into the attribute table
if caps & QgsVectorDataProvider.AddAttributes:
    # Adding as a list of items, each with
    # the name and the data type of the field
    res = layer.dataProvider().addAttributes(
        [QgsField("Owl_Type", QVariant.String)])
# update to propagate the changes  
layer.updateFields



# remove the fields 
#if caps & QgsVectorDataProvider.DeleteAttributes:
#    res = layer.dataProvider().deleteAttributes([16,17,18])
##
### update to propagate the changes  
#layer.updateFields() 


# Get the index of the new field "owl_tpye" and the tag_ident
field_name_i_search = 'tag_ident'
field_owlT = "Owl_Type"
fields = layer.dataProvider().fields()
IDindex = 0

for field in layer.fields():
    if field.name() == field_name_i_search:
        break
    IDindex += 1
print(IDindex)

owlIndex = 0
for field in layer.fields():
    if field.name() == field_owlT:
        break
    owlIndex += 1
print(owlIndex)




# Find all the specific owls and categorize them
# into the owltypes "rural" and "urban". Then 
# insert the type of the owl in the "owl_type" column
updates = {}
for feat in layer.getFeatures():
    # Get the date time value from the gpx
    #date_time = QDateTime(gpx_feat['time'])
    if feat['tag_ident'] == '4848' or feat['tag_ident'] == '4043' or feat['tag_ident'] == '4046' or feat['tag_ident'] == '5158' or feat['tag_ident'] == '3892' or feat['tag_ident'] == '3893' or feat['tag_ident'] == '1750' or feat['tag_ident'] =='1751'or feat['tag_ident'] == '1753' or feat['tag_ident'] == '1754' or feat['tag_ident'] == '3899' or feat['tag_ident'] == '4044' or feat['tag_ident'] == '4595' or feat['tag_ident'] == '4045':
        type = 'urban'
    if feat['tag_ident'] == '3897' or feat['tag_ident'] == '3898' or feat['tag_ident'] == '4846' or feat['tag_ident'] == '3894' or feat['tag_ident'] == '1292' or feat['tag_ident'] == '3896' or feat['tag_ident'] == '3895':
        type = 'rural'
        
    # Update the empty field in the shapefile
    updates[feat.id()] = {owlIndex: type}
#print(updates)

# update the field for all features
layer.dataProvider().changeAttributeValues(updates)
# Update to propagate the changes
layer.updateFields()
print("done")
