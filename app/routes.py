#!/usr/bin/python3
from flask import current_app as app
from flask import jsonify
from flask import render_template, request
import requests
from datetime import datetime


def calvin_to_celsius(temp):
    """Converts temperature from
      Kelvin to Celsius."""
    return temp - 273.15


def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    with open(".api_key", "r") as f:
        api_key = f.read()
    url = base_url + 'appid=' + api_key + '&q=' + city
    response = requests.get(url).json()

    if response.get('cod') != 200:
        return None

    wind_speed = response['wind']['speed']
    temp = response['main']['temp']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    icon = response['weather'][0]['icon']
    temp_c = int(calvin_to_celsius(temp))
    temp_min = int(calvin_to_celsius(response['main']['temp_min']))
    temp_max = int(calvin_to_celsius(response['main']['temp_max']))
    weather_data = {
            'city': city,
            'wind_speed': wind_speed,
            'temperature': temp_c,
            'humidity': humidity,
            'description': description,
            'temp_min': temp_min,
            'temp_max': temp_max,
            'icon': icon
        }

    return weather_data

def get_forecast(city):
    base_url = "https://api.openweathermap.org/data/2.5/forecast?"
    with open(".api_key", "r") as f:
        api_key = f.read()
    url = base_url + 'appid=' + api_key + '&q=' + city
    response = requests.get(url).json()

    if response.get('cod') != '200':
        return None

    forecast_data = []
    for forecast in response['list']:
        date_time = forecast['dt_txt']
        temp = forecast['main']['temp']
        temp_c = int(calvin_to_celsius(temp))
        description = forecast['weather'][0]['description']
        icon = forecast['weather'][0]['icon']
        forecast_data.append({
            'date_time': date_time,
            'temperature': temp_c,
            'description': description,
            'icon': icon
        })
        if len(forecast_data) == 3:
            break


    return forecast_data


@app.route('/')
def index():
   
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
        city = request.form['city']
        weather_data = get_weather(city)
        return jsonify(weather_data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

