import numpy as np
import joblib


class ConfidenceMonitor:

    def __init__(self, model_path, incoming_data):

        self.model = joblib.load(model_path)
        self.incoming_data = incoming_data

    def run(self):

        print("\nRunning Confidence Monitoring...\n")

        if not hasattr(self.model, "predict_proba"):

            print("Model does not support probability predictions")
            return

        probabilities = self.model.predict_proba(self.incoming_data)

        confidences = np.max(probabilities, axis=1)

        avg_confidence = np.mean(confidences)

        print("Average prediction confidence:", round(avg_confidence, 4))

        return avg_confidence