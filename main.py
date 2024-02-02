
# pip install openmeteo-requests requests-cache retry-requests numpy pandas prophet

from geopy.geocoders import Nominatim
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import datetime
from datetime import timedelta

from prophet import Prophet
import argparse

logistic_trend_values = {
  'relative_humidity_2m' : [0, 100]
}

# todo: взяти з аргументів місце, дату

#get_weather("Kyiv", "2024-01-28")

def get_weather(location, date_end, days = 10):

  endd = datetime.datetime.strptime(date_end, "%Y-%m-%d")
  today = datetime.datetime.now()
  if today - timedelta(5) < endd:
    print("oh fuck, service dont have info about last 5 days ()") #todo
  startt = (endd - timedelta(days)).strftime("%Y-%m-%d")

  # Setup the Open-Meteo API client with cache and retry on error
  cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
  retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
  openmeteo = openmeteo_requests.Client(session = retry_session)

  # Make sure all required weather variables are listed here
  # The order of variables in hourly or daily is important to assign them correctly below
  url = "https://archive-api.open-meteo.com/v1/archive"
  # todo: перетворити місце на lat та lon, вставити нижче, також взяти дату нижче замість того що є end_date: дата, start_date: дата - (мінус) 10 днів

  #дата затримується на 5  днів
  geolocator = Nominatim(user_agent='myapplication')
  location = geolocator.geocode(location)
  print(location)



  params = {
    "latitude": location.latitude,
    "longitude": location.longitude,
    "start_date": startt,
    "end_date": date_end,
    "hourly": ["temperature_2m", "relative_humidity_2m"]
  }
  responses = openmeteo.weather_api(url, params=params)

  # Process first location. Add a for-loop for multiple locations or weather models
  response = responses[0]
  print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
  print(f"Elevation {response.Elevation()} m asl")
  print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
  print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

  # Process hourly data. The order of variables needs to be the same as requested.
  hourly = response.Hourly()
  hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
  hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()

  hourly_data = {"date": pd.date_range(
    start = pd.to_datetime(hourly.Time(), unit = "s"),
    end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
    freq = pd.Timedelta(seconds = hourly.Interval()),
    inclusive = "left"
  )}
  hourly_data["temperature_2m"] = hourly_temperature_2m
  hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m

  hourly_dataframe = pd.DataFrame(data = hourly_data)
  #print(hourly_dataframe)
  return hourly_dataframe


def forecast(location, date_start, predict_days):

  df = get_weather(location, date_start, 30)
  df = df.dropna()
  result = pd.DataFrame()
  for column in df.columns.to_list()[1:]:
    train_df = pd.DataFrame()
    train_df['ds'] = df['date']
    train_df['y'] = df[column]
    is_logistic = column in logistic_trend_values

    if(is_logistic):
      train_df['floor'] = logistic_trend_values[column][0]
      train_df['cap'] = logistic_trend_values[column][1]

    model = Prophet(growth= "logistic" if is_logistic else "linear")
    model.fit(train_df)
    future = model.make_future_dataframe(periods = 24*(predict_days + 1), freq = 'H')

    if(is_logistic):
      future['floor'] = logistic_trend_values[column][0]
      future['cap'] = logistic_trend_values[column][1]
    forecast = model.predict(future)
    result['date'] = forecast['ds']
    result[column] = forecast['yhat']

  result = result[len(df.index):]
  result = result.reset_index()
  result = result.drop(columns=["index"])
  return result

parser = argparse.ArgumentParser()
parser.add_argument("location", default="Kyiv")
parser.add_argument("date", default="2024-01-25")
parser.add_argument("predict_days", default="5")

args = parser.parse_args()
locc = args.location
ddate = args.date

get_weather(locc, ddate)
print(args.predict_days)
print(forecast(locc, ddate, int(args.predict_days)))