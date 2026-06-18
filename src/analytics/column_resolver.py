from difflib import get_close_matches


class ColumnResolver:

    def __init__(
        self,
        columns,
        dataset_summary
    ):

        self.columns = columns

        self.metrics = (
            dataset_summary.get(
                "candidate_metrics",
                []
            )
        )

        self.dimensions = (
            dataset_summary.get(
                "candidate_dimensions",
                []
            )
        )

    # =====================================
    # RESOLVE METRIC
    # =====================================

    def resolve_metric(
        self,
        metric_text
    ):

        if not metric_text:

            return None

        metric_text = (
            metric_text
            .lower()
            .strip()
        )

        # Exact match

        for column in self.metrics:

            if (
                metric_text
                ==
                column.lower()
            ):

                return column

        # Partial match

        for column in self.metrics:

            if (
                metric_text
                in
                column.lower()
            ):

                return column

            if (
                column.lower()
                in
                metric_text
            ):

                return column

        # Fuzzy match

        matches = get_close_matches(

            metric_text,

            self.metrics,

            n=1,

            cutoff=0.4
        )

        if matches:

            return matches[0]

        return None

    # =====================================
    # RESOLVE DIMENSION
    # =====================================

    def resolve_dimension(
        self,
        dimension_text
    ):

        if not dimension_text:

            return None

        dimension_text = (
            dimension_text
            .lower()
            .strip()
        )

        # Exact match

        for column in self.dimensions:

            if (
                dimension_text
                ==
                column.lower()
            ):

                return column

        # Partial match

        for column in self.dimensions:

            if (
                dimension_text
                in
                column.lower()
            ):

                return column

            if (
                column.lower()
                in
                dimension_text
            ):

                return column

        # Fuzzy match

        matches = get_close_matches(

            dimension_text,

            self.dimensions,

            n=1,

            cutoff=0.4
        )

        if matches:

            return matches[0]

        return None