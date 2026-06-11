import pandas as pd
from pathlib import Path


class DataLoader:

    @staticmethod
    def load_data():

        file_path = Path("data/raw/sales_data.csv")

        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        try:

            if file_path.suffix.lower() == ".csv":

                try:

                    df = pd.read_csv(
                        file_path,
                        encoding="utf-8"
                    )

                except UnicodeDecodeError:

                    df = pd.read_csv(
                        file_path,
                        encoding="latin1"
                    )

            elif file_path.suffix.lower() in [
                ".xlsx",
                ".xls"
            ]:

                df = pd.read_excel(
                    file_path
                )

            else:

                raise ValueError(
                    "Unsupported file format"
                )

            # Convert Date Columns

            date_columns = [
                "Order Date",
                "Ship Date"
            ]

            for column in date_columns:

                if column in df.columns:

                    df[column] = pd.to_datetime(
                        df[column],
                        errors="coerce"
                    )

            return df

        except Exception as e:

            raise Exception(
                f"Error loading dataset: {str(e)}"
            )