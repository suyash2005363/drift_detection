import pandas as pd
import yaml
import os


class DataIngestion:

    def __init__(self, config_path):

        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        self.reference_path = config["reference_data_path"]
        self.incoming_folder = config["incoming_data_folder"]

    def load_reference_data(self):

        print("\nLoading reference dataset...")

        reference_data = pd.read_csv(self.reference_path)

        print("Reference data shape:", reference_data.shape)

        return reference_data

    def load_batches(self):

        print("\nLoading incoming batches...")

        batch_files = sorted(os.listdir(self.incoming_folder))

        batches = []

        for file in batch_files:

            if file.endswith(".csv"):

                path = os.path.join(self.incoming_folder, file)

                data = pd.read_csv(path)

                batches.append((file, data))

        print(f"{len(batches)} batches loaded")

        return batches