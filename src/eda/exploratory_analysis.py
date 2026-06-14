import pandas as pd
import numpy as np

from src.schema.schema_analyzer import analyze_schema


class ExploratoryAnalysis:

    def __init__(self, df):
        self.df = df.copy()
        self.schema = analyze_schema(self.df)

    def get_dataset_summary(self):

        return {
            "rows": int(len(self.df)),
            "columns": int(len(self.df.columns)),
            "missing_values": int(self.df.isnull().sum().sum()),
            "duplicate_rows": int(self.df.duplicated().sum())
        }

    def get_numeric_summary(self):

        numeric_cols = self.schema["numeric_columns"]

        summary = {}

        for col in numeric_cols:

            summary[col] = {
                "sum": round(float(self.df[col].sum()), 2),
                "mean": round(float(self.df[col].mean()), 2),
                "median": round(float(self.df[col].median()), 2),
                "min": round(float(self.df[col].min()), 2),
                "max": round(float(self.df[col].max()), 2),
                "std": round(float(self.df[col].std()), 2)
            }

        return summary

    def get_categorical_summary(self):

        categorical_cols = (
            self.schema["categorical_columns"]
            + self.schema["boolean_columns"]
        )

        summary = {}

        for col in categorical_cols:

            value_counts = (
                self.df[col]
                .astype(str)
                .value_counts()
                .head(10)
                .to_dict()
            )

            summary[col] = value_counts

        return summary

    def get_date_summary(self):

        date_cols = self.schema["date_columns"]

        summary = {}

        for col in date_cols:

            valid_dates = self.df[col].dropna()

            if len(valid_dates) == 0:
                continue

            summary[col] = {
                "start_date": str(valid_dates.min()),
                "end_date": str(valid_dates.max()),
                "records": int(len(valid_dates))
            }

        return summary

    def get_correlation_analysis(self):

        numeric_cols = self.schema["numeric_columns"]

        if len(numeric_cols) < 2:
            return {}

        corr_matrix = self.df[numeric_cols].corr()

        correlations = {}

        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):

                col1 = numeric_cols[i]
                col2 = numeric_cols[j]

                correlations[
                    f"{col1} vs {col2}"
                ] = round(
                    float(
                        corr_matrix.loc[col1, col2]
                    ),
                    3
                )

        return correlations

    def get_missing_value_analysis(self):

        missing = (
            self.df
            .isnull()
            .sum()
            .sort_values(ascending=False)
        )

        return {
            col: int(val)
            for col, val in missing.items()
            if val > 0
        }

    def get_outlier_analysis(self):

        numeric_cols = self.schema["numeric_columns"]

        outlier_report = {}

        for col in numeric_cols:

            series = self.df[col].dropna()

            if len(series) < 5:
                continue

            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)

            iqr = q3 - q1

            lower = q1 - (1.5 * iqr)
            upper = q3 + (1.5 * iqr)

            outliers = series[
                (series < lower)
                | (series > upper)
            ]

            outlier_report[col] = {
                "outlier_count": int(len(outliers)),
                "outlier_percentage": round(
                    (len(outliers) / len(series)) * 100,
                    2
                )
            }

        return outlier_report

    def generate_eda_report(self):

        return {

            "dataset_summary":
                self.get_dataset_summary(),

            "numeric_summary":
                self.get_numeric_summary(),

            "categorical_summary":
                self.get_categorical_summary(),

            "date_summary":
                self.get_date_summary(),

            "correlation_analysis":
                self.get_correlation_analysis(),

            "missing_value_analysis":
                self.get_missing_value_analysis(),

            "outlier_analysis":
                self.get_outlier_analysis()
        }