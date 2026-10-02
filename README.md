# SurakshaTaap Pune - PMC Heatwave & Thermal Stress Platform

**Ministry of Earth Sciences (MoES) / NCMRWF - Problem Statement 26083**
**Hyper-Local Human Thermal Stress & Mortality Risk Platform for Pune Municipal Corporation (PMC)**

---

## 🌟 Overview
SurakshaTaap Pune is an advanced decision-support system designed to safeguard citizens and municipal workers against extreme heatwaves. By modeling thermal stress, WBGT, UTCI, and mortality risk at hyper-local PMC ward resolution, it equips city administrators with real-time analytics, automated alerts, and Heat Action Plan (HAP) protocols.

## 🚀 Key Features
- **Comprehensive Heat Stress Engine**: Calculates Wet Bulb Globe Temperature (WBGT), Universal Thermal Climate Index (UTCI), Heat Index, and physiological strain.
- **Ward-Level GIS Mapping**: Interactive GeoJSON mapping across Pune Municipal Corporation administrative wards with vulnerability indices.
- **Mortality & Morbidity Risk Forecasting**: Predictive epidemiological risk modeling based on temperature exposure thresholds.
- **Automated Heat Action Plan (HAP)**: Real-time trigger systems with multi-lingual alerts (English & Marathi).
- **FastAPI Backend & Interactive Web UI**: High-performance asynchronous API paired with dynamic responsive dashboards.

## 🛠️ Tech Stack
- **Backend**: Python 3, FastAPI, Pydantic, Uvicorn
- **Modeling**: NumPy, SciPy, Mathematical epidemiological risk models
- **Frontend**: Responsive HTML5, Modern CSS3, JavaScript, Leaflet.js / Charts.js

## 🏁 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/sohamd530-eng/thisisforvideo.git
cd thisisforvideo
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
Then open `http://localhost:8000` in your web browser.
