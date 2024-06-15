#!/usr/bin/python3
from flask import Flask
import requests



def calvin_to_celsius(temp):
    """Converts temperature from
      Kelvin to Celsius."""
    
    return temp - 273.15


def get_weather():
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    city = "Casablanca"
    api_key = open(".api_key", "r").read()
    url = base_url + 'appid=' + api_key + '&q=' + city
    response = requests.get(url).json()

    wind_speed = response['wind']['speed']
    temp = response['main']['temp']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    temp_c = calvin_to_celsius(temp)

    weather_data = {
          'city': city,
          'wind_speed': wind_speed,
          'temperature': temp_c,
          'humidity': humidity,
          'description': description
      }

    return weather_data



