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

        # Get common columns
        common_columns = list(
            set(reference_df.columns).intersection(set(current_df.columns))
        )

        for column in common_columns:
            try:
                # Only numeric columns
                if pd.api.types.is_numeric_dtype(reference_df[column]):

                    ref_data = reference_df[column].dropna()
                    curr_data = current_df[column].dropna()

                    if len(ref_data) > 0 and len(curr_data) > 0:

                        stat, p_value = ks_2samp(ref_data, curr_data)

                        drift_report[column] = {
                            "p_value": float(p_value),
                            "drift_detected": bool(p_value < self.threshold)
                        }

                    else:
                        drift_report[column] = {
                            "error": "Insufficient data"
                        }

            except Exception as e:
                drift_report[column] = {
                    "error": str(e)
                }

        return drift_report