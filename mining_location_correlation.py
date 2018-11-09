import global_vars
import os
import xlrd
from auxiliary_fns import getTimeStamp

def location_correlation():
    correlation = []
    tripPartitionTime = 60*60*5
    b = 1
    locationsNum = len(global_vars.LOCATION_DICT)
    empty = [0]*locationsNum
    for count in range(0,locationsNum):
        correlation.append(empty)

    for dirname,dirnames,filenames in os.walk('Location_History'):
        for filename in filenames:
            history = {}
            wb = xlrd.open_workbook(os.path.join(dirname,filename))
            sheet = wb.sheet_by_index(0)
            row_count = sheet.nrows
            for row_num in range(1,row_count):
                arrival_time = sheet.cell_value(row_num,2)
                leave_time = sheet.cell_value(row_num,3)
                key = (arrival_time,leave_time)
                val = int(sheet.cell_value(row_num,4))
                history[key] = val
            trips = TripPartition(history,tripPartitionTime)
            for trip in trips:
                for index1 in range(len(trip)):
                    for index2 in range(index1+1,len(trip)):
                        alpha = b**(-1*(index2-index1-1))
                        correlation[trip[index1]-1][trip[index2]-1] += alpha
    print(correlation)
    return correlation
location_correlation()


def TripPartition(history,tripPartitionTime):
    trips = []
#     timeStampedHistory = {}
#     for h in history:
#         ts1 = getTimeStamp(h[0])
#         ts2 = getTimeStamp(h[1])
#         timeStampedHistory[(ts1,ts2)] = history[h]
#     prevtime =
#     for tsh in timeStampedHistory:
#         if tsh[]
#         prevtime = tsh[1]
    return trips