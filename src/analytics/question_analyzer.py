from src.analytics.semantic_mapper import (
    SemanticMapper
)


class QuestionAnalyzer:

    @staticmethod
    def find_matching_column(
        question,
        columns
    ):

        question = question.lower()

        for column in columns:

            if (
                column.lower()
                in question
            ):

                return column

        return None

    @staticmethod
    def find_matching_value(
        question,
        dataframe
    ):

        question = question.lower()

        for column in dataframe.columns:

            try:

                values = (
                    dataframe[column]
                    .dropna()
                    .astype(str)
                    .unique()
                )

                for value in values:

                    if (
                        str(value)
                        .lower()
                        in question
                    ):

                        return (
                            column,
                            value
                        )

            except Exception:

                continue

        return (
            None,
            None
        )

    # =====================================
    # GROUP BY DETECTION
    # =====================================

    @staticmethod
    def find_groupby_columns(
        question,
        columns
    ):

        question = question.lower()

        measure_column = None

        group_column = None

        # =====================================
        # FIND GROUP COLUMN
        # =====================================

        if " by " in question:

            parts = question.split(
                " by "
            )

            after_by = parts[1]

            group_column = (
                SemanticMapper.find_column(
                    after_by,
                    columns
                )
            )

        # =====================================
        # FIND MEASURE COLUMN
        # =====================================

        measure_column = (
            SemanticMapper.find_column(
                question,
                columns
            )
        )

        if (
            measure_column
            ==
            group_column
        ):

            measure_column = None

        return (
            measure_column,
            group_column
        )