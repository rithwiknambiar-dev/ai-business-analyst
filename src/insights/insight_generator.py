class InsightGenerator:

    def __init__(self, eda_report):
        self.eda_report = eda_report

    def generate_dataset_summary_insight(self):

        summary = self.eda_report.get(
            "dataset_summary",
            {}
        )

        rows = summary.get(
            "rows",
            0
        )

        columns = summary.get(
            "columns",
            0
        )

        duplicates = summary.get(
            "duplicate_rows",
            0
        )

        missing = summary.get(
            "missing_values",
            0
        )

        return (
            f"The dataset contains {rows:,} rows and "
            f"{columns} columns. "
            f"There are {missing:,} missing values and "
            f"{duplicates:,} duplicate records."
        )

    def generate_numeric_insight(self):

        numeric_summary = self.eda_report.get(
            "numeric_summary",
            {}
        )

        if not numeric_summary:

            return (
                "No numeric columns were detected "
                "for statistical analysis."
            )

        insights = []

        for column, stats in list(
            numeric_summary.items()
        )[:3]:

            insights.append(
                f"{column} has an average value of "
                f"{stats['mean']:,.2f} "
                f"with values ranging from "
                f"{stats['min']:,.2f} to "
                f"{stats['max']:,.2f}."
            )

        return " ".join(insights)

    def generate_categorical_insight(self):

        categorical_summary = self.eda_report.get(
            "categorical_summary",
            {}
        )

        if not categorical_summary:

            return (
                "No categorical columns were detected."
            )

        column = next(
            iter(categorical_summary)
        )

        values = categorical_summary[column]

        if not values:

            return (
                f"No category distribution "
                f"available for {column}."
            )

        top_value = max(
            values,
            key=values.get
        )

        count = values[top_value]

        return (
            f"The most common value in "
            f"{column} is '{top_value}' "
            f"with {count:,} occurrences."
        )

    def generate_date_insight(self):

        date_summary = self.eda_report.get(
            "date_summary",
            {}
        )

        if not date_summary:

            return (
                "No date columns were detected."
            )

        column = next(
            iter(date_summary)
        )

        details = date_summary[column]

        return (
            f"The dataset spans from "
            f"{details['start_date']} "
            f"to {details['end_date']} "
            f"based on {column}."
        )

    def generate_correlation_insight(self):

        correlations = self.eda_report.get(
            "correlation_analysis",
            {}
        )

        if not correlations:

            return (
                "Insufficient numeric columns "
                "for correlation analysis."
            )

        strongest_pair = max(
            correlations,
            key=lambda x: abs(
                correlations[x]
            )
        )

        value = correlations[
            strongest_pair
        ]

        return (
            f"The strongest detected "
            f"relationship is between "
            f"{strongest_pair} "
            f"with a correlation of "
            f"{value:.3f}."
        )

    def generate_outlier_insight(self):

        outlier_report = self.eda_report.get(
            "outlier_analysis",
            {}
        )

        if not outlier_report:

            return (
                "No outlier analysis was available."
            )

        highest_column = max(
            outlier_report,
            key=lambda x:
            outlier_report[x][
                "outlier_count"
            ]
        )

        count = outlier_report[
            highest_column
        ][
            "outlier_count"
        ]

        percentage = outlier_report[
            highest_column
        ][
            "outlier_percentage"
        ]

        return (
            f"{highest_column} contains "
            f"{count:,} potential outliers "
            f"representing {percentage}% "
            f"of the records."
        )

    def generate_data_quality_insight(self):

        missing_values = self.eda_report.get(
            "missing_value_analysis",
            {}
        )

        if not missing_values:

            return (
                "No missing values were detected."
            )

        column = max(
            missing_values,
            key=missing_values.get
        )

        count = missing_values[column]

        return (
            f"The column '{column}' contains "
            f"the highest number of missing "
            f"values ({count:,})."
        )

    def generate_all_insights(self):

        return [

            self.generate_dataset_summary_insight(),

            self.generate_numeric_insight(),

            self.generate_categorical_insight(),

            self.generate_date_insight(),

            self.generate_correlation_insight(),

            self.generate_outlier_insight(),

            self.generate_data_quality_insight()

        ]