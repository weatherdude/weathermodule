import requests
import pandas as pd
import csv

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
Lat = 39.7456
Lon = -97.0892

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

# get latest observation of a weather station

url = "https://api.weather.gov/stations/KPHX/observations/latest"
data = requests.get(url)
data = data.json()

keys = ['temperature', 'dewpoint', 'windDirection', 'windSpeed','windSpeed','windGust','barometricPressure','seaLevelPressure','visibility','maxTemperatureLast24Hours','minTemperatureLast24Hours','precipitationLastHour',
'precipitationLast3Hours','precipitationLast6Hours','relativeHumidity','windChill','heatIndex']
data_selection= {x:data['properties'][x] for x in keys}

data_df = pd.DataFrame.from_dict(data_selection)
data_df.to_csv('presentweather.csv',index=True)
data_df.to_excel("presentweather.xlsx",index=True)

with open('presentweather.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in data['properties'].items():
       writer.writerow([key, value])
