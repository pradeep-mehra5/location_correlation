import requests
import openpyxl
import xlrd


# wb = xlrd.open_workbook('/home/pradeep/Desktop/Minor_Project/locations.xlsx')
# sheet = wb.sheet_by_index(0)
# row_count = sheet.nrows
# temp = []
# print(f"total rows are :{row_count}\n")
# for row_num in range(1,row_count):
#     lat = float(sheet.cell_value(row_num, 1))
#     long = float(sheet.cell_value(row_num, 2))
#     latlong = (lat, long)
#     temp.append(latlong)
# print(f'{temp}\n')
#



########################## GOOGLE API ##############################
sensor = 'true'
key = "&key=AIzaSyCbb0jbXn2QIE3kXzrNxORoqkLji5CkxzI"

base = "https://maps.googleapis.com/maps/api/geocode/json?"
# for each in temp:
params = "latlng={lat},{lon}&sensor={sen}".format(
    lat=str(39.984702),
    lon=str(116.318417),
    sen=sensor
)
url = "{base}{params}{key}".format(base=base, params=params , key=key)
response = requests.get(url)
print(f'{response.json()["results"][0]["types"]}\n')
