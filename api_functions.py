import requests
import streamlit as st
import pandas as pandas
import numpy as numpy
# import matplotlin=b.pyplot as pyplot
import plotly.express as px
from datetime import date, datetime, timedelta
import time


API_KEY = '948c5aa53cbd3c18d24e95358f0a1b77'

@st.cache_data(ttl = 300) #cache for 5 minutes
def get_air_quality_data(city_name):
    '''Fetch air quality data from OpenWeatherMap'''
    try:
        # Get coordinates
        geo_url = f'https://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}'
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if not geo_data:
            return None

        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # Get air quality data
        api_url = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
        api_response = requests.get(api_url)
        api_data = api_response.json()

        components = api_data['list'][0]['components']
        
        return {
            'city': city_name,
            'aqi': api_data['list'][0]['main']['aqi'],
            'co': components.get('co', 0),
            'no2': components.get('no2', 0),
            'o3': components.get('o3', 0),
            'pm2_5': components.get('pm2_5', 0),
            'pm10': components.get('pm10', 0),
            'so2': components.get('so2', 0),
            'timestamp': datetime.now()
        }
    except Exception as e:
        st.error(f'Error fetching data for {city_name}: {str(e)}')
        return None


def get_pollutants_for_decision(city_name):
    """
    Fetch pollutant data formatted specifically for the decision engine.
    Returns a clean dictionary of pollutant concentrations.
    """
    data = get_air_quality_data(city_name)
    if not data:
        return None
    
    return {
        'pm2_5': data.get('pm2_5', 0),
        'pm10': data.get('pm10', 0),
        'o3': data.get('o3', 0),
        'no2': data.get('no2', 0),
        'co': data.get('co', 0),
        'so2': data.get('so2', 0)
    }