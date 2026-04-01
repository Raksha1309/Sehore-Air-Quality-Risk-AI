import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

np.random.seed(42)

# Generate STRONGER dataset
n = 5000

df = pd.DataFrame({
    'pm25': np.random.uniform(10, 300, n),
    'pm10': np.random.uniform(20, 500, n),
    'no2': np.random.uniform(5, 200, n),
    'so2': np.random.uniform(2, 100, n),
    'co': np.random.uniform(0.1, 5, n),
})

# 🔥 STRONG NON-LINEAR RISK FUNCTION
df['risk_score'] = (
    0.4 * (df['pm25']/300)**2 +   # squared → more sensitivity
    0.3 * (df['pm10']/500) +
    0.1 * (df['no2']/200) +
    0.1 * (df['so2']/100) +
    0.1 * (df['co']/5)
)

# ADD RANDOM NOISE (important!)
df['risk_score'] += np.random.normal(0, 0.05, n)

# CLEAR CLASS SEPARATION
conditions = [
    df['risk_score'] < 0.3,
    (df['risk_score'] >= 0.3) & (df['risk_score'] < 0.6),
    df['risk_score'] >= 0.6
]

choices = ['Low', 'Medium', 'High']
df['risk'] = np.select(conditions, choices)

# FEATURES
X = df[['pm25','pm10','no2','so2','co']]
y = df['risk']

# SCALE
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# TRAIN MODEL
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_scaled, y)

# SAVE
joblib.dump(model, "sehore_risk_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model retrained successfully")