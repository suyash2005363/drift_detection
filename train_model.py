import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier


print("🚀 Starting training pipeline...")

# -------------------------------
# LOAD DATA
# -------------------------------

data_path = os.path.join("data", "adult.csv")

df = pd.read_csv(data_path)

# Clean column names
df.columns = df.columns.str.strip()

# Replace '?' with NaN
df.replace("?", np.nan, inplace=True)

# Drop missing values
df.dropna(inplace=True)

print(f"✅ Data loaded: {df.shape}")

# -------------------------------
# ENCODING
# -------------------------------

label_encoders = {}

for col in df.select_dtypes(include="object").columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

print("✅ Encoding completed")

# -------------------------------
# SPLIT FEATURES & TARGET
# -------------------------------

X = df.drop("income", axis=1)
y = df["income"]

# Save feature names (important for UI)
joblib.dump(X.columns.tolist(), "Models/features.pkl")

# -------------------------------
# SCALING
# -------------------------------

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------------
# LDA
# -------------------------------

lda = LinearDiscriminantAnalysis(n_components=1)
X_lda = lda.fit_transform(X_scaled, y)

print("✅ LDA applied")

# -------------------------------
# TRAIN MODEL
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_lda, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

print("✅ Model trained")

# -------------------------------
# SAVE EVERYTHING
# -------------------------------

os.makedirs("Models", exist_ok=True)

joblib.dump(model, "Models/model.pkl")
joblib.dump(scaler, "Models/scaler.pkl")
joblib.dump(lda, "Models/lda.pkl")

print("💾 Model, scaler, LDA saved successfully!")

# -------------------------------
# OPTIONAL: MODEL ACCURACY
# -------------------------------

accuracy = model.score(X_test, y_test)
print(f"🎯 Model Accuracy: {accuracy:.4f}")

print("🎉 Training pipeline completed successfully!")