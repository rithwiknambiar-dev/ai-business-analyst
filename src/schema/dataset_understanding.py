import re
from dataclasses import dataclass

import pandas as pd

from src.schema.schema_analyzer import analyze_schema


@dataclass
class DatasetUnderstanding:
    df: pd.DataFrame
    schema_metadata: dict | None = None

    def summarize(self) -> dict:
        schema_metadata = self.schema_metadata or analyze_schema(self.df)
        candidate_metrics = self._candidate_metrics(schema_metadata)
        candidate_dimensions = self._candidate_dimensions(schema_metadata)
        dataset_type = self._classify_dataset_type()

        return {
            "row_count": int(self.df.shape[0]),
            "column_count": int(self.df.shape[1]),
            "missing_values": self.df.isnull().sum().to_dict(),
            "duplicate_rows": int(self.df.duplicated().sum()),
            "candidate_metrics": candidate_metrics,
            "candidate_dimensions": candidate_dimensions,
            "suggested_questions": self._suggest_questions(
                dataset_type,
                candidate_metrics,
                candidate_dimensions,
                schema_metadata,
            ),
            "dataset_type": dataset_type,
        }

    def _candidate_metrics(self, schema_metadata: dict) -> list[str]:
        excluded_columns = set(schema_metadata.get("id_columns", []))
        excluded_columns.update(schema_metadata.get("boolean_columns", []))

        return [
            column
            for column in schema_metadata.get("numeric_columns", [])
            if column not in excluded_columns
        ]

    def _candidate_dimensions(self, schema_metadata: dict) -> list[str]:
        dimensions = []

        for key in [
            "categorical_columns",
            "boolean_columns",
            "date_columns",
        ]:
            for column in schema_metadata.get(key, []):
                if column not in dimensions:
                    dimensions.append(column)

        return dimensions

    def _classify_dataset_type(self) -> str:
        tokens = self._column_tokens()
        scores = {
            "Sales": self._score(
                tokens,
                {
                    "sales",
                    "sale",
                    "profit",
                    "revenue",
                    "order",
                    "product",
                    "customer",
                    "region",
                    "discount",
                    "quantity",
                    "category",
                    "segment",
                },
            ),
            "HR": self._score(
                tokens,
                {
                    "employee",
                    "department",
                    "salary",
                    "hire",
                    "attrition",
                    "performance",
                    "manager",
                    "role",
                    "job",
                    "tenure",
                },
            ),
            "Healthcare": self._score(
                tokens,
                {
                    "patient",
                    "diagnosis",
                    "treatment",
                    "doctor",
                    "hospital",
                    "clinic",
                    "medical",
                    "readmitted",
                    "visit",
                    "claim",
                },
            ),
            "Telecom": self._score(
                tokens,
                {
                    "subscriber",
                    "churn",
                    "plan",
                    "contract",
                    "call",
                    "data",
                    "usage",
                    "network",
                    "tower",
                    "sim",
                },
            ),
            "Finance": self._score(
                tokens,
                {
                    "account",
                    "transaction",
                    "balance",
                    "credit",
                    "debit",
                    "loan",
                    "payment",
                    "invoice",
                    "bank",
                    "amount",
                },
            ),
        }

        dataset_type, score = max(
            scores.items(),
            key=lambda item: item[1],
        )

        return dataset_type if score >= 2 else "Generic"

    def _suggest_questions(
        self,
        dataset_type: str,
        candidate_metrics: list[str],
        candidate_dimensions: list[str],
        schema_metadata: dict,
    ) -> list[str]:
        questions = []

        if candidate_metrics:
            metric = candidate_metrics[0]
            questions.append(f"What is the overall summary of {metric}?")

            if candidate_dimensions:
                dimension = candidate_dimensions[0]
                questions.append(
                    f"How does {metric} vary by {dimension}?"
                )

        if len(candidate_metrics) >= 2:
            questions.append(
                "Which numeric columns are most strongly correlated?"
            )

        if schema_metadata.get("date_columns") and candidate_metrics:
            questions.append(
                f"What trend is visible over {schema_metadata['date_columns'][0]}?"
            )

        if dataset_type != "Generic":
            questions.append(
                f"What are the key patterns in this {dataset_type} dataset?"
            )
        else:
            questions.append("What are the most important patterns in this dataset?")

        questions.append("Are there missing values, duplicates, or outliers to review?")

        return questions[:6]

    def _column_tokens(self) -> set[str]:
        tokens = set()

        for column in self.df.columns:
            tokens.update(
                token
                for token in re.split(r"[^a-z0-9]+", str(column).lower())
                if token
            )

        return tokens

    @staticmethod
    def _score(tokens: set[str], keywords: set[str]) -> int:
        return len(tokens.intersection(keywords))


def understand_dataset(
    df: pd.DataFrame,
    schema_metadata: dict | None = None,
) -> dict:
    return DatasetUnderstanding(df, schema_metadata).summarize()
