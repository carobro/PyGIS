from matplotlib import pyplot as plt
import csv
import pandas as pd
import numpy as np
import matplotlib

id_u = []
duration_u = []
start_u = []
end_u = []
id_r = []
duration_r = []
start_r = []
end_r = []
tagI = []
hoursR = []
hoursU = []
with open('C:/Users/celeb/Desktop/Uni/Master/Python_in_GIS/sampleCSV.csv', 'r') as file:
    reader = csv.reader(file)
    name = next(reader)[1]
    for row in reader:
        if (row[4] == ' rural'):
            id_r.append(row[0])
            start_r.append(row[2])
            end_r.append(row[3])
            duration_r.append(row[1])
            hour = row[1]
            slice = hour[1:3]
            number = int(slice)
            hoursR.append(number)
        else: 
            id_u.append(row[0])
            start_u.append(row[2])
            end_u.append(row[3])
            duration_u.append(row[1])
            hour = row[1]
            slice = hour[1:3]
            number = int(slice)
            hoursU.append(number)

len1 = len(hoursU) - len(hoursR)
len2 = len(hoursR) - len(hoursU)

while (len1 != len2):
    if len1 < len2:
        hoursU.append(0)
    if len2 < len1:
        hoursR.append(0)
    else: break
    
hoursR.sort()
hoursU.sort()
sortedR = []
sortedU = []
print(hoursR)
print(hoursU)
#
#k= 0
#while(k < len(hoursR)):
#    for i,j in zip(hoursR, hoursU):
#        #for j in range(0, len(hoursU)):
#            #if i = 0 || j = 0:
#            if i != 0 and j != 0:  
#                if i < j:
#                    sortedR.append(i)
#                    sortedU.append(0)
#                if j > i:
#                    sortedR.append(0)
#                    sortedU.append(j)
#                else:
#                    sortedU.append(j)
#                    sortedR.append(i)
#                
#
#            else:
#                sortedU.append(j)
#                sortedR.append(i)
#                
#            continue
#            
#    k = k +1
#        
#    
#print(sortedR)
#print(sortedU)
#            
            
        

labels = 5
x = np.arange(labels)

width = 0.35
fig, ax = plt.subplots()
p1 = ax.bar(x, hoursU, width)
#p2 = ax.bar(x, hoursR, width)#, bottom=hoursR)
#plt.show()

labels = ['G1', 'G2', 'G3', 'G4', 'G5']
fig, ax = plt.subplots()


ax.bar(labels, hoursU, width, label='Urban')
ax.bar(labels, hoursR, width, bottom=hoursU,
       label='Rural')

ax.set_ylabel('Duration hours')
ax.set_title('Duration owls')
ax.legend()

plt.show()





