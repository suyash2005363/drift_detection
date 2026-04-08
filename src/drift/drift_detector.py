from scipy.stats import ks_2samp
import pandas as pd


class DriftDetector:

    def __init__(self, reference_data, incoming_data):

        self.reference_data = reference_data
        self.incoming_data = incoming_data

    def detect_drift(self):

        drift_results = {}

        for column in self.reference_data.columns:

            if pd.api.types.is_numeric_dtype(self.reference_data[column]):

                stat, p_value = ks_2samp(
                    self.reference_data[column],
                    self.incoming_data[column]
                )

                drift = p_value < 0.05

                drift_results[column] = {
                    "p_value": p_value,
                    "drift_detected": drift
                }

        return drift_results

    def run(self):

        print("\nRunning Drift Detection...\n")

        results = self.detect_drift()

        drift_count = 0

        for feature, result in results.items():

            print(f"Feature: {feature}")
            print(f"P-value: {result['p_value']:.5f}")

            if result["drift_detected"]:
                print("Drift Detected\n")
                drift_count += 1
            else:
                print("No Drift\n")

        print("Total features with drift:", drift_count)