import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geopy.distance import geodesic
from streamlit_folium import st_folium
import folium

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Sehore Risk AI", layout="wide")

# -----------------------------
# 🎯 GLOBAL FONT SIZE (16px)
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 16px !important;
}
h1 { font-size: 36px !important; }
h2 { font-size: 28px !important; }
h3 { font-size: 22px !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model():
    model = joblib.load("sehore_risk_model.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, scaler

model, scaler = load_model()

# -----------------------------
# RIVER COORDINATES
# -----------------------------
SIVAN_RIVER = [(23.20,77.08),(23.18,77.05),(23.22,77.12)]

def distance_to_river(lat, lon):
    return min([geodesic((lat, lon), r).km for r in SIVAN_RIVER])

# -----------------------------
# LEACHING MODEL
# -----------------------------
def leaching_time(risk, soil):
    perm = {"Black Cotton Soil":1e-9,"Loamy Soil":1e-7,"Sandy Soil":1e-5}
    velocity = (perm[soil]*0.01)/0.35
    years = (10 / max(velocity,1e-10)) / (60*60*24*365)

    if risk == "High": years *= 0.5
    elif risk == "Medium": years *= 0.8

    return round(years, 2)

# -----------------------------
# MITIGATION ENGINE
# -----------------------------
def mitigation(risk, soil):
    if risk == "High":
        if soil == "Black Cotton Soil":
            return ["🧪 Gypsum Treatment", "🌻 Sunflower Phyto-remediation"]
        return ["🚫 Stop dumping", "🧼 Soil washing"]
    elif risk == "Medium":
        return ["⚠️ Monitor AQI", "🌿 Vegetation cover"]
    return ["✅ Safe Zone"]

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("⚙️ Input Parameters")
st.sidebar.info("Adjust pollutant levels and soil type to simulate environmental conditions and observe how risk changes dynamically.")

u_pm25 = st.sidebar.slider("PM2.5", 0, 300, 80)
u_pm10 = st.sidebar.slider("PM10", 0, 500, 120)
u_no2  = st.sidebar.slider("NO2", 0, 200, 40)
u_so2  = st.sidebar.slider("SO2", 0, 100, 10)
u_co   = st.sidebar.slider("CO", 0.0, 5.0, 1.0)

soil = st.sidebar.selectbox("Soil Type",
    ["Black Cotton Soil","Loamy Soil","Sandy Soil"])

# -----------------------------
# HEADER
# -----------------------------
st.title("🌍 Sehore Eco-Risk Intelligence Platform")
st.caption("This AI-powered system analyzes environmental pollutants, soil conditions, and spatial proximity to predict land contamination risk and its future impact.")

# -----------------------------
# MAP UI
# -----------------------------
default_loc = [23.2032, 77.0844]
m = folium.Map(location=default_loc, zoom_start=10)

for r in SIVAN_RIVER:
    folium.CircleMarker(location=r, radius=5, color='blue').add_to(m)

map_data = st_folium(m, height=400)

st.info("📍 Click anywhere on the map to simulate risk at that location. The system dynamically calculates environmental risk based on proximity to the river.")

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
else:
    lat, lon = default_loc

st.success(f"📍 Selected Location: {lat:.4f}, {lon:.4f}")

# -----------------------------
# ANALYZE BUTTON
# -----------------------------
if st.button("🚀 Analyze Risk"):

    inp = np.array([[u_pm25, u_pm10, u_no2, u_so2, u_co]])
    inp_scaled = scaler.transform(inp)

    probs = model.predict_proba(inp_scaled)[0]
    classes = model.classes_

    risk_value = int(
        probs[classes.tolist().index("Low")] * 30 +
        probs[classes.tolist().index("Medium")] * 60 +
        probs[classes.tolist().index("High")] * 90
    )

    if risk_value < 40:
        pred = "Low"
    elif risk_value < 70:
        pred = "Medium"
    else:
        pred = "High"

    dist = distance_to_river(lat, lon)
    leach = leaching_time(pred, soil)

    # -----------------------------
    # GAUGE
    # -----------------------------
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_value,
        title={'text': f"Risk Level: {pred}"},
        gauge={
            'axis': {'range':[0,100]},
            'steps':[
                {'range':[0,40],'color':'green'},
                {'range':[40,70],'color':'yellow'},
                {'range':[70,100],'color':'red'}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("The gauge shows overall environmental risk (0–100).")

    # -----------------------------
    # DISTANCE + LEACHING
    # -----------------------------
    st.info(f"🌊 Distance to River: {round(dist,2)} km")
    st.warning(f"⏳ Groundwater contamination expected in: {leach} years")

    # -----------------------------
    # MITIGATION
    # -----------------------------
    st.subheader("🛠️ Recommendations")
    st.caption("AI-driven remediation suggestions based on predicted risk and soil.")

    for m in mitigation(pred, soil):
        st.success(m)

    # -----------------------------
    # HEATMAP
    # -----------------------------
    st.subheader("🔥 Risk Heatmap")
    st.caption("Shows spatial spread of environmental risk.")

    lat_range = np.linspace(lat-0.1, lat+0.1, 30)
    lon_range = np.linspace(lon-0.1, lon+0.1, 30)

    grid = []
    for la in lat_range:
        for lo in lon_range:
            d = distance_to_river(la, lo)
            score = (u_pm25/300 + u_pm10/500)/2 + (1/(d+0.5))

            if score < 0.8:
                risk_val = 25
            elif score < 1.5:
                risk_val = 60
            else:
                risk_val = 90

            grid.append({"lat": la, "lon": lo, "risk": risk_val})

    grid_df = pd.DataFrame(grid)

    fig_map = px.density_mapbox(
        grid_df,
        lat='lat',
        lon='lon',
        z='risk',
        radius=10,
        center=dict(lat=lat, lon=lon),
        zoom=10,
        mapbox_style="carto-positron",
        color_continuous_scale="RdYlGn_r"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # -----------------------------
    # -----------------------------
    # FORECAST (TensorFlow optional)
    # -----------------------------
    st.subheader("AQI Forecast")
    st.caption("Forecasts near-term pollution trend.")

    data = np.array([u_pm25 + np.random.randint(-10, 10) for _ in range(20)])
    future = []

    try:
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense

        X = data[:-1].reshape(-1, 1, 1)
        y = data[1:]

        lstm = Sequential([LSTM(10, input_shape=(1, 1)), Dense(1)])
        lstm.compile("adam", "mse")
        lstm.fit(X, y, epochs=5, verbose=0)

        curr = data[-1]
        for _ in range(7):
            p = lstm.predict(np.array([[[curr]]]), verbose=0)[0][0]
            future.append(p)
            curr = p
    except Exception:
        # Keep deployment lightweight when TensorFlow is unavailable.
        st.info("TensorFlow not installed; using lightweight forecast fallback.")
        trend = np.mean(np.diff(data[-6:])) if len(data) > 6 else 0
        curr = float(data[-1])
        for _ in range(7):
            curr = max(0.0, curr + trend)
            future.append(curr)

    st.line_chart(future)

    # -----------------------------
    # SHAP / FALLBACK
    # -----------------------------
    st.subheader("🧠 AI Explanation")
    st.caption("Shows contribution of each pollutant to risk.")

    features = ['PM2.5','PM10','NO2','SO2','CO']

    try:
        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(pd.DataFrame(inp, columns=features))

        vals = shap_values[0][0] if isinstance(shap_values, list) else shap_values[0]
        colors = ["green" if v > 0 else "red" for v in vals]

        fig = go.Figure(go.Bar(
            x=vals,
            y=features,
            orientation='h',
            marker=dict(color=colors)
        ))
        st.plotly_chart(fig, use_container_width=True)

    except:
        st.warning("⚠️ SHAP fallback used")
        fallback = np.array([u_pm25/300, u_pm10/500, u_no2/200, u_so2/100, u_co/5])
        st.bar_chart(pd.DataFrame({"Feature":features,"Impact":fallback}).set_index("Feature"))

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.info("AI + GIS powered environmental risk monitoring system.")
