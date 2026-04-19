import pandas as pd
from src.drift.drift_detector import DriftDetector

print("🔍 Running drift test...")

ref = pd.read_csv("data/reference/reference_dataset.csv")
curr = pd.read_csv("data/income/batch_1.csv")

detector = DriftDetector()
result = detector.detect_drift(ref, curr)

drift_count = sum(
    1 for v in result.values()
    if "drift_detected" in v and v["drift_detected"]
)

print(f"⚠️ Drifted features: {drift_count}")

# Fail CI if too much drift
if drift_count > 5:
    raise Exception("🚨 Too much drift detected!")

print("✅ Drift test passed")