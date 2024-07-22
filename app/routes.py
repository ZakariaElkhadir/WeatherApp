#!/usr/bin/python3
from flask import current_app as app
from flask import jsonify, render_template, request
import requests
from datetime import datetime, timedelta

"""This module contains the routes and
utility functions for the Weather App."""


def calvin_to_celsius(temp):
    """
    Converts temperature from Kelvin to Celsius.

    Parameters:
        temp (float): Temperature in Kelvin.

    Returns:
        float: Temperature in Celsius.
    """
    return temp - 273.15


def get_weather(city):
    """
    Gets the current weather data for a specified city.

    Parameters:
        city (str): The name of the city.

    Returns:
        dict: A dictionary containing current weather data for the city,
              or None if the city is not found or an error occurs.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    with open(".api_key", "r") as f:
        api_key = f.read().strip()  # Strip any extraneous whitespace
    url = f"{base_url}appid={api_key}&q={city}"
    response = requests.get(url).json()

    # Check if the API request was successful
    if response.get('cod') != 200:
        return None

    # Extract relevant data from the response
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
    """
    Gets the weather forecast for the next few days for a specified city.

    Parameters:
        city (str): The name of the city.

    Returns:
        list: A list of dictionaries containing
        weather forecast data for the city,
        or None if the city is not found or an error occurs.
    """
    base_url = "https://api.openweathermap.org/data/2.5/forecast?"
    with open(".api_key", "r") as f:
        api_key = f.read().strip()  # Strip any extraneous whitespace
    url = f"{base_url}appid={api_key}&q={city}"
    response = requests.get(url).json()

    # Check if the API request was successful
    if response.get('cod') != '200':
        return None

    forecast_data = []
    today = datetime.utcnow().date()
    processed_dates = set()

    # Process the forecast data
    for forecast in response['list']:
        date_time = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
        # Skip forecasts for today or duplicate dates
        if date_time.date() <= today or date_time.date() in processed_dates:
            continue

        temp = forecast['main']['temp']
        temp_c = int(calvin_to_celsius(temp))
        description = forecast['weather'][0]['description']
        icon = forecast['weather'][0]['icon']

        forecast_data.append({
            'date': date_time.date().strftime('%Y-%m-%d'),
            'temperature': temp_c,
            'description': description,
            'icon': icon
        })
        processed_dates.add(date_time.date())

        # Limit the forecast to 3 days
        if len(processed_dates) == 3:
            break

    return forecast_data


@app.route('/')
def index():
    """Renders the index page."""
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
    """
    Handles the weather data request for a city.

    Gets the current weather data and the forecast for the specified city.

    Returns:
        json: A JSON response containing the weather and forecast data,
              or an error message if the data cannot be retrieved.
    """
    city = request.form['city']
    weather_data = get_weather(city)
    forecast_data = get_forecast(city)

    if weather_data is None:
        return jsonify({"error": "Could not get current weather data."}), 500
    if forecast_data is None:
        weather_data['forecast'] = []
    else:
        weather_data['forecast'] = forecast_data

    return jsonify(weather_data)


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html')


@app.context_processor
def inject_now():
    """
    Injects the current time into all templates.

    Returns:
        dict: A dictionary containing the current time.
    """
    return {'now': datetime.utcnow()}
