import pandas as pd
from scipy.stats import ks_2samp

class DriftDetector:
    def __init__(self, threshold=0.05):
        self.threshold = threshold

    def detect_drift(self, reference_df, current_df):
        """
        Detect drift between reference and current dataset
        using Kolmogorov-Smirnov test
        """
        drift_report = {}

        # Ensure same columns
        common_columns = list(set(reference_df.columns).intersection(set(current_df.columns)))

        for column in common_columns:
            try:
                # Only numeric columns
                if pd.api.types.is_numeric_dtype(reference_df[column]):

                    stat, p_value = ks_2samp(
                        reference_df[column],
                        current_df[column]
                    )

                    drift_report[column] = {
                        "p_value": float(p_value),
                        "drift_detected": bool(p_value < self.threshold)
                    }

            except Exception as e:
                drift_report[column] = {
                    "error": str(e)
                }

        return drift_report