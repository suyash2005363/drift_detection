import pandas as pd
import yaml
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


CONFIG_PATH = "config/config.yaml"


with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)


reference_path = config["reference_data_path"]
incoming_path = config["incoming_data_path"]


reference_data = pd.read_csv(reference_path)
incoming_data = pd.read_csv(incoming_path)


report = Report(metrics=[DataDriftPreset()])


report.run(
    reference_data=reference_data,
    current_data=incoming_data
)


report.save_html("drift_report.html")

print("Drift report generated: drift_report.html")