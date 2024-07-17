#!/usr/bin/python3
from app import create_app
"""the run.py module runs the Weather App."""


def run_weather_app():
    """
    Runs the Weather App.

    This function creates an instance of the Weather
    App using the create_app() function from the app module.
    It then runs the app in debug mode.

    Parameters:
    None

    Returns:
    None
    """
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    run_weather_app()
