#!/usr/bin/python3
from flask import current_app as app
from flask import render_template, request
import requests
from datetime import datetime


def calvin_to_celsius(temp):
    """Converts temperature from
      Kelvin to Celsius."""
    return temp - 273.15


def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    # city = "Casablanca"
    api_key = open(".api_key", "r").read()
    url = base_url + 'appid=' + api_key + '&q=' + city
    response = requests.get(url).json()

    if response.get('cod') != 200:
        return None

    wind_speed = response['wind']['speed']
    temp = response['main']['temp']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
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
            'temp_max': temp_max
        }

    return weather_data


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.form.get('city'):
        city = request.form.get('city')
        weather_data = get_weather(city)
    return render_template('index.html', weather_data=weather_data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}
