import pandas as pd
import requests
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# =========================
# CONFIG
# =========================
API_KEY = os.getenv("DATA_GOV_IN_API_KEY")  # optional
USE_API = True   # 🔴 set False if no API key


# =========================
# 1. FETCH DATA
# =========================
def fetch_cpcb_data():
    if USE_API and API_KEY:
        print("🌐 Fetching from API...")
        url = f"https://api.data.gov.in/resource/air-quality?api-key={API_KEY}&format=json&limit=1000"
        
        response = requests.get(url)
        data = response.json()
        
        df = pd.DataFrame(data['records'])
    
    else:
        print("📂 Using local CSV data...")
        
        # 🔴 MAKE SURE THIS FILE EXISTS
        df = pd.read_csv("aqi_data.csv")

    return df


# =========================
# 2. CLEAN DATA
# =========================
def clean_data(df):
    cols = ['city', 'pm25', 'pm10', 'no2', 'so2', 'co']
    df = df[cols]

    df.columns = ['city', 'PM2.5', 'PM10', 'NO2', 'SO2', 'CO']

    for col in ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna()

    # Focus on MP region
    df = df[df['city'].str.contains("Bhopal|Sehore", case=False)]

    return df


# =========================
# 3. FEATURE ENGINEERING
# =========================
def compute_aqi(row):
    return (
        0.4 * row['PM2.5'] +
        0.3 * row['PM10'] +
        0.1 * row['NO2'] +
        0.1 * row['SO2'] +
        0.1 * row['CO'] * 100
    )


def add_features(df):
    df['AQI'] = df.apply(compute_aqi, axis=1)

    def classify(aqi):
        if aqi <= 50:
            return "Low"
        elif aqi <= 100:
            return "Medium"
        else:
            return "High"

    df['risk'] = df['AQI'].apply(classify)
    return df


# =========================
# 4. TRAIN MODEL
# =========================
def train_model(df):
    X = df[['PM2.5', 'PM10', 'NO2', 'SO2', 'CO']]
    y = df['risk']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=200)
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    print(f"✅ Model Accuracy: {acc*100:.2f}%")

    return model


# =========================
# 5. SAVE MODEL
# =========================
def save_model(model):
    joblib.dump(model, "sehore_risk_model.pkl")


# =========================
# 6. RUN PIPELINE
# =========================
def run_pipeline():
    print("📥 Fetching data...")
    df = fetch_cpcb_data()

    print("🧹 Cleaning data...")
    df = clean_data(df)

    print("🧠 Feature engineering...")
    df = add_features(df)

    print("🤖 Training model...")
    model = train_model(df)

    print("💾 Saving model...")
    save_model(model)

    print("🚀 DONE! Model saved as sehore_risk_model.pkl")


if __name__ == "__main__":
    run_pipeline()