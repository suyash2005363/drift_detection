import pandas as pd
import joblib


class PredictionMonitor:

    def __init__(self, model_path, reference_data, incoming_data):

        self.model = joblib.load(model_path)
        self.reference_data = reference_data
        self.incoming_data = incoming_data

    def run(self):

        print("\nRunning Prediction Monitoring...\n")

        ref_predictions = self.model.predict(self.reference_data)
        incoming_predictions = self.model.predict(self.incoming_data)

        ref_distribution = pd.Series(ref_predictions).value_counts(normalize=True)
        incoming_distribution = pd.Series(incoming_predictions).value_counts(normalize=True)

        print("Reference Prediction Distribution:\n", ref_distribution)
        print("\nIncoming Prediction Distribution:\n", incoming_distribution)

        print("\nPrediction monitoring completed")