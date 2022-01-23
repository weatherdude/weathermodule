import requests
import pandas as pd
import csv

# get weather data from visualcrossing - worldwide access to historical and forecast data

api_key = 'GSBMDJLRQK5P7UK5UEKEXQTR4'
start_date = '2022-01-22T15:00:00'     # date format yyyy-MM-dd or yyyy-MM-ddTHH:mm:ss (will be rounded to the closest hour)
end_date = '2022-01-22T15:00:00'

location = 'Braunschweig'

unitGroup = 'metric' # Supported values are us, uk, metric, base - default US


url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+location+'/'+start_date+'/'+end_date+'?key='+api_key+'&unitGroup='+unitGroup+'&include=alerts'
data = requests.get(url)
data = data.json()

#data['days']
#data['days'][0]['hours']

# forecast
url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Braunschweig?key='+api_key+'&unitGroup='+unitGroup+'&include=alerts'

def weather_at_obs(start_date,end_date,lat,lon,unitGroup):
    # Get historical weather data for specific date and time

    # date format yyyy-MM-dd or yyyy-MM-ddTHH:mm:ss
    # lat: latitude (°)
    # lon: longitude (°)
    # unitGroup: Supported values are us, uk, metric, base - default is US
    # units for the variables can be looked up here: https://www.visualcrossing.com/resources/documentation/weather-api/unit-groups-and-measurement-units/

    latlon = str(lat)+','+str(lon)

    api_key = 'GSBMDJLRQK5P7UK5UEKEXQTR4'
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+location+'/'+start_date+'/'+end_date+'?key='+api_key+'&unitGroup='+unitGroup+'&include=alerts'
    data = requests.get(url)
    data = data.json()

    data_df = pd.DataFrame.from_dict(data['days'])
    data_df.to_csv('weather_at_obs.csv',index=False)
    data_df.to_excel("weather_at_obs.xlsx",index=False)

def weather_forecast(lat,lon,unitGroup):
    # Get weather forecast for the next 14 days

    # date format yyyy-MM-dd or yyyy-MM-ddTHH:mm:ss
    # lat: latitude (°)
    # lon: longitude (°)
    # unitGroup: Supported values are us, uk, metric, base - default is US
    # units for the variables can be looked up here: https://www.visualcrossing.com/resources/documentation/weather-api/unit-groups-and-measurement-units/

    latlon = str(lat)+','+str(lon)
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+latlon+'?key=YOUR_API_KEY'
    alerts = data['alerts']
    data_df = pd.DataFrame.from_dict(data['days'])
    data_df.to_csv('weather_forecast.csv',index=False)
    data_df.to_excel("weather_forecast.xlsx",index=False)