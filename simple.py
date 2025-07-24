import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# Page setup
st.set_page_config(page_title="Air Quality Monitor", page_icon="🌬️", layout="wide")
st.title("🌬️ Air Quality Monitor Dashboard")
st.markdown("Real-time air quality tracking across cities")

# Sidebar
st.sidebar.title("🏙️ Settings")
st.sidebar.markdown("---")

# City selection
cities = ["New York", "London", "Tokyo", "Delhi", "Beijing", "Mumbai", "Sydney", "Paris"]
selected_cities = st.sidebar.multiselect(
    "Choose cities to monitor:",
    cities,
    default=["New York", "London", "Tokyo"]
)

# Generate sample data function
def create_sample_data(cities):
    data = []
    for city in cities:
        aqi = random.randint(1, 5)
        data.append({
            'City': city,
            'AQI': aqi,
            'PM2.5': random.randint(10, 100),
            'PM10': random.randint(20, 150),
            'NO2': random.randint(5, 80),
            'O3': random.randint(30, 120),
            'Status': ['Good', 'Fair', 'Moderate', 'Poor', 'Very Poor'][aqi-1],
            'Color': ['#00E400', '#FFFF00', '#FF7E00', '#FF0000', '#8F3F97'][aqi-1]
        })
    return pd.DataFrame(data)

# Main content
if selected_cities:
    # Generate data
    df = create_sample_data(selected_cities)
    
    # Display metrics
    st.header("📊 Current Air Quality")
    cols = st.columns(len(selected_cities))
    
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i]:
            st.metric(
                label=row['City'],
                value=f"AQI: {row['AQI']}",
                delta=row['Status']
            )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(df, x='City', y='AQI', title='Air Quality Index by City',
                     color='AQI', color_continuous_scale='RdYlBu_r')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(df, x='City', y='PM2.5', title='PM2.5 Levels',
                     color='PM2.5', color_continuous_scale='Reds')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Data table
    st.header("📋 Detailed Data")
    st.dataframe(df[['City', 'AQI', 'Status', 'PM2.5', 'PM10', 'NO2', 'O3']], 
                use_container_width=True)
    
    # Health recommendations
    st.header("💡 Health Recommendations")
    for _, row in df.iterrows():
        if row['AQI'] <= 2:
            advice = "✅ Good air quality. Safe for outdoor activities."
        elif row['AQI'] == 3:
            advice = "⚠️ Moderate air quality. Sensitive people should limit outdoor activities."
        else:
            advice = "🚨 Poor air quality. Avoid outdoor activities and use masks."
        
        st.write(f"**{row['City']}**: {advice}")
    
    # Refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()
        
else:
    st.info("👆 Please select cities from the sidebar to start monitoring!")

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")