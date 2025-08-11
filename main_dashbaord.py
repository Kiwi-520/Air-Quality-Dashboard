from click import progressbar
from api_functions import get_air_quality_data
from aqi_utils import create_aqi_gauge, get_aqi_info
import streamlit as st
import time
import plotly.express as px
import pandas as pd
def main():
    # Sidebar for city selection
    st.sidebar.header("🏙️ City Selection")
    
    # Predefined cities
    popular_cities = ["New York", "London", "Tokyo", "Delhi", "Beijing", "Los Angeles", "Mumbai", "São Paulo"]
    
    selected_cities = st.sidebar.multiselect(
        "Select cities to monitor:",
        popular_cities,
        default=["New York", "London", "Tokyo"]
    )
    
    # Custom city input
    custom_city = st.sidebar.text_input("Add custom city:")
    if custom_city:
        selected_cities.append(custom_city)
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("Auto-refresh (every 5 minutes)")
    
    if auto_refresh:
        st.sidebar.write("⏱️ Auto-refreshing...")
        time.sleep(1)
        st.rerun()
    
    # Fetch data for selected cities
    if selected_cities:
        city_data = []
        
        # Progress bar
        progress_bar = st.progress(0)
        for i, city in enumerate(selected_cities):
            data = get_air_quality_data(city)
            if data:
                city_data.append(data)
            progress_bar.progress((i + 1) / len(selected_cities))
        
        progress_bar.empty()
        
        if city_data:
            display_dashboard(city_data)
    else:
        st.info("👆 Please select cities from the sidebar to start monitoring!")

def display_dashboard(city_data):
    # Current AQI Overview
    st.header("🌍 Current Air Quality Status")
    
    cols = st.columns(len(city_data))
    for i, data in enumerate(city_data):
        with cols[i]:
            aqi_info = get_aqi_info(data['aqi'])
            st.metric(
                label=data['city'],
                value=f"AQI: {data['aqi']}",
                delta=aqi_info['category']
            )
            st.plotly_chart(create_aqi_gauge(data['aqi'], data['city']), use_container_width=True)
    
    # Detailed pollutant comparison
    st.header("🧪 Pollutant Levels Comparison")
    
    df = pd.DataFrame(city_data)
    
    # Create comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        # PM2.5 comparison
        fig_pm25 = px.bar(df, x='city', y='pm2_5', title='PM2.5 Levels (μg/m³)')
        fig_pm25.update_traces(marker_color='orange')
        st.plotly_chart(fig_pm25, use_container_width=True)
    
    with col2:
        # PM10 comparison
        fig_pm10 = px.bar(df, x='city', y='pm10', title='PM10 Levels (μg/m³)')
        fig_pm10.update_traces(marker_color='red')
        st.plotly_chart(fig_pm10, use_container_width=True)
    
    # Health recommendations
    st.header("💡 Health Recommendations")
    for data in city_data:
        aqi_info = get_aqi_info(data['aqi'])
        st.write(f"**{data['city']}**: {aqi_info['health']}")
    
    # Data table
    st.header("📊 Detailed Data")
    st.dataframe(df[['city', 'aqi', 'pm2_5', 'pm10', 'no2', 'o3', 'co']])

if __name__ == "__main__":
    main()