import pandas as pd
from scipy.stats import ks_2samp, chisquare

class DriftDetector:
    def __init__(self, threshold=0.05):
        self.threshold = threshold

    def detect_drift(self, reference_df, current_df):

        drift_report = {}

        common_columns = list(
            set(reference_df.columns).intersection(set(current_df.columns))
        )

        for column in common_columns:
            try:

                ref_col = reference_df[column]
                curr_col = current_df[column]

                # 🔹 Numerical Features → KS Test
                if pd.api.types.is_numeric_dtype(ref_col):

                    ref_data = ref_col.dropna()
                    curr_data = curr_col.dropna()

                    if len(ref_data) > 0 and len(curr_data) > 0:
                        stat, p_value = ks_2samp(ref_data, curr_data)

                        drift_report[column] = {
                            "p_value": float(p_value),
                            "drift_detected": bool(p_value < self.threshold),
                            "type": "numerical"
                        }

                # 🔹 Categorical Features → Chi-Square Test
                else:

                    ref_counts = ref_col.value_counts()
                    curr_counts = curr_col.value_counts()

                    # Align categories
                    all_categories = set(ref_counts.index).union(set(curr_counts.index))
                    ref_counts = ref_counts.reindex(all_categories, fill_value=0)
                    curr_counts = curr_counts.reindex(all_categories, fill_value=0)

                    stat, p_value = chisquare(curr_counts, ref_counts)

                    drift_report[column] = {
                        "p_value": float(p_value),
                        "drift_detected": bool(p_value < self.threshold),
                        "type": "categorical"
                    }

            except Exception as e:
                drift_report[column] = {
                    "error": str(e)
                }

        return drift_report