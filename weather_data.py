import requests
import pandas as pd

#url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/locations"

#data = requests.get(url)
#data = data.json()

# NOAA weather API

def get_noaa_data(url, data_type, header):

    data = requests.get(url, data_type, headers=header)
    data = data.json()
    print(data)


token = 'nFkmRqoPvCvOQMsWSGMhHsmKVzRrIemZ'
creds = dict(token=token)
dtype = 'dataset'
url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'

get_noaa_data(url, dtype, creds)


# NWS weather API

# get info about correct end points with Lat, Lon
url = "https://api.weather.gov/points/39.7456,-97.0892"
data = requests.get(url)
data = data.json()

gridX = data['properties']['gridX']
gridY = data['properties']['gridY']
office = data['properties']['cwa']

# get weather forecast
# structure: https://api.weather.gov/gridpoints/{office}/{grid X},{grid Y}/forecast
url = "https://api.weather.gov/gridpoints/"+str(office)+"/"+str(gridX)+","+str(gridY)+"/forecast"

data = requests.get(url)
data = data.json()


data_df = pd.DataFrame.from_dict(data['properties']['periods'])
data_df.to_csv('forecast.csv',index=False)
data_df.to_excel("forecast.xlsx",index=False)
