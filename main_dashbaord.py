from click import progressbar
from api_functions import get_air_quality_data, get_pollutants_for_decision
from aqi_utils import create_aqi_gauge, get_aqi_info
from decision_engine import (
    calculate_activity_risk, 
    get_decision_recommendation,
    create_risk_gauge,
    create_contribution_chart,
    get_pollutant_comparison_table,
    get_activity_list,
    get_top_risk_drivers
)
import streamlit as st
import time
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Air Quality Decision Engine",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title and description
st.title("🎯 Air Quality Decision Engine")
st.markdown("""
**From Monitoring to Decision-Making** | Transform air quality data into actionable recommendations

This intelligent system uses **Multi-Criteria Decision Analysis (MCDA)** to provide prescriptive 
go/no-go recommendations for outdoor activities based on real-time air quality data.
""")
st.markdown("---")

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
    
    # ==========================================
    # DECISION ENGINE SECTION
    # ==========================================
    st.sidebar.markdown("---")
    st.sidebar.header("🎯 Decision Engine")
    st.sidebar.markdown("*Activity recommendations*")
    
    # Activity selection
    activity = st.sidebar.selectbox(
        "What activity are you planning?",
        get_activity_list(),
        help="Select your planned outdoor activity to get a personalized risk assessment"
    )
    
    # City selection for decision
    decision_cities = selected_cities if selected_cities else popular_cities
    city_for_decision = st.sidebar.selectbox(
        "Which city?",
        options=decision_cities,
        key="decision_city",
        help="Select the city where you plan to do this activity"
    )
    
    # Decision button
    decision_button = st.sidebar.button("🚀 Get Recommendation", type="primary", use_container_width=True)
    
    # Add explanation
    with st.sidebar.expander("ℹ️ How does this work?"):
        st.markdown("""
        The **Decision Engine** uses a sophisticated rule-based model that:
        
        1. **Analyzes** real-time pollutant data (PM2.5, PM10, O3, NO2, CO)
        2. **Calculates** activity-specific risk scores using weighted sensitivity profiles
        3. **Compares** values against WHO Air Quality Guidelines
        4. **Delivers** prescriptive go/no-go recommendations
        
        Each activity has different pollutant sensitivity based on respiratory rate and exposure duration.
        """)
    
    st.sidebar.markdown("---")
    
    if auto_refresh:
        st.sidebar.write("⏱️ Auto-refreshing...")
        time.sleep(1)
        st.rerun()
    
    # ==========================================
    # HANDLE DECISION BUTTON CLICK
    # ==========================================
    if decision_button:
        display_decision_engine(activity, city_for_decision)
        st.markdown("---")
    
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


def display_decision_engine(activity: str, city: str):
    """
    Display the decision engine results with prescriptive recommendations.
    This transforms the dashboard from monitoring to decision-making.
    """
    st.header("🎯 Decision Engine: Activity Risk Assessment")
    st.markdown(f"**Activity:** {activity} | **Location:** {city}")
    
    # Fetch pollutant data
    with st.spinner(f"Analyzing air quality data for {city}..."):
        pollutant_data = get_pollutants_for_decision(city)
    
    if not pollutant_data:
        st.error(f"❌ Unable to fetch air quality data for {city}. Please try another city.")
        return
    
    # Calculate risk using decision engine
    try:
        risk_score, contributions, normalized = calculate_activity_risk(activity, pollutant_data)
        decision = get_decision_recommendation(risk_score, activity)
    except Exception as e:
        st.error(f"❌ Error in decision calculation: {str(e)}")
        return
    
    # ==========================================
    # MAIN DECISION OUTPUT
    # ==========================================
    st.markdown("---")
    
    # Display decision with appropriate styling
    if decision['decision'] == 'GO':
        st.success(decision['recommendation'])
    elif decision['decision'] == 'CAUTION':
        st.warning(decision['recommendation'])
    else:  # STOP
        st.error(decision['recommendation'])
    
    st.markdown("---")
    
    # ==========================================
    # VISUAL ANALYTICS
    # ==========================================
    st.subheader("📊 Risk Analysis Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk gauge
        st.plotly_chart(create_risk_gauge(risk_score, activity), use_container_width=True)
        
        # Key metrics
        st.metric(
            label="Overall Risk Score",
            value=f"{risk_score:.3f}",
            delta=f"{decision['level']}",
            delta_color="inverse" if decision['decision'] == 'GO' else "normal"
        )
    
    with col2:
        # Pollutant contribution breakdown
        st.plotly_chart(create_contribution_chart(contributions), use_container_width=True)
    
    # ==========================================
    # DATA TRANSPARENCY
    # ==========================================
    st.subheader("🔬 Data Used for This Decision")
    
    # Comparison table
    comparison_df = get_pollutant_comparison_table(pollutant_data, normalized)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    # Top risk drivers
    st.subheader("⚠️ Primary Risk Drivers")
    top_drivers = get_top_risk_drivers(contributions, top_n=3)
    
    cols = st.columns(3)
    for i, (pollutant, contribution) in enumerate(top_drivers):
        with cols[i]:
            pollutant_display = pollutant.upper().replace('_', '.')
            st.metric(
                label=f"#{i+1}: {pollutant_display}",
                value=f"{contribution:.3f}",
                help=f"Weighted contribution to overall risk score"
            )
    
    # ==========================================
    # DECISION METHODOLOGY
    # ==========================================
    with st.expander("🧠 Decision Methodology & Model Details"):
        st.markdown(f"""
        ### Risk Scoring Model
        
        **Model Type:** Rule-based multi-criteria decision analysis (MCDA)
        
        **Calculation Steps:**
        1. **Normalization:** Each pollutant concentration is normalized against WHO Air Quality Guidelines
        2. **Weighting:** Activity-specific weights are applied based on pollutant sensitivity
        3. **Aggregation:** Weighted sum produces the final risk score
        
        **Activity Sensitivity Profile for "{activity}":**
        """)
        
        # Show weights for this activity
        from decision_engine import ACTIVITY_WEIGHTS
        weights = ACTIVITY_WEIGHTS[activity]
        weight_df = pd.DataFrame([
            {"Pollutant": k.upper().replace('_', '.'), "Sensitivity Weight": f"{v:.2f}"}
            for k, v in weights.items()
        ])
        st.table(weight_df)
        
        st.markdown("""
        ### Decision Thresholds
        - **< 0.8:** LOW RISK → Proceed with activity
        - **0.8 - 1.5:** MODERATE RISK → Proceed with caution
        - **> 1.5:** HIGH RISK → Activity not recommended
        
        ### Why This Matters
        This model transforms raw environmental data into **actionable intelligence** by:
        - Contextualizing risk based on specific use cases
        - Providing transparent, explainable recommendations
        - Enabling proactive health decisions
        """)
    
    # Export option
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Create decision summary for export
        decision_summary = {
            "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "City": city,
            "Activity": activity,
            "Risk Score": risk_score,
            "Decision": decision['decision'],
            "Risk Level": decision['level'],
            **{f"{k.upper()}": v for k, v in pollutant_data.items()}
        }
        
        decision_df = pd.DataFrame([decision_summary])
        csv = decision_df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Decision Report",
            data=csv,
            file_name=f"decision_report_{city}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )


if __name__ == "__main__":
    main()