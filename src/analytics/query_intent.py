from dataclasses import dataclass
import re


@dataclass
class QueryIntent:

    operation: str | None = None

    metric_text: str | None = None

    dimension_text: str | None = None

    raw_question: str | None = None


class QueryIntentParser:

    OPERATION_PATTERNS = {

        "average": [
            r"\baverage\b",
            r"\bavg\b",
            r"\bmean\b"
        ],

        "sum": [
            r"\btotal\b",
            r"\bsum\b"
        ],

        "count": [
            r"\bcount\b",
            r"\bhow many\b",
            r"\bnumber of\b"
        ],

        "maximum": [
            r"\bmax\b",
            r"\bmaximum\b",
            r"\bhighest\b",
            r"\blargest\b",
            r"\btop\b"
        ],

        "minimum": [
            r"\bmin\b",
            r"\bminimum\b",
            r"\blowest\b",
            r"\bsmallest\b"
        ]
    }

    @classmethod
    def parse(
        cls,
        question
    ):

        question = (
            question
            .strip()
            .lower()
        )

        operation = (
            cls._detect_operation(
                question
            )
        )

        metric_text = (
            cls._extract_metric(
                question,
                operation
            )
        )

        dimension_text = (
            cls._extract_dimension(
                question
            )
        )

        return QueryIntent(

            operation=operation,

            metric_text=metric_text,

            dimension_text=dimension_text,

            raw_question=question
        )

    @classmethod
    def _detect_operation(
        cls,
        question
    ):

        for operation, patterns in (

            cls.OPERATION_PATTERNS.items()

        ):

            for pattern in patterns:

                if re.search(
                    pattern,
                    question
                ):

                    return operation

        return None

    @staticmethod
    def _extract_metric(
        question,
        operation
    ):

        if operation is None:

            return None

        question = (
            question
            .replace(
                "how many",
                ""
            )
            .replace(
                "number of",
                ""
            )
        )

        operation_words = [

            "average",
            "avg",
            "mean",

            "total",
            "sum",

            "count",

            "maximum",
            "max",
            "highest",
            "largest",
            "top",

            "minimum",
            "min",
            "lowest",
            "smallest"
        ]

        metric = question

        for word in operation_words:

            metric = re.sub(

                rf"\b{word}\b",

                "",

                metric
            )

        if " by " in metric:

            metric = metric.split(
                " by "
            )[0]

        metric = (
            metric
            .replace(
                "?",
                ""
            )
            .strip()
        )

        if metric == "":

            return None

        return metric

    @staticmethod
    def _extract_dimension(
        question
    ):

        if " by " not in question:

            return None

        parts = question.split(
            " by "
        )

        if len(parts) < 2:

            return None

        dimension = (
            parts[1]
            .replace(
                "?",
                ""
            )
            .strip()
        )

        if dimension == "":

            return None

        return dimension