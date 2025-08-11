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

        return {
            'city': city_name,
            'aqi': api_data['list'][0]['main']['aqi'],
            'co': api_data['list'][0]['components']['co'],
            'no2': api_data['list'][0]['components']['no2'],
            'o3': api_data['list'][0]['components']['o3'],
            'pm2_5': api_data['list'][0]['components']['pm2_5'],
            'pm10': api_data['list'][0]['components']['pm10'],
            'timestamp': datetime.now()
        }
    except Exception as e:
        st.error(f'Error fetching data for {city_name}: {str(e)}')
        return None