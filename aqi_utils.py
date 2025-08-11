import plotly.graph_objects as go
def get_aqi_info(aqi_level):
    """Return AQI category and health recommendations"""
    aqi_categories = {
        1: {"category": "Good", "color": "#00E400", "health": "Air quality is satisfactory"},
        2: {"category": "Fair", "color": "#FFFF00", "health": "Acceptable for most people"},
        3: {"category": "Moderate", "color": "#FF7E00", "health": "Sensitive individuals may experience symptoms"},
        4: {"category": "Poor", "color": "#FF0000", "health": "Health warnings of emergency conditions"},
        5: {"category": "Very Poor", "color": "#8F3F97", "health": "Health alert: everyone may experience serious effects"}
    }
    return aqi_categories.get(aqi_level, aqi_categories[1])

def create_aqi_gauge(aqi_value, city_name):
    """Create a gauge chart for AQI"""
    aqi_info = get_aqi_info(aqi_value)
    
    fig = go.Figure(go.Indicator( # type: ignore
        mode = "gauge+number+delta",
        value = aqi_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"AQI - {city_name}"},
        gauge = {
            'axis': {'range': [None, 5]},
            'bar': {'color': aqi_info['color']},
            'steps': [
                {'range': [0, 1], 'color': "#00E400"},
                {'range': [1, 2], 'color': "#FFFF00"},
                {'range': [2, 3], 'color': "#FF7E00"},
                {'range': [3, 4], 'color': "#FF0000"},
                {'range': [4, 5], 'color': "#8F3F97"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 4
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig