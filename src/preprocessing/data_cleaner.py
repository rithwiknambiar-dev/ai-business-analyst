import pandas as pd


class DataCleaner:

    def __init__(self, df):
        self.df = df

    def generate_cleaning_report(self):

        report = {

            "missing_values":
                self.df.isnull().sum().to_dict(),

            "duplicate_rows":
                int(
                    self.df.duplicated().sum()
                ),

            "invalid_dates":
                self.check_invalid_dates()
        }

        return report

    def check_invalid_dates(self):

        invalid_dates = {}

        for column in self.df.columns:

            if "date" in column.lower():

                converted = pd.to_datetime(
                    self.df[column],
                    errors="coerce"
                )

                invalid_dates[column] = int(
                    converted.isnull().sum()
                )

        return invalid_dates