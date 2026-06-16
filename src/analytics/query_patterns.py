import re


class QueryPatterns:

    COUNT_PATTERNS = [

        r"how many (.+)",
        r"count (.+)",
        r"number of (.+)"
    ]

    AVERAGE_PATTERNS = [

        r"average (.+)",
        r"mean (.+)",
        r"avg (.+)"
    ]

    MAX_PATTERNS = [

        r"maximum (.+)",
        r"highest (.+)",
        r"max (.+)"
    ]

    MIN_PATTERNS = [

        r"minimum (.+)",
        r"lowest (.+)",
        r"min (.+)"
    ]

    TOTAL_PATTERNS = [

        r"total (.+)",
        r"sum of (.+)"
    ]

    GROUPBY_PATTERNS = [

        r"average (.+) by (.+)",
        r"mean (.+) by (.+)",
        r"avg (.+) by (.+)",

        r"count (.+) by (.+)",
        r"number of (.+) by (.+)",
        r"how many (.+) by (.+)",

        r"total (.+) by (.+)",
        r"sum of (.+) by (.+)"
    ]

    @staticmethod
    def detect_question_type(
        question
    ):

        question = question.lower()

        # =====================================
        # GROUP BY DETECTION FIRST
        # =====================================

        for pattern in (
            QueryPatterns.GROUPBY_PATTERNS
        ):

            if re.search(
                pattern,
                question
            ):

                return "groupby"

        # =====================================
        # COUNT
        # =====================================

        for pattern in (
            QueryPatterns.COUNT_PATTERNS
        ):

            if re.search(
                pattern,
                question
            ):

                return "count"

        # =====================================
        # AVERAGE
        # =====================================

        for pattern in (
            QueryPatterns.AVERAGE_PATTERNS
        ):

            if re.search(
                pattern,
                question
            ):

                return "average"

        # =====================================
        # MAXIMUM
        # =====================================

        for pattern in (
            QueryPatterns.MAX_PATTERNS
        ):

            if re.search(
                pattern,
                question
            ):

                return "maximum"

        # =====================================
        # MINIMUM
        # =====================================

        for pattern in (
            QueryPatterns.MIN_PATTERNS
        ):

            if re.search(
                pattern,
                question
            ):

                return "minimum"

        # =====================================
        # TOTAL
        # =====================================

        for pattern in (
            QueryPatterns.TOTAL_PATTERNS
        ):

            if re.search(
                pattern,
                question
            ):

                return "total"

        return None