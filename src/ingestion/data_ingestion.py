import pandas as pd
import os

class DataIngestion:
    def __init__(self):
        # ✅ Updated paths based on your structure
        self.reference_path = "data/reference/reference_dataset.csv"
        self.batch_paths = [
            "data/income/batch_1.csv",
            "data/income/batch_2.csv",
            "data/income/batch_3.csv"
        ]

    def load_reference_data(self):
        """Load reference dataset"""
        if not os.path.exists(self.reference_path):
            raise FileNotFoundError(f"Reference dataset not found at {self.reference_path}")
        
        df = pd.read_csv(self.reference_path)
        print("✅ Reference data loaded")
        return df

    def load_batch_data(self):
        """Load all batch datasets"""
        batches = []

        for path in self.batch_paths:
            if not os.path.exists(path):
                print(f"⚠️ Warning: {path} not found, skipping")
                continue

            df = pd.read_csv(path)
            batches.append(df)
            print(f"✅ Loaded batch: {path}")

        return batches