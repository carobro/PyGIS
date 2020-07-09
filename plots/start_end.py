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
with open("C:/Users/caro1/Downloads/results.csv", 'r') as file:
    reader = csv.reader(file)
    name = next(reader)[1]
    for row in reader:
        if (row[4] == 'rural'):
            hoursinminutes_r = int(row[2][0:2])*60
            time_r = hoursinminutes_r + int(row[2][3:5])
            start_r.append(time_r)
            
            hoursinminutes_r_end = int(row[3][0:2])*60
            time_r_end = hoursinminutes_r_end + int(row[3][3:5])
            end_r.append(time_r_end)
        else: 
            hoursinminutes_u = int(row[2][0:2])*60
            time_u = hoursinminutes_u + int(row[2][3:5])
            start_u.append(time_u)
            
            hoursinminutes_u_end = int(row[3][0:2])*60
            time_u_end = hoursinminutes_u_end + int(row[3][3:5])
            end_u.append(time_u_end)

print(start_u)
print(start_r)

fig, (ax1, ax2) = plt.subplots(1,2)
ax1.boxplot([start_u, start_r])
ax1.set_title('Start Owl Hunting')

ax2.boxplot([end_u, end_r])
ax2.set_title('End Owl Hunting')

plt.show()