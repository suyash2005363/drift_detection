from dotenv import load_dotenv
load_dotenv()
from src.ingestion.data_ingestion import DataIngestion
from src.validation.data_validation import DataValidation
from src.drift.drift_detector import DriftDetector
from src.monitoring.prediction_monitor import PredictionMonitor
from src.monitoring.confidence_monitor import ConfidenceMonitor
from src.alert.alert_system import AlertSystem

# ✅ NEW: GenAI import
from src.genai.explanation import generate_explanation

import yaml
import time


CONFIG_PATH = "config/config.yaml"

def log_stage(stage_name):
    print("\n----------------------------------")
    print(f"PIPELINE STAGE: {stage_name}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("----------------------------------")

def main():

    print("\nStarting Drift Detection Pipeline\n")

    ingestion = DataIngestion(CONFIG_PATH)

    reference_data = ingestion.load_reference_data()
    batches = ingestion.load_batches()

    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)

    model_path = config["model_path"]

    for batch_name, incoming_data in batches:

        print("\n==============================")
        print(f"Processing {batch_name}")
        print("==============================")

        # -------------------------------
        # VALIDATION
        # -------------------------------
        validation = DataValidation(reference_data, incoming_data)
        validation.run()

        # -------------------------------
        # DRIFT DETECTION
        # -------------------------------
        drift = DriftDetector(reference_data, incoming_data)
        drift_results = drift.detect_drift()

        drift_count = sum(
            1 for result in drift_results.values()
            if result["drift_detected"]
        )

        total_features = len(drift_results)
        drift_percentage = (drift_count / total_features) * 100

        drift.run()

        # -------------------------------
        # MONITORING
        # -------------------------------
        prediction_monitor = PredictionMonitor(
            model_path,
            reference_data,
            incoming_data
        )
        prediction_monitor.run()

        confidence_monitor = ConfidenceMonitor(
            model_path,
            incoming_data
        )
        confidence = confidence_monitor.run()

        # -------------------------------
        # ALERT SYSTEM
        # -------------------------------
        alert = AlertSystem(
            drift_count,
            total_features,
            confidence
        )
        alert.run()

        # -------------------------------
        # 🤖 GENAI EXPLANATION (NEW)
        # -------------------------------
        try:
            ai_explanation = generate_explanation(
                drift_results,
                drift_percentage,
                confidence
            )

            print("\n🤖 AI Explanation:\n")
            print(ai_explanation)

        except Exception as e:
            print("\n⚠️ GenAI failed:", e)


if __name__ == "__main__":
    main()