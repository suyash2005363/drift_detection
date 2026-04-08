class AlertSystem:

    def __init__(self, drift_count, total_features, confidence):

        self.drift_count = drift_count
        self.total_features = total_features
        self.confidence = confidence

    def run(self):

        print("\nRunning Alert System...\n")

        drift_ratio = self.drift_count / self.total_features

        if drift_ratio > 0.2:

            print("ALERT: Significant data drift detected!")

        if self.confidence < 0.6:

            print("ALERT: Model confidence dropped!")

        if drift_ratio <= 0.2 and self.confidence >= 0.6:

            print("System is stable")