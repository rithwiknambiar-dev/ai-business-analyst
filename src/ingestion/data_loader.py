from pathlib import Path

import pandas as pd

from src.schema.schema_analyzer import analyze_schema


class DataLoader:

    @staticmethod
    def load_data(file_path):

        dataset_path = Path(file_path)

        if not dataset_path.exists():

            raise FileNotFoundError(
                f"Dataset not found: {dataset_path}"
            )

        return DataLoader.load_file(
            dataset_path
        )

    @staticmethod
    def load_file(file_path):

        file_path = Path(file_path)

        df = DataLoader._read_dataset(
            file_path,
            file_path.suffix.lower()
        )

        return DataLoader.prepare_dataframe(
            df
        )

    @staticmethod
    def load_uploaded_data(uploaded_file):

        file_name = getattr(
            uploaded_file,
            "name",
            "uploaded.csv"
        )

        df = DataLoader._read_dataset(
            uploaded_file,
            Path(file_name).suffix.lower()
        )

        return DataLoader.prepare_dataframe(
            df
        )

    @staticmethod
    def prepare_dataframe(df):

        schema_metadata = analyze_schema(
            df
        )

        for column in schema_metadata.get(
            "date_columns",
            []
        ):

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed"
            )

        return df

    @staticmethod
    def _read_dataset(
        file_source,
        suffix
    ):

        if suffix == ".csv":

            try:

                return pd.read_csv(
                    file_source,
                    encoding="utf-8"
                )

            except UnicodeDecodeError:

                DataLoader._reset_file_source(
                    file_source
                )

                return pd.read_csv(
                    file_source,
                    encoding="latin1"
                )

        if suffix in [
            ".xlsx",
            ".xls"
        ]:

            return pd.read_excel(
                file_source
            )

        raise ValueError(
            f"Unsupported file format: {suffix}"
        )

    @staticmethod
    def _reset_file_source(
        file_source
    ):

        if hasattr(
            file_source,
            "seek"
        ):

            file_source.seek(0)