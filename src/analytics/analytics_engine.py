import pandas as pd


class AnalyticsEngine:

    def __init__(self, df):

        self.df = df

    # =====================================
    # BASIC ANALYTICS
    # =====================================

    def count_records(
        self,
        column,
        value
    ):

        if column not in self.df.columns:

            return None

        return len(
            self.df[
                self.df[column]
                .astype(str)
                .str.lower()
                ==
                str(value).lower()
            ]
        )

    def average(
        self,
        column
    ):

        if column not in self.df.columns:

            return None

        return round(
            pd.to_numeric(
                self.df[column],
                errors="coerce"
            ).mean(),
            2
        )

    def maximum(
        self,
        column
    ):

        if column not in self.df.columns:

            return None

        return (
            pd.to_numeric(
                self.df[column],
                errors="coerce"
            )
            .max()
        )

    def minimum(
        self,
        column
    ):

        if column not in self.df.columns:

            return None

        return (
            pd.to_numeric(
                self.df[column],
                errors="coerce"
            )
            .min()
        )

    def total(
        self,
        column
    ):

        if column not in self.df.columns:

            return None

        return round(
            pd.to_numeric(
                self.df[column],
                errors="coerce"
            ).sum(),
            2
        )

    # =====================================
    # GROUP BY ANALYTICS
    # =====================================

    def groupby_average(
        self,
        measure_column,
        group_column
    ):

        if (
            measure_column not in self.df.columns
            or
            group_column not in self.df.columns
        ):

            return None

        result = (
            self.df.groupby(
                group_column
            )[measure_column]
            .mean()
            .round(2)
            .sort_values(
                ascending=False
            )
        )

        return result.to_dict()

    def groupby_total(
        self,
        measure_column,
        group_column
    ):

        if (
            measure_column not in self.df.columns
            or
            group_column not in self.df.columns
        ):

            return None

        result = (
            self.df.groupby(
                group_column
            )[measure_column]
            .sum()
            .round(2)
            .sort_values(
                ascending=False
            )
        )

        return result.to_dict()

    def groupby_count(
        self,
        group_column
    ):

        if (
            group_column
            not in self.df.columns
        ):

            return None

        result = (
            self.df[
                group_column
            ]
            .value_counts()
        )

        return result.to_dict()

    # =====================================
    # UTILITIES
    # =====================================

    def unique_values(
        self,
        column
    ):

        if column not in self.df.columns:

            return []

        return (
            self.df[column]
            .dropna()
            .unique()
            .tolist()
        )

    def column_exists(
        self,
        column
    ):

        return (
            column in self.df.columns
        )

    def get_columns(self):

        return (
            self.df.columns.tolist()
        )