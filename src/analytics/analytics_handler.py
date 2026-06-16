from src.analytics.analytics_engine import (
    AnalyticsEngine
)

from src.analytics.query_patterns import (
    QueryPatterns
)

from src.analytics.question_analyzer import (
    QuestionAnalyzer
)

from src.analytics.semantic_mapper import (
    SemanticMapper
)


class AnalyticsHandler:

    def __init__(self, df):

        self.df = df

        self.engine = AnalyticsEngine(
            df
        )

    def answer_question(
        self,
        question
    ):

        question_type = (
            QueryPatterns
            .detect_question_type(
                question
            )
        )

        if question_type is None:

            return None

        try:

            # =====================================
            # GROUP BY QUESTIONS
            # =====================================

            if question_type == "groupby":

                measure_column, group_column = (
                    QuestionAnalyzer
                    .find_groupby_columns(
                        question,
                        self.engine.get_columns()
                    )
                )

                print(
                    "\n========== GROUPBY DEBUG =========="
                )

                print(
                    f"Question: {question}"
                )

                print(
                    f"Measure Column: {measure_column}"
                )

                print(
                    f"Group Column: {group_column}"
                )

                print(
                    "===================================\n"
                )

                # ---------------------------------

                if (
                    "average" in question.lower()
                    or
                    "avg" in question.lower()
                    or
                    "mean" in question.lower()
                ):

                    if (
                        measure_column
                        and
                        group_column
                    ):

                        result = (
                            self.engine
                            .groupby_average(
                                measure_column,
                                group_column
                            )
                        )

                        return (
                            f"Average "
                            f"{measure_column} "
                            f"by "
                            f"{group_column}:\n\n"
                            f"{result}"
                        )

                # ---------------------------------

                if (
                    "total" in question.lower()
                    or
                    "sum" in question.lower()
                ):

                    if (
                        measure_column
                        and
                        group_column
                    ):

                        result = (
                            self.engine
                            .groupby_total(
                                measure_column,
                                group_column
                            )
                        )

                        return (
                            f"Total "
                            f"{measure_column} "
                            f"by "
                            f"{group_column}:\n\n"
                            f"{result}"
                        )

                # ---------------------------------

                if (
                    "count" in question.lower()
                    or
                    "how many" in question.lower()
                    or
                    "number of" in question.lower()
                ):

                    if group_column:

                        result = (
                            self.engine
                            .groupby_count(
                                group_column
                            )
                        )

                        return (
                            f"Count by "
                            f"{group_column}:\n\n"
                            f"{result}"
                        )

            # =====================================
            # STANDARD ANALYTICS
            # =====================================

            column = (
                SemanticMapper.find_column(
                    question,
                    self.engine.get_columns()
                )
            )

            value_column, value = (
                QuestionAnalyzer
                .find_matching_value(
                    question,
                    self.df
                )
            )

            # =====================================
            # COUNT
            # =====================================

            if (
                question_type == "count"
                and value_column
                and value
            ):

                count = (
                    self.engine
                    .count_records(
                        value_column,
                        value
                    )
                )

                return (
                    f"{count} records match "
                    f"{value_column} = {value}."
                )

            # =====================================
            # AVERAGE
            # =====================================

            if (
                question_type == "average"
                and column
            ):

                result = (
                    self.engine.average(
                        column
                    )
                )

                return (
                    f"The average "
                    f"{column} is "
                    f"{result}."
                )

            # =====================================
            # MAXIMUM
            # =====================================

            if (
                question_type == "maximum"
                and column
            ):

                result = (
                    self.engine.maximum(
                        column
                    )
                )

                return (
                    f"The maximum "
                    f"{column} is "
                    f"{result}."
                )

            # =====================================
            # MINIMUM
            # =====================================

            if (
                question_type == "minimum"
                and column
            ):

                result = (
                    self.engine.minimum(
                        column
                    )
                )

                return (
                    f"The minimum "
                    f"{column} is "
                    f"{result}."
                )

            # =====================================
            # TOTAL
            # =====================================

            if (
                question_type == "total"
                and column
            ):

                result = (
                    self.engine.total(
                        column
                    )
                )

                return (
                    f"The total "
                    f"{column} is "
                    f"{result}."
                )

        except Exception as e:

            print(
                f"Analytics Error: {e}"
            )

            return None

        return None