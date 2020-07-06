import matplotlib.pyplot as plt
import ogr
import os

#############
# Reading a shapefile
in_path = os.path.join('C:\\', 'Users', 'caro1', \
'Downloads', 'pig_proj', 'convexat', '1292', 'points_convexhull.shp')

# Get the correct driver and open file for reading
driver = ogr.GetDriverByName('ESRI Shapefile')
track = driver.Open(in_path, 0)

# Get the layer
layer = track.GetLayer(0)

# Create the plot
f, ax = plt.subplots(1)
# Access single features in the places layer
# And plot them
for feat in layer:
    pt = feat.geometry()
print(pt)
index = 0
x = []
y = []
for coord in pt:
    for index in range(0,15):
        x.append(coord.GetX(index))
        y.append(coord.GetY(index))
        
ax.plot(x, y, 'r-')
ax.set_xlabel('x coordinate')
ax.set_ylabel('y coordinate')
# Make the axes' units equal
plt.axis('equal')
plt.show()

