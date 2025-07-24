import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="Air Quality Monitor",
    page_icon="🌬️",
    layout="wide"
)

st.title("🌬️ Real-Time Air Quality Monitor")
st.markdown("Track air pollution levels across different cities worldwide")
