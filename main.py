from dotenv import load_dotenv
load_dotenv()

from src.ingestion.data_ingestion import DataIngestion
from src.validation.data_validation import DataValidation
from src.drift.drift_detector import DriftDetector
from src.monitoring.confidence_monitor import ConfidenceMonitor
from src.alert.alert_system import AlertSystem

# GenAI
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

    # -------------------------------
    # INGESTION
    # -------------------------------
    ingestion = DataIngestion()

    reference_data = ingestion.load_reference_data()
    batches = ingestion.load_batch_data()

    # -------------------------------
    # CONFIG
    # -------------------------------
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)

    model_path = config["model_path"]

    # -------------------------------
    # LOOP THROUGH BATCHES
    # -------------------------------
    for i, batch in enumerate(batches):

        if isinstance(batch, tuple):
            batch_name, incoming_data = batch
        else:
            batch_name = f"batch_{i+1}"
            incoming_data = batch

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
        drift = DriftDetector()
        drift_results = drift.detect_drift(reference_data, incoming_data)

        drift_count = sum(
            1 for result in drift_results.values()
            if result["drift_detected"]
        )

        total_features = len(drift_results)
        drift_percentage = (drift_count / total_features) * 100

        # -------------------------------
        # CONFIDENCE MONITORING (SAFE)
        # -------------------------------
        try:
            confidence_monitor = ConfidenceMonitor(
                model_path,
                incoming_data
            )
            confidence = confidence_monitor.run()

        except Exception as e:
            print("\n⚠️ Confidence monitoring failed:", e)
            confidence = 0.7  # fallback

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
        # 🤖 GENAI EXPLANATION
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