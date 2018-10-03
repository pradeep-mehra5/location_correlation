import time
import datetime
import os
from ctypes import *
from xlwt import Workbook
from auxiliary_fns import getDistance , getMeanCoordinates
from dbscan import dbscan

time_format = '%Y-%m-%d,%H:%M:%S'

class stayPoint(Structure):
    _fields_ = [
        ("latitude", c_double),
        ("longitude", c_double),
        ("arrival_time", c_uint64),
        ("leave_time", c_uint64)
    ]


#function to extract stay points from a GPS log file
#the function takes :
#       1. the name of the GPS file
#       2.threshold distance (here, = 200metres as default)
#       3.threshold time (here, = 20 minutes or 1200 seconds as default)
def stayPointExtraction(fileName, t_distance=200, t_time = 1200):
    stayPoints = [] #list of stay points
    with open(fileName) as logsFile:
        gpsPoints = logsFile.readlines()[6:]  # first 6 lines are useless
        num_of_points = len(gpsPoints)
        i = 0
        while i < num_of_points - 1:
            j = i+1
            while j < num_of_points:
                field_pointi = gpsPoints[i].rstrip().split(',')
                field_pointj = gpsPoints[j].rstrip().split(',')
                distance = getDistance(float(field_pointi[0]), float(field_pointi[1]),float(field_pointj[0]),float(field_pointj[1]) )

                if distance > t_distance:  # distance becomes greater than the threshold distance
                    t_i = time.mktime(time.strptime(field_pointi[-2] + ',' + field_pointi[-1], time_format))
                    t_j = time.mktime(time.strptime(field_pointj[-2] + ',' + field_pointj[-1], time_format))
                    deltaT = t_j - t_i
                    if deltaT > t_time:
                        sp = stayPoint()
                        sp.latitude, sp.longitude = getMeanCoordinates(gpsPoints[i:j])
                        sp.arrival_time, sp.leave_time = int(t_i), int(t_j)
                        stayPoints.append(sp)
                    break
                j += 1
            i = j
    return stayPoints


def cluster_stay_points(all_spts):
    print('Clustering preprocessing has been started')
    all_lats = []
    all_longs = []
    all_cords = []
    for point in all_spts:
        all_lats.append(point[0])
        all_longs.append(point[1])
    all_cords.append(all_lats)
    all_cords.append(all_longs)
    dbscan(all_cords,200,10)

def main():
    all_spts = set({})
    count = 0
    print(f'Time: {datetime.datetime.now()} \nWriting in files..please wait for some time.The data is hugeeee..!!!')
    for dirname, dirnames, filenames in os.walk('Data'):
        filenum = len(filenames)
        for filename in filenames:
            if filename.endswith('plt'):
                gpsfile = os.path.join(dirname, filename)
                spt = stayPointExtraction(gpsfile)
                if len(spt) > 0:

                    spfile = gpsfile.replace('Data', 'StayPoint')
                    if not os.path.exists(os.path.dirname(spfile)):
                        os.makedirs(os.path.dirname(spfile))

                    # for writing in a plt file
                    # with open(spfile,'w+') as spfile_handle:
                    #     spfile_handle.write('Extracted stay points:\longitude\t\tlatitude\t\tarriving time\t\tleaving time\n')
                    #
                    #     for sp in spt:
                    #         spfile_handle.write(str(sp.latitude) +"\t"+ str(sp.longitude)+"\t"+ str(time.strftime(time_format, time.localtime(
                    #     sp.arrival_time)))+ "\t"+str(time.strftime(time_format, time.localtime(sp.leave_time))) +"\n")

                    wb = Workbook()
                    sheet1 = wb.add_sheet((os.path.splitext(os.path.basename(spfile))[0]))
                    sheet1.write(0,0,"Latitude")
                    sheet1.write(0,1,"Longitude")
                    sheet1.write(0,2,"Arrival Time")
                    sheet1.write(0,3,"Leave Time")
                    row = 1
                    col = 0
                    for sp in spt:
                        latlong = (sp.latitude,sp.longitude)
                        all_spts.add(latlong)
                        sheet1.write(row, col, str(sp.latitude))
                        sheet1.write(row, col+1 , str(sp.longitude))
                        sheet1.write(row,col+2, str(time.strftime(time_format, time.localtime(sp.arrival_time))))
                        sheet1.write(row,col+3, str(time.strftime(time_format, time.localtime(sp.leave_time))))
                        row+=1
                    wb.save(os.path.join(
                        os.path.dirname(spfile) + '/' + (os.path.splitext(os.path.basename(spfile))[0]) + '.xls'))
    print(f'\n\nTime: {datetime.datetime.now()}\nAll staypoints are:\n{all_spts}')
    cluster_stay_points(all_spts)

if __name__ == '__main__':
    main()