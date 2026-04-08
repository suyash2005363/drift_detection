class DataValidation:

    def __init__(self, reference_data, incoming_data):

        self.reference_data = reference_data
        self.incoming_data = incoming_data

    def check_column_match(self):

        reference_columns = set(self.reference_data.columns)
        incoming_columns = set(self.incoming_data.columns)

        if reference_columns == incoming_columns:

            print("Columns match between datasets")

            return True

        else:

            missing_cols = reference_columns - incoming_columns
            extra_cols = incoming_columns - reference_columns

            print("Column mismatch detected")
            print("Missing columns:", missing_cols)
            print("Extra columns:", extra_cols)

            return False

    def check_missing_values(self):

        reference_missing = self.reference_data.isnull().sum().sum()
        incoming_missing = self.incoming_data.isnull().sum().sum()

        print("Missing values in reference data:", reference_missing)
        print("Missing values in incoming data:", incoming_missing)

    def run(self):

        print("\nRunning Data Validation...\n")

        column_check = self.check_column_match()

        if not column_check:
            raise Exception("Dataset columns do not match")

        self.check_missing_values()

        print("\nData validation completed")