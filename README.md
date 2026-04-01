<div align="center">

<!-- Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a472a,50:2d6a4f,100:52b788&height=200&section=header&text=Sehore%20EcoRisk%20Intelligence&fontSize=38&fontColor=d8f3dc&fontAlignY=38&desc=AI-Powered%20Environmental%20Risk%20Assessment%20Platform&descAlignY=58&descColor=b7e4c7&animation=fadeIn" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-f7931e?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM-ff6f00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-52b788?style=for-the-badge)](LICENSE)

<br/>

> *Combining geospatial intelligence, machine learning, and environmental science to quantify contamination risk across Sehore and surrounding regions.*

</div>

---

## 🌿 What Is This?

**Sehore EcoRisk Intelligence** is an interactive, AI-driven platform that evaluates environmental contamination risk by fusing air quality data, soil sensitivity profiles, and proximity to water bodies — delivering actionable, explainable risk intelligence in real time.

Whether you're a researcher, urban planner, or environmental policymaker, this tool gives you a decision-support layer grounded in spatial analytics and interpretable ML.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎛️ **Pollutant Simulation** | Real-time sliders for PM2.5, PM10, NO₂, SO₂, CO inputs |
| 🗺️ **Map-Click Location** | Click any point on the map to simulate site-specific risk |
| 🌲 **Random Forest Classifier** | Trained model classifies risk as `Low`, `Medium`, or `High` |
| 🪨 **Soil-Aware Leaching** | Estimates groundwater contamination timelines per soil type |
| 💡 **Mitigation Engine** | Rule-based recommendations tailored to detected risk profile |
| 📊 **Plotly Visualizations** | Risk gauge + density heatmap overlays |
| 📈 **LSTM AQI Forecasting** | Lightweight neural network for short-term air quality trends |
| 🔍 **SHAP Explainability** | Feature importance with graceful fallback mode |

---

## 🧠 How It Works

```
User Input (pollutants + location)
         │
         ▼
  Feature Engineering
  ┌─────────────────────────────┐
  │  Air Quality Index (AQI)    │
  │  Soil Sensitivity Score     │
  │  Distance to River (km)     │
  └─────────────────────────────┘
         │
         ▼
  Random Forest Classifier
         │
         ▼
  Risk Output: Low / Medium / High
         │
    ┌────┴────┐
    ▼         ▼
  SHAP      Mitigation
  Report    Recommendations
```

---

## 📁 Repository Structure

```
sehore-risk-ai/
│
├── 📄 app.py                  # Streamlit app — inference & UI workflow
├── 🧪 train_model.py          # Synthetic data training + artifact export
├── 🔌 data_pipeline.py        # CPCB / local data pipeline (optional)
├── 📊 aqi_data.csv            # Sample local air-quality dataset
├── 🤖 sehore_risk_model.pkl   # Trained Random Forest model
├── ⚖️  scaler.pkl              # Fitted feature scaler
└── 🧩 test.py                 # Lightweight testing placeholder
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **ML / Classification** | Scikit-learn (Random Forest) |
| **Deep Learning** | TensorFlow / Keras (LSTM) |
| **Visualization** | Plotly, Folium, streamlit-folium |
| **Explainability** | SHAP |
| **Geospatial** | Geopy |
| **Data** | Pandas, NumPy |
| **Serialization** | Joblib |

</div>

---

## 🚀 Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd sehore-risk-ai
```

### 2. Create & activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

**From requirements file (recommended):**
```bash
pip install -r requirements.txt
```

**Or manually:**
```bash
pip install streamlit scikit-learn pandas numpy plotly \
            folium streamlit-folium geopy tensorflow joblib requests shap
```

### 4. (Optional) Retrain the model

```bash
python train_model.py
# or
python data_pipeline.py
```

### 5. Launch the app

```bash
streamlit run app.py
```

Open your browser at → **[http://localhost:8501](http://localhost:8501)**

---

## ☁️ Deployment

### GitHub

```bash
git init
git add .
git commit -m "feat: initial commit — Sehore EcoRisk Intelligence"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Streamlit Community Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Click **New app**
4. Select your repository and branch (`main`)
5. Set the main file path to `app.py`
6. Click **Deploy** 🚀

#### Recommended Streamlit config

Create `.streamlit/config.toml`:

```toml
[server]
headless = true
enableCORS = false
port = 8501
```

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATA_GOV_IN_API_KEY` | Optional | API key for `data_pipeline.py` live data fetch |

---

## 🗺️ Roadmap

- [ ] 🌐 Real-time IoT sensor integration
- [ ] 🏙️ Multi-city risk mapping dashboard
- [ ] 🔄 Automated model retraining pipeline
- [ ] 📅 Historical trend dashboard & model monitoring
- [ ] 🗂️ Export reports as PDF / CSV

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with 💚 for environmental awareness in Sehore, Madhya Pradesh**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a472a,50:2d6a4f,100:52b788&height=100&section=footer" width="100%"/>

</div>