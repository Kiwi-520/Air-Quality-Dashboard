"""
Decision Engine for Air Quality Risk Assessment
------------------------------------------------
A rule-based decision model that calculates activity-specific risk scores
based on pollutant concentrations and provides prescriptive recommendations.

Author: Kiwi-520
Purpose: Advanced Air Quality Decision Intelligence
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Tuple


# WHO Air Quality Guidelines (μg/m³)
WHO_GUIDELINES = {
    'pm2_5': 25.0,  # 24-hour mean
    'pm10': 50.0,   # 24-hour mean
    'o3': 100.0,    # 8-hour mean
    'no2': 40.0,    # Annual mean
    'co': 10000.0,  # 8-hour mean
    'so2': 40.0     # 24-hour mean
}

# Activity-specific sensitivity weights
# Each activity has different sensitivity to pollutants based on:
# - Respiratory rate (higher during exercise)
# - Duration of exposure
# - Vulnerability of target population
ACTIVITY_WEIGHTS = {
    "Strenuous Exercise (e.g., running, cycling)": {
        "pm2_5": 0.50,  # High sensitivity - deep breathing increases particle intake
        "pm10": 0.20,   # Moderate sensitivity - larger particles
        "o3": 0.20,     # High sensitivity - ozone damages lung tissue during exercise
        "no2": 0.05,    # Lower sensitivity
        "co": 0.05      # Lower sensitivity
    },
    "Moderate Activity (e.g., walking the dog)": {
        "pm2_5": 0.40,
        "pm10": 0.20,
        "o3": 0.25,
        "no2": 0.10,
        "co": 0.05
    },
    "Relaxing Outdoors (e.g., sitting in a park)": {
        "pm2_5": 0.25,  # Lower breathing rate
        "pm10": 0.15,
        "o3": 0.40,     # Ozone still matters for prolonged exposure
        "no2": 0.15,
        "co": 0.05
    },
    "Outdoor Event (e.g., party, picnic)": {
        "pm2_5": 0.30,
        "pm10": 0.20,
        "o3": 0.30,
        "no2": 0.15,
        "co": 0.05
    },
    "Children's Outdoor Play": {
        "pm2_5": 0.55,  # Children are more vulnerable
        "pm10": 0.25,
        "o3": 0.15,
        "no2": 0.03,
        "co": 0.02
    },
    "Commuting (walking/biking)": {
        "pm2_5": 0.35,
        "pm10": 0.20,
        "o3": 0.15,
        "no2": 0.20,    # Higher NO2 weight due to traffic exposure
        "co": 0.10
    }
}


def normalize_pollutant(value: float, pollutant: str) -> float:
    """
    Normalize pollutant concentration against WHO guidelines.
    Returns a ratio where:
    - < 1.0 = Below guideline (safe)
    - 1.0 = At guideline threshold
    - > 1.0 = Above guideline (concerning)
    
    Args:
        value: Pollutant concentration in μg/m³
        pollutant: Pollutant type key
    
    Returns:
        Normalized ratio
    """
    if value is None or value <= 0:
        return 0.0
    
    guideline = WHO_GUIDELINES.get(pollutant, 1.0)
    return value / guideline


def calculate_activity_risk(activity: str, pollutant_data: Dict[str, float]) -> Tuple[float, Dict[str, float], Dict[str, float]]:
    """
    Calculate a weighted risk score for a specific activity based on current pollutant levels.
    
    This is the core decision model that transforms raw air quality data into
    actionable risk intelligence. The model uses:
    1. Activity-specific weights (sensitivity profiles)
    2. WHO guideline normalization (health-based thresholds)
    3. Weighted sum aggregation (multi-criteria decision making)
    
    Args:
        activity: Selected activity type
        pollutant_data: Dictionary of pollutant concentrations
                       e.g., {'pm2_5': 15.2, 'o3': 70.1, 'no2': 20.5}
    
    Returns:
        Tuple of:
        - risk_score (float): Overall risk score (0-3+ range)
        - contributions (dict): Individual pollutant contributions to total risk
        - normalized_values (dict): Normalized pollutant levels vs WHO guidelines
    """
    
    # Get activity-specific weights
    if activity not in ACTIVITY_WEIGHTS:
        raise ValueError(f"Unknown activity: {activity}")
    
    weights = ACTIVITY_WEIGHTS[activity]
    
    # Extract pollutant values with safe defaults
    pm2_5 = pollutant_data.get('pm2_5', 0.0)
    pm10 = pollutant_data.get('pm10', 0.0)
    o3 = pollutant_data.get('o3', 0.0)
    no2 = pollutant_data.get('no2', 0.0)
    co = pollutant_data.get('co', 0.0)
    
    # Normalize against WHO guidelines
    normalized = {
        'pm2_5': normalize_pollutant(pm2_5, 'pm2_5'),
        'pm10': normalize_pollutant(pm10, 'pm10'),
        'o3': normalize_pollutant(o3, 'o3'),
        'no2': normalize_pollutant(no2, 'no2'),
        'co': normalize_pollutant(co, 'co')
    }
    
    # Calculate weighted risk contributions
    contributions = {
        'pm2_5': normalized['pm2_5'] * weights['pm2_5'],
        'pm10': normalized['pm10'] * weights['pm10'],
        'o3': normalized['o3'] * weights['o3'],
        'no2': normalized['no2'] * weights['no2'],
        'co': normalized['co'] * weights['co']
    }
    
    # Overall risk score (weighted sum)
    risk_score = sum(contributions.values())
    
    return risk_score, contributions, normalized


def get_decision_recommendation(risk_score: float, activity: str) -> Dict[str, str]:
    """
    Generate prescriptive recommendation based on risk score.
    
    Decision thresholds:
    - < 0.8: LOW RISK → Go ahead
    - 0.8-1.5: MODERATE RISK → Proceed with caution
    - > 1.5: HIGH RISK → Not recommended
    
    Args:
        risk_score: Calculated risk score
        activity: Activity type
    
    Returns:
        Dictionary with decision, color, icon, and detailed recommendation
    """
    
    if risk_score < 0.8:
        return {
            'decision': 'GO',
            'level': 'LOW RISK',
            'color': '#00E400',
            'icon': '🟢',
            'recommendation': (
                f"✅ **DECISION: PROCEED**\n\n"
                f"Air quality is **favorable** for {activity.lower()}. "
                f"Calculated risk score is **{risk_score:.2f}** (low threshold).\n\n"
                f"**Action:** Enjoy your outdoor activity with minimal concerns. "
                f"Air quality conditions are within safe limits for this activity type."
            ),
            'short_advice': 'Conditions are favorable - enjoy!',
            'risk_level_numeric': 1
        }
    
    elif risk_score < 1.5:
        return {
            'decision': 'CAUTION',
            'level': 'MODERATE RISK',
            'color': '#FF7E00',
            'icon': '🟡',
            'recommendation': (
                f"⚠️ **DECISION: PROCEED WITH CAUTION**\n\n"
                f"Air quality presents **moderate risk** for {activity.lower()}. "
                f"Calculated risk score is **{risk_score:.2f}** (caution threshold).\n\n"
                f"**Suggested Actions:**\n"
                f"- Consider reducing intensity or duration of outdoor activity\n"
                f"- Sensitive individuals (elderly, children, respiratory conditions) should reconsider\n"
                f"- Monitor for any discomfort (coughing, shortness of breath)\n"
                f"- Move activity indoors if symptoms develop"
            ),
            'short_advice': 'Proceed with reduced intensity',
            'risk_level_numeric': 2
        }
    
    else:
        return {
            'decision': 'STOP',
            'level': 'HIGH RISK',
            'color': '#FF0000',
            'icon': '🔴',
            'recommendation': (
                f"🚫 **DECISION: NOT RECOMMENDED**\n\n"
                f"Air quality presents **high risk** for {activity.lower()}. "
                f"Calculated risk score is **{risk_score:.2f}** (high threshold).\n\n"
                f"**Strongly Advised Actions:**\n"
                f"- **Postpone** outdoor activity to another time\n"
                f"- **Move activity indoors** if possible\n"
                f"- If outdoor exposure unavoidable, use N95/N99 mask\n"
                f"- Limit duration to absolute minimum\n"
                f"- Vulnerable populations should avoid outdoor exposure entirely"
            ),
            'short_advice': 'Postpone or move indoors',
            'risk_level_numeric': 3
        }


def create_risk_gauge(risk_score: float, activity: str) -> go.Figure:
    """
    Create an interactive gauge chart visualizing the risk score.
    
    Args:
        risk_score: Calculated risk score
        activity: Activity type
    
    Returns:
        Plotly figure object
    """
    
    decision_info = get_decision_recommendation(risk_score, activity)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Activity Risk Score<br><sub>{activity}</sub>", 'font': {'size': 16}},
        delta={'reference': 1.5, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [None, 3], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': decision_info['color'], 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 0.8], 'color': '#E8F5E9'},
                {'range': [0.8, 1.5], 'color': '#FFF3E0'},
                {'range': [1.5, 3], 'color': '#FFEBEE'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 1.5
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        font={'family': "Arial, sans-serif"}
    )
    
    return fig


def create_contribution_chart(contributions: Dict[str, float]) -> go.Figure:
    """
    Create a horizontal bar chart showing individual pollutant contributions to risk.
    
    Args:
        contributions: Dictionary of pollutant contributions
    
    Returns:
        Plotly figure object
    """
    
    # Sort by contribution (highest first)
    sorted_items = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
    pollutants = [item[0].upper().replace('_', '.') for item in sorted_items]
    values = [item[1] for item in sorted_items]
    
    # Color bars by magnitude
    colors = ['#FF4444' if v > 0.5 else '#FFA500' if v > 0.25 else '#4CAF50' for v in values]
    
    fig = go.Figure(go.Bar(
        x=values,
        y=pollutants,
        orientation='h',
        marker=dict(color=colors),
        text=[f'{v:.3f}' for v in values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Risk Contribution by Pollutant',
        xaxis_title='Weighted Risk Contribution',
        yaxis_title='Pollutant',
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )
    
    return fig


def get_pollutant_comparison_table(pollutant_data: Dict[str, float], 
                                   normalized: Dict[str, float]) -> pd.DataFrame:
    """
    Create a comparison table of actual vs. WHO guideline values.
    
    Args:
        pollutant_data: Raw pollutant concentrations
        normalized: Normalized values vs WHO guidelines
    
    Returns:
        Pandas DataFrame for display
    """
    
    data = []
    for pollutant, value in pollutant_data.items():
        if pollutant in WHO_GUIDELINES:
            guideline = WHO_GUIDELINES[pollutant]
            norm_value = normalized.get(pollutant, 0)
            
            # Status indicator
            if norm_value < 0.5:
                status = '✅ Safe'
            elif norm_value < 1.0:
                status = '⚠️ Elevated'
            else:
                status = '🚫 Exceeds'
            
            data.append({
                'Pollutant': pollutant.upper().replace('_', '.'),
                'Current (μg/m³)': f'{value:.1f}',
                'WHO Guideline': f'{guideline:.0f}',
                '% of Guideline': f'{norm_value * 100:.0f}%',
                'Status': status
            })
    
    return pd.DataFrame(data)


def get_activity_list() -> list:
    """Return list of available activities."""
    return list(ACTIVITY_WEIGHTS.keys())


def get_top_risk_drivers(contributions: Dict[str, float], top_n: int = 3) -> list:
    """
    Identify the top risk-driving pollutants.
    
    Args:
        contributions: Dictionary of pollutant contributions
        top_n: Number of top contributors to return
    
    Returns:
        List of (pollutant, contribution) tuples
    """
    sorted_items = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:top_n]


if __name__ == "__main__":
    # Test the decision engine
    print("=" * 60)
    print("DECISION ENGINE TEST")
    print("=" * 60)
    
    # Sample pollutant data
    test_data = {
        'pm2_5': 45.0,
        'pm10': 70.0,
        'o3': 85.0,
        'no2': 35.0,
        'co': 800.0
    }
    
    print(f"\nTest Pollutant Data:")
    for k, v in test_data.items():
        print(f"  {k}: {v} μg/m³")
    
    # Test all activities
    for activity in get_activity_list():
        print(f"\n{'=' * 60}")
        print(f"Activity: {activity}")
        print('=' * 60)
        
        risk_score, contributions, normalized = calculate_activity_risk(activity, test_data)
        decision = get_decision_recommendation(risk_score, activity)
        
        print(f"\nRisk Score: {risk_score:.3f}")
        print(f"Decision: {decision['decision']} ({decision['level']})")
        print(f"\nTop Risk Drivers:")
        for pollutant, contrib in get_top_risk_drivers(contributions):
            print(f"  {pollutant.upper()}: {contrib:.3f}")
