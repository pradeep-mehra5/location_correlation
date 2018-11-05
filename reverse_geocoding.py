import requests
from auxiliary_fns import getLocationFromSPs
from xlwt import Workbook
import datetime

#for mapping clusterID with Location
LOCATION_DICT = {}

#for mapping clusterID with mean coordinates
CLUSTER_MEAN = {}

def getAddress(latitude,longitude):
    sensor = 'true'
    key = "&key=AIzaSyBxWpE_8OK5pA0NaFvx00KOdk1ZFfQxVIc"
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor={sen}".format(
        lat=latitude,
        lon=longitude,
        sen=sensor
    )
    url = "{base}{params}{key}".format(base=base, params=params , key=key)
    response = requests.get(url)
    if len(response.json()['results'])==0:
        return f"Error fetching location for Latitude :{latitude} Longitude :{longitude}. Error Message :{response.json()['error_message']}"
    else:
        return response.json()['results'][0]['formatted_address']


#   for creating a dictionary of locations mapping locations with their clusterID
def createLocationDictionary(CLUSTER_DICT):
    print(f'\n\nTime: {datetime.datetime.now()}')
    print("Creating location dictionary")
    for clusterID in CLUSTER_DICT:
        CLUSTER_MEAN[clusterID] = getLocationFromSPs(CLUSTER_DICT[clusterID])
    print(CLUSTER_MEAN)

    for clusterID in CLUSTER_MEAN:
        LOCATION_DICT[clusterID] = getAddress(CLUSTER_MEAN[clusterID][0],CLUSTER_MEAN[clusterID][1])
    print(LOCATION_DICT)
    storeInFile(LOCATION_DICT,CLUSTER_MEAN)


#   writing the data in file
def storeInFile(LOCATION_DICT,CLUSTER_MEAN):
    print(f'\n\nTime: {datetime.datetime.now()}\nWriting Locations into Files')
    wb = Workbook()
    locationSheet = wb.add_sheet('Locations')
    locationSheet.write(0,0,'LocationID(ClusterID)')
    locationSheet.write(0,1,'Latitude')
    locationSheet.write(0,2,'Longitude')
    locationSheet.write(0,3,'Location Address')

    row = 1
    for clusterId in CLUSTER_MEAN:
        locationSheet.write(row,0,str(clusterId))
        locationSheet.write(row,1,str(CLUSTER_MEAN[clusterId][0]))
        locationSheet.write(row,2,str(CLUSTER_MEAN[clusterId][1]))
        locationSheet.write(row,3,str(LOCATION_DICT[clusterId]))
        row+=1
    wb.save('locations.xls')