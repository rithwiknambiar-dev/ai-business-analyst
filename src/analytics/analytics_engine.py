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

            measure_column
            not in self.df.columns

            or

            group_column
            not in self.df.columns

        ):

            return None

        temp_df = self.df.copy()

        temp_df[
            measure_column
        ] = pd.to_numeric(

            temp_df[
                measure_column
            ],

            errors="coerce"
        )

        result = (

            temp_df.groupby(
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

            measure_column
            not in self.df.columns

            or

            group_column
            not in self.df.columns

        ):

            return None

        temp_df = self.df.copy()

        temp_df[
            measure_column
        ] = pd.to_numeric(

            temp_df[
                measure_column
            ],

            errors="coerce"
        )

        result = (

            temp_df.groupby(
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
    # ADVANCED ANALYTICS
    # =====================================

    def correlation_matrix(self):

        numeric_df = (

            self.df.select_dtypes(
                include=["number"]
            )

        )

        if numeric_df.empty:

            return None

        return numeric_df.corr()

    def top_correlations(
        self,
        limit=10
    ):

        corr = self.correlation_matrix()

        if corr is None:

            return None

        correlations = []

        columns = corr.columns

        for i in range(
            len(columns)
        ):

            for j in range(
                i + 1,
                len(columns)
            ):

                correlations.append(

                    (
                        columns[i],
                        columns[j],
                        round(
                            corr.iloc[i, j],
                            3
                        )
                    )

                )

        correlations.sort(

            key=lambda x: abs(
                x[2]
            ),

            reverse=True
        )

        return correlations[:limit]

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