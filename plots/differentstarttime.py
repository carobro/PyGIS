from matplotlib import pyplot as plt
import csv
import numpy as np
import matplotlib
from datetime import time

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
time_u_end = []
time_u_start = []

time_r_end = []
time_r_start = []
pm6 = "C:/Users/caro1/Downloads/PyGIS-master/PyGIS-master/analysis/results6pm.csv"
pm7 = "C:/Users/caro1/Downloads/PyGIS-master/PyGIS-master/analysis/results7pm.csv"
pm8 = "C:/Users/caro1/Downloads/PyGIS-master/PyGIS-master/analysis/results8pm.csv" 
pm = []
pm = [pm6,pm7,pm8]

for i in pm:
    print(i)
    with open(i, 'r') as file:
        reader = csv.reader(file)
        name = next(reader)[1]
        for row in reader:
            print(row[2])
            if (row[4] == 'rural'):
                hoursinminutes_r = int(row[2][0:2])*60
                print(row[2][3:5])
                time_r = hoursinminutes_r + int(row[2][3:5])
                start_r.append(time_r/60)
                
                hoursinminutes_r_end = int(row[3][0:2])*60
                time_r_end = hoursinminutes_r_end + int(row[3][3:5])
                end_r.append(time_r_end/60)

            else: 
                hoursinminutes_u = int(row[2][0:2])*60
                print(row[2][3:5])
                time_u = hoursinminutes_u + int(row[2][3:5])
                start_u.append(time_u/60)
                
                hoursinminutes_u_end = int(row[3][0:2])
                time_u_end = hoursinminutes_u_end + int(row[3][3:5])
                end_u.append(time_u_end/60)
                
    print(start_u)
    print(start_r)
    print(end_u)
    print(end_r)

    mean_u_start = round(sum(start_u)/len(start_u), 3)
    print("Mean urban starttime is:")
    print(mean_u_start)
    mean_u_end = round(sum(end_u)/len(end_u), 3)
    print("Mean urban endtime is:")
    print(mean_u_end)

    mean_r_start = round(sum(start_r)/len(start_r),3)
    print("Mean rural starttime is:")
    print(mean_r_start)
    mean_r_end = round(sum(end_r)/len(end_r), 3)
    print("Mean rural endtime is:")
    print(mean_r_end)


    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.boxplot([start_u, start_r])
    ax1.set_title('Start Owl Hunting')

    ax2.boxplot([end_u, end_r])
    ax2.set_title('End Owl Hunting')

    ax1.set_ylabel("Time")
    fig.suptitle('Owl Hunting Times')

    plt.show()