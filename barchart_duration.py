from matplotlib import pyplot as plt
import csv
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
with open('C:/Users/caro1/Downloads/sampleCSV_trash.csv', 'r') as file:
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

for i,j in zip(hoursR, hoursU):
    if i != 0 and j != 0:  
        if i < j:
            sortedR.append(i)
            sortedU.append(0)
        if j > i:
            sortedR.append(0)
            sortedU.append(j)
        else:
            sortedU.append(j)
            sortedR.append(i)
    else:
        sortedU.append(j)
        sortedR.append(i)

print(sortedR)
print(sortedU)
            
##################################################################
# create a stacket bar plot
#labels = len(sortedR)
#x = np.arange(labels)
#
#width = 0.35
#labels = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7']
#fig, ax = plt.subplots()
#ax.bar(labels, sortedU, width, label='Urban')
#ax.bar(labels, sortedR, width, label='Rural', bottom=sortedU)
#
#ax.set_ylabel('Duration hours')
#ax.set_title('Duration owls')
#ax.legend()
#
#plt.show()
#############################################
# create a Bar plot plot
fig, ax = plt.subplots()
n_groups = len(sortedR)
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, sortedU, bar_width, alpha=opacity, color='b',
label='Urban')
rects2 = plt.bar(index + bar_width, sortedR, bar_width, alpha=opacity, 
color='orange', label='Rural')

plt.xlabel('duration')
plt.ylabel('hour section')
plt.title('Duration owls')
plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E', 'F'))
plt.legend()

plt.tight_layout()
plt.show()




