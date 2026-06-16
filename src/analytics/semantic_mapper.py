import re


class SemanticMapper:

    COLUMN_SYNONYMS = {

        "MonthlyIncome": [
            "salary",
            "income",
            "pay",
            "compensation",
            "earnings"
        ],

        "Department": [
            "department",
            "team",
            "division",
            "business unit"
        ],

        "Age": [
            "age",
            "employee age"
        ],

        "JobRole": [
            "job role",
            "role",
            "position",
            "designation"
        ],

        "Attrition": [
            "attrition",
            "turnover",
            "employee leaving",
            "employee exit"
        ],

        "Gender": [
            "gender",
            "sex"
        ],

        "YearsAtCompany": [
            "tenure",
            "years in company",
            "experience"
        ]
    }

    @staticmethod
    def find_column(
        question,
        columns
    ):

        question = question.lower().strip()

        # =====================================
        # EXACT COLUMN NAME MATCH
        # =====================================

        for column in columns:

            pattern = (
                r"\b"
                + re.escape(
                    column.lower()
                )
                + r"\b"
            )

            if re.search(
                pattern,
                question
            ):

                return column

        # =====================================
        # SYNONYM MATCH
        # =====================================

        for column, synonyms in (
            SemanticMapper.COLUMN_SYNONYMS.items()
        ):

            if column not in columns:

                continue

            for synonym in synonyms:

                pattern = (
                    r"\b"
                    + re.escape(
                        synonym.lower()
                    )
                    + r"\b"
                )

                if re.search(
                    pattern,
                    question
                ):

                    return column

        return None