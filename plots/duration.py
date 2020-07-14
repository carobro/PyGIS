from matplotlib import pyplot as plt
import csv
import numpy as np
import matplotlib
import statistics

timeR = []
timeU = []
with open('C:/Users/caro1/Downloads/PyGIS-master/PyGIS-master/analysis/resultsbuffer.csv', 'r') as file:
    reader = csv.reader(file)
    name = next(reader)[1]
    for row in reader:
        print(row)
        if (row[4] == 'rural'):
            hoursinminutes_r = int(row[1][0:2])*60
            time_r = hoursinminutes_r + int(row[1][3:5])
            timeR.append(time_r)
            print(time_r)
        else: 
            hoursinminutes_u = int(row[1][0:2])*60
            time_u = hoursinminutes_u + int(row[1][3:5])
            timeU.append(time_u)
            print(time_u)

#print(timeR)
#print(timeU)

meanU = round(sum(timeU)/len(timeU), 3)
print("Mean urban duration is:")
print(meanU)
medU = statistics.median(timeU)
print("Median urban duration is:")
print(medU)
sdU = round(statistics.stdev(timeU),3)
print("SD urban duration is:")
print(sdU)

print('_________________________________________')
meanR = round(sum(timeR)/len(timeR), 3)
print("Mean rural duration is:")
print(meanR)
medR = statistics.median(timeR)
print("Median rural duration is:")
print(medR)
sdR = round(statistics.stdev(timeR), 3)
print("SD rural duration is:")
print(sdR)


plt.boxplot([timeU, timeR], labels=["Urban", "Rural"])
plt.suptitle('Owl Hunting Duration')
plt.ylabel("Minutes")
plt.xlabel("Owl Types")

plt.show()
