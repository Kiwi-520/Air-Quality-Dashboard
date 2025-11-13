# 🌬️ Air Quality Decision Engine

**Transform Air Quality Monitoring into Actionable Intelligence**

![Python](https://img.shields.io/badge/python-v3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.51+-red.svg)
![Decision Science](https://img.shields.io/badge/Decision_Science-MCDA-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An **intelligent decision system** that transforms real-time air quality data into **prescriptive, context-aware recommendations** using Multi-Criteria Decision Analysis (MCDA) and WHO health guidelines.

---

## 🎬 Demo Video

https://github.com/user-attachments/assets/331402b1-9da1-445d-8622-6702aa481f66

*See the Decision Engine in action: from activity selection to risk assessment and prescriptive recommendations.*

---

## 🚀 Quick Start

### Live Demo
🌐 **[Try it Live](https://air-quality-dashboard-kiwi-520.streamlit.app/)**

### Local Setup
```bash
git clone https://github.com/Kiwi-520/Air-Quality-Dashboard.git
cd Air-Quality-Dashboard
pip install -r requirements.txt
streamlit run main_dashbaord.py
```

Open `http://localhost:8501` in your browser.

---

## ✨ Key Features

### 🎯 Decision Engine (Core Innovation)
**Transform "What's the AQI?" into "What should I do?"**

- **🏃‍♂️ Activity-Specific Risk Assessment:** 6 activity types with unique sensitivity profiles
- **🎯 Prescriptive Recommendations:** Clear GO/CAUTION/STOP decisions with detailed rationale
- **📊 Multi-Criteria Decision Analysis:** Weighted risk scoring using WHO guidelines
- **📈 Visual Risk Analytics:** Interactive gauges, contribution charts, and transparency reports

### 📡 Real-Time Air Quality Monitoring
- **🌍 Multi-City Tracking:** Monitor multiple global locations simultaneously
- **⚡ Live API Integration:** OpenWeatherMap with intelligent 5-minute caching
- **🧪 Comprehensive Pollutants:** PM2.5, PM10, O3, NO2, CO, SO2
- **🚨 Health Status Indicators:** Color-coded alerts and recommendations

### 📊 Interactive Visualizations
- **🎛️ Risk Gauges:** Real-time risk scoring with threshold indicators
- **🔍 Contribution Analysis:** See which pollutants drive each decision
- **📈 Comparison Charts:** Side-by-side multi-city analysis
- **📋 Data Tables:** Exportable decision reports (CSV)

---

## 🧠 How the Decision Engine Works

### The Problem
Traditional air quality dashboards show **what is** (AQI = 3) but not **what to do**.

### Our Solution
**Multi-Criteria Decision Analysis (MCDA)** that provides prescriptive recommendations.

### The Algorithm
```
1. 📊 DATA COLLECTION
   ↓ Real-time pollutant concentrations (μg/m³)
   
2. 📏 NORMALIZATION  
   ↓ Compare against WHO Air Quality Guidelines
   
3. ⚖️ ACTIVITY WEIGHTING
   ↓ Apply sensitivity profiles (exercise vs. relaxing)
   
4. 🔢 RISK AGGREGATION
   ↓ Weighted sum = Overall Risk Score
   
5. 🎯 DECISION MAPPING
   ↓ Risk Score → GO/CAUTION/STOP + Rationale
```

### Example: Why "Strenuous Exercise" Gets Different Advice

| Pollutant | Weight | Reasoning |
|-----------|--------|-----------|
| **PM2.5** | 50% | High breathing rate increases particle intake |
| **O3** | 20% | Ozone damages lung tissue during exertion |
| **PM10** | 20% | Moderate concern for larger particles |
| **NO2** | 5% | Lower relative impact during exercise |
| **CO** | 5% | Lower relative impact during exercise |

**Result:** Same city, different activities → different recommendations

---

## 🎨 User Experience & Design

### Dashboard Interface
- **🎯 Clean Design:** Intuitive sidebar controls with clear visual hierarchy
- **📱 Progressive Disclosure:** Basic view → Advanced analytics → Full methodology
- **🖥️ Responsive Layout:** Optimized for desktop and tablet devices

### Color Psychology
- **🟢 Green (Safe):** Proceed with confidence
- **🟡 Yellow (Caution):** Proceed with awareness  
- **🔴 Red (Stop):** Take protective action

### User Journey
1. **Select Activity** → Choose your planned outdoor activity
2. **Pick City** → Select location from global database
3. **Get Decision** → Receive instant GO/CAUTION/STOP recommendation
4. **Explore Analysis** → Dive into risk drivers and methodology
5. **Export Report** → Download decision documentation (CSV)

---

## 🛠️ Technical Architecture

### Core Components

**🧠 `decision_engine.py` - The Brain**
- `calculate_activity_risk()` - Core MCDA algorithm
- `get_decision_recommendation()` - Maps scores to actions
- Risk visualization functions
- Activity weights & WHO guideline definitions

**🖥️ `main_dashbaord.py` - The Interface**
- Streamlit application orchestration
- Decision engine integration
- Interactive visualization management
- User interaction handling

**🔌 `api_functions.py` - The Data Pipeline**
- OpenWeatherMap API integration (Geocoding + Air Pollution)
- Clean data formatting for decision engine
- 5-minute intelligent caching strategy
- Robust error handling & user feedback

**📊 `aqi_utils.py` - Supporting Visuals**
- Traditional AQI gauge charts (1-5 scale)
- Health category color mapping
- Interactive pollution level displays

---

## 📋 Installation & Configuration

### Prerequisites
- **Python 3.12+** 
- **OpenWeatherMap API Key** ([Get Free Key](https://openweathermap.org/api))

### Step-by-Step Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/Kiwi-520/Air-Quality-Dashboard.git
   cd Air-Quality-Dashboard
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   ```python
   # Edit api_functions.py, line 7:
   API_KEY = 'your_openweathermap_api_key_here'
   ```

4. **Launch Application**
   ```bash
   streamlit run main_dashbaord.py
   ```

5. **Access Dashboard**
   - Open browser: `http://localhost:8501`
   - Use Decision Engine in sidebar
   - Select cities to monitor

### Dependencies
```
streamlit>=1.51.0
requests>=2.31.0
pandas>=2.0.3
plotly>=5.16.1
numpy>=1.24.0
```

---

## 🎯 Usage Examples

### Scenario 1: Morning Jog Planning
**Input:** "Strenuous Exercise" in "New York"  
**Output:** Risk Score 1.2 → **🟡 CAUTION**  
*"Air quality presents moderate risk. Consider reducing intensity or duration."*

### Scenario 2: Family Picnic Planning
**Input:** "Outdoor Event" in "London"  
**Output:** Risk Score 0.6 → **🟢 GO**  
*"Conditions are favorable, enjoy your outdoor activity!"*

### Scenario 3: Daily Commute Assessment
**Input:** "Commuting (walking/biking)" in "Delhi"  
**Output:** Risk Score 2.1 → **🔴 STOP**  
*"High risk detected. Consider indoor alternatives or protective equipment."*

---

## 📊 Project Structure

```
Air-Quality-Dashboard/
├── 📄 main_dashbaord.py       # Streamlit application entry point
├── 🧠 decision_engine.py      # Core decision science algorithms  
├── 🔌 api_functions.py        # OpenWeatherMap API integration
├── 📈 aqi_utils.py           # Traditional AQI visualizations
├── 📋 requirements.txt       # Python dependencies
├── 📚 DOCUMENTATION.md       # Technical implementation guide
├── 📖 README.md             # This file
└── 🗂️ __pycache__/          # Python bytecode cache
```

---

## 🔬 Scientific Foundation

### WHO Air Quality Guidelines (2021)
| Pollutant | Guideline Value | Primary Health Impact |
|-----------|-----------------|---------------------|
| **PM2.5** | 25 μg/m³ | Cardiovascular & respiratory disease |
| **PM10** | 50 μg/m³ | Respiratory irritation, reduced lung function |
| **O3** | 100 μg/m³ | Respiratory damage, especially during exercise |
| **NO2** | 40 μg/m³ | Airway inflammation, reduced immunity |
| **CO** | 10,000 μg/m³ | Reduced oxygen delivery to organs |

### Evidence-Based Risk Assessment
- **🔬 Activity Profiles:** Based on respiratory physiology research
- **📊 Validated Thresholds:** Decision boundaries from health impact studies  
- **🔍 Transparent Methodology:** Full mathematical model available for review

---

## 🤝 Contributing

We welcome contributions to improve the decision engine and expand its capabilities!

### How to Contribute
1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes (focus on decision engine improvements)
4. **Add** tests for new functionality
5. **Submit** pull request with detailed description

### Priority Areas
- **🎯 New Activity Types:** Add specialized outdoor activities
- **🌍 Localization:** Multi-language support and regional guidelines
- **📊 Enhanced Visualizations:** Advanced charts and interactive elements
- **🔬 Algorithm Improvements:** Refined risk models and validation studies
- **📱 Mobile Optimization:** Responsive design improvements

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Kiwi-520**
- GitHub: [@Kiwi-520](https://github.com/Kiwi-520)
- Project: [Air-Quality-Dashboard](https://github.com/Kiwi-520/Air-Quality-Dashboard)

---

## 🙏 Acknowledgments

- **[OpenWeatherMap](https://openweathermap.org/)** - Reliable real-time air quality data
- **[World Health Organization](https://www.who.int/)** - Air quality guidelines and research
- **[Streamlit Team](https://streamlit.io/)** - Excellent web application framework
- **[Plotly](https://plotly.com/)** - Interactive visualization capabilities
- **Environmental Health Research Community** - Scientific foundation for risk assessment

---

## 📚 References & Further Reading

1. **WHO Air Quality Guidelines (2021)** - Global health standards and recommendations
2. **Multi-Criteria Decision Analysis in Environmental Health** - MCDA methodology
3. **Exercise Physiology & Air Pollution Research** - Activity-specific risk factors
4. **OpenWeatherMap API Documentation** - Technical integration specifications

---

## 🔄 Version History

### v1.0.0 - Current Release
- ✅ **Core Decision Engine** with 6 activity-specific profiles
- ✅ **Real-Time Multi-City Monitoring** with live API integration
- ✅ **Interactive Risk Visualizations** and analytics dashboard
- ✅ **WHO Guideline Integration** for scientific accuracy
- ✅ **Exportable Decision Reports** for documentation

### 🚀 Future Roadmap
- 🔜 **Mobile-Responsive Design** for smartphone access
- 🔜 **Historical Data Analysis** and trend visualization
- 🔜 **Personalized Risk Profiles** based on user health conditions
- �� **RESTful API Endpoints** for developer integration
- 🔜 **Machine Learning Enhancement** for improved predictions

---

## 📞 Support & Feedback

Found a bug? Have a feature request? We'd love to hear from you!

- **🐛 Issues:** [GitHub Issues](https://github.com/Kiwi-520/Air-Quality-Dashboard/issues)
- **💡 Feature Requests:** [GitHub Discussions](https://github.com/Kiwi-520/Air-Quality-Dashboard/discussions)
- **📧 Contact:** Create an issue for direct communication

---

⭐ **If you find this project helpful, please star the repository!**

🌱 **Built with passion for public health and environmental awareness**
