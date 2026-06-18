from src.analytics.analytics_engine import (
    AnalyticsEngine
)

from src.analytics.query_intent import (
    QueryIntentParser
)

from src.analytics.column_resolver import (
    ColumnResolver
)


class AnalyticsHandler:

    def __init__(
        self,
        df,
        dataset_summary
    ):

        self.df = df

        self.engine = AnalyticsEngine(
            df
        )

        self.resolver = ColumnResolver(
            df.columns.tolist(),
            dataset_summary
        )

    def answer_question(
        self,
        question
    ):

        try:

            intent = (
                QueryIntentParser.parse(
                    question
                )
            )

            if (
                intent.operation
                is None
            ):

                return None

            metric_column = (
                self.resolver
                .resolve_metric(
                    intent.metric_text
                )
            )

            dimension_column = (
                self.resolver
                .resolve_dimension(
                    intent.dimension_text
                )
            )

            # =====================================
            # GROUP BY ANALYTICS
            # =====================================

            if dimension_column:

                if (
                    intent.operation
                    ==
                    "average"
                ):

                    result = (
                        self.engine
                        .groupby_average(
                            metric_column,
                            dimension_column
                        )
                    )

                    return (
                        f"Average "
                        f"{metric_column} "
                        f"by "
                        f"{dimension_column}:\n\n"
                        f"{result}"
                    )

                if (
                    intent.operation
                    ==
                    "sum"
                ):

                    result = (
                        self.engine
                        .groupby_total(
                            metric_column,
                            dimension_column
                        )
                    )

                    return (
                        f"Total "
                        f"{metric_column} "
                        f"by "
                        f"{dimension_column}:\n\n"
                        f"{result}"
                    )

                if (
                    intent.operation
                    ==
                    "count"
                ):

                    result = (
                        self.engine
                        .groupby_count(
                            dimension_column
                        )
                    )

                    return (
                        f"Count by "
                        f"{dimension_column}:\n\n"
                        f"{result}"
                    )

            # =====================================
            # STANDARD ANALYTICS
            # =====================================

            if (
                metric_column
                is None
            ):

                return None

            if (
                intent.operation
                ==
                "average"
            ):

                result = (
                    self.engine
                    .average(
                        metric_column
                    )
                )

                return (
                    f"The average "
                    f"{metric_column} "
                    f"is "
                    f"{result}."
                )

            if (
                intent.operation
                ==
                "sum"
            ):

                result = (
                    self.engine
                    .total(
                        metric_column
                    )
                )

                return (
                    f"The total "
                    f"{metric_column} "
                    f"is "
                    f"{result}."
                )

            if (
                intent.operation
                ==
                "maximum"
            ):

                result = (
                    self.engine
                    .maximum(
                        metric_column
                    )
                )

                return (
                    f"The maximum "
                    f"{metric_column} "
                    f"is "
                    f"{result}."
                )

            if (
                intent.operation
                ==
                "minimum"
            ):

                result = (
                    self.engine
                    .minimum(
                        metric_column
                    )
                )

                return (
                    f"The minimum "
                    f"{metric_column} "
                    f"is "
                    f"{result}."
                )

        except Exception as e:

            print(
                f"Analytics Error: {e}"
            )

            return None

        return None