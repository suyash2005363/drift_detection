import os
import pickle
import numpy as np

# Correct absolute path to model
model_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../Models/model.pkl")
)

# Load model
model = pickle.load(open(model_path, "rb"))

def predict_output(data: dict):
    features = np.array(list(data.values())).reshape(1, -1)

    prediction = model.predict(features)[0]

    if hasattr(model, "predict_proba"):
        confidence = max(model.predict_proba(features)[0])
    else:
        confidence = None

    return {
        "prediction": int(prediction),
        "confidence": float(confidence) if confidence else None
    }