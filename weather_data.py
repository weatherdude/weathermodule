import requests
import pandas as pd
import csv

# get weather data from visualcrossing - worldwide access to historical and forecast data

api_key = ''
start_date = '2022-01-22T15:00:00'     # date format yyyy-MM-dd or yyyy-MM-ddTHH:mm:ss (will be rounded to the closest hour)
end_date = '2022-01-22T15:00:00'

location = 'Braunschweig'
lat = 52.276187
lon = 10.538474
unitGroup = 'metric' # Supported values are us, uk, metric, base - default US


url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+location+'/'+start_date+'/'+end_date+'?key='+api_key+'&unitGroup='+unitGroup+'&include=alerts'
data = requests.get(url)
data = data.json()

#data['days']
#data['days'][0]['hours']

# forecast
url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Braunschweig?key='+api_key+'&unitGroup='+unitGroup+'&include=alerts'

# current conditions
url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+location+'?key='+api_key+'&unitGroup='+unitGroup+'&include=current'

def current_weather(lat,lon,unitGroup):
    # lat: latitude (°)
    # lon: longitude (°)

    latlon = str(lat)+','+str(lon)
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+latlon+'?key='+api_key+'&unitGroup='+unitGroup+'&include=current'
    data = requests.get(url)
    data = data.json()
    data_df = pd.DataFrame.from_dict(data['currentConditions']).iloc[0]
    temperature = data_df['temp']               # US = Fahrenheit; Metric = Celsius
    relative_humidity = data_df['humidity']     # (%)
    dew_point = data_df['dew']                  # US = Fahrenheit; Metric = Celsius
    precipitation = data_df['precip']           # US = Inches ; Metric = Millimeters
    snow = data_df['snow']                      # US = Inches ; Metric = Centimeters
    windgust = data_df['windgust']              # US = MpH ; Metric = KpH
    windspeed = data_df['windspeed']            # US = MpH ; Metric = KpH
    winddir = data_df['winddir']                # (°)
    pressure = data_df['pressure']              # Mb/hPa
    visibility = data_df['visibility']          # US = Miles ; Metric = KM
    cloudcover = data_df['cloudcover']          # (%)
    solarradiation = data_df['solarradiation']  # (W m-2)
    uvindex = data_df['uvindex']
    conditions = data_df['conditions']
    station_ID = data_df['stations']
    sunrise = data_df['sunrise']
    sunset = data_df['sunset']
    moonphase = data_df['moonphase']            # 0 = new moon ; 0.5 = full moon

    return temperature,relative_humidity,dew_point,precipitation,snow,windgust,windspeed,winddir,pressure,visibility,cloudcover,solarradiation,uvindex,conditions,station_ID,sunrise,sunset,moonphase


def weather_at_obs(start_date,end_date,lat,lon,unitGroup):
    # Get historical weather data for specific date and time

    # date format yyyy-MM-dd or yyyy-MM-ddTHH:mm:ss
    # lat: latitude (°)
    # lon: longitude (°)
    # unitGroup: Supported values are us, uk, metric, base - default is US
    # units for the variables can be looked up here: https://www.visualcrossing.com/resources/documentation/weather-api/unit-groups-and-measurement-units/

    latlon = str(lat)+','+str(lon)

    api_key = ''
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
