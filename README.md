# 🌬️ Air Quality Monitor Dashboard
-------------------------------------

A real-time air pollution monitoring system that tracks air quality across multiple cities worldwide using the OpenWeatherMap API.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Features

- **Real-time Data**: Live air quality data from OpenWeatherMap API
- **Multi-city Monitoring**: Track AQI across multiple cities simultaneously  
- **Interactive Visualizations**: Color-coded health status indicators and comparison charts
- **Health Recommendations**: Automated health advice based on AQI thresholds
- **Pollutant Analysis**: Detailed breakdown of PM2.5, PM10, NO2, O3, and CO levels
- **Sample Data Mode**: Try the dashboard without API key using realistic sample data

## 📊 Dashboard Preview

### Key Metrics
- Real-time AQI values with color-coded health status
- Pollutant level comparisons (PM2.5, PM10, NO2, O3, CO)
- Interactive gauge charts for visual AQI representation

### Health Categories
- 🟢 **Good (AQI 1)**: Air quality is satisfactory
- 🟡 **Fair (AQI 2)**: Acceptable for most people  
- 🟠 **Moderate (AQI 3)**: Sensitive individuals may experience symptoms
- 🔴 **Poor (AQI 4)**: Health warnings of emergency conditions
- 🟣 **Very Poor (AQI 5)**: Health alert for everyone

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Kiwi-520/air-quality-dashboard.git
cd air-quality-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Get your API key**
   - Visit [OpenWeatherMap API](https://openweathermap.org/api)
   - Sign up for a free account
   - Copy your API key

4. **Run the application**
```bash
streamlit run air_quality_app.py
```

5. **Access the dashboard**
   - Open your browser and go to `http://localhost:8501`
   - Enter your API key in the sidebar
   - Select cities to monitor

## 📋 Requirements

```txt
streamlit==1.28.0
requests==2.31.0
pandas==2.0.3
plotly==5.16.1
```

## 🎯 Usage

### Getting Started
1. **Try Sample Data**: Click "🎮 Use Sample Data" to explore features without API key
2. **Real Data**: Enter your OpenWeatherMap API key in the sidebar
3. **Select Cities**: Choose from popular cities or add custom locations
4. **Monitor**: View real-time air quality data and health recommendations

### Available Cities
- New York, London, Tokyo, Delhi, Beijing
- Los Angeles, Mumbai, São Paulo, Paris, Sydney
- Custom city input supported

### Key Functionality
- **Real-time Updates**: Fresh data every 5 minutes with caching
- **Multi-city Comparison**: Side-by-side AQI analysis
- **Health Guidance**: Automated recommendations based on pollution levels
- **Data Export**: View detailed pollutant measurements in tabular format

## 🏗️ Project Structure

```
air-quality-dashboard/
├── air_quality_app.py          # Main application file
├── requirements.txt            # Python dependencies
├── README.md                  # Project documentation
└── .gitignore                # Git ignore file
```

## 🔧 Technical Implementation

### API Integration
- **OpenWeatherMap Geocoding API**: Convert city names to coordinates
- **Air Pollution API**: Fetch real-time AQI and pollutant data
- **Error Handling**: Robust error management for API failures
- **Caching**: 5-minute cache to optimize API usage

### Data Processing
- AQI classification and health category mapping
- Pollutant level analysis (PM2.5, PM10, NO2, O3, CO)
- Real-time data validation and cleaning

### Visualization
- **Plotly Charts**: Interactive bar charts for pollutant comparison
- **Color Coding**: Health status visualization with standard AQI colors
- **Responsive Design**: Adaptive layout for different screen sizes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Kiwi-520**
- GitHub: [@Kiwi-520](https://github.com/Kiwi-520)
- Project Link: [https://github.com/Kiwi-520/air-quality-dashboard](https://github.com/Kiwi-520/air-quality-dashboard)

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing free air quality API
- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [Plotly](https://plotly.com/) for interactive visualizations

---

⭐ **Star this repository if you found it helpful!**
