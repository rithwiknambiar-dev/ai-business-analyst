import re
from dataclasses import dataclass

import pandas as pd


@dataclass
class SchemaAnalyzer:
    df: pd.DataFrame
    sample_size: int = 1000
    categorical_unique_limit: int = 30
    categorical_unique_ratio: float = 0.2
    id_unique_ratio: float = 0.9
    date_parse_ratio: float = 0.75

    def analyze(self) -> dict:
        schema = {
            "numeric_columns": [],
            "categorical_columns": [],
            "date_columns": [],
            "text_columns": [],
            "id_columns": [],
            "boolean_columns": [],
        }

        for column in self.df.columns:
            column_type = self._classify_column(column)
            schema[column_type].append(column)

        return schema

    def _classify_column(self, column: str) -> str:
        series = self.df[column]

        if self._is_boolean(series):
            return "boolean_columns"

        if self._is_date(column, series):
            return "date_columns"

        if self._is_identifier(column, series):
            return "id_columns"

        if pd.api.types.is_numeric_dtype(series):
            return "numeric_columns"

        if self._is_text(series):
            return "text_columns"

        if self._is_categorical(series):
            return "categorical_columns"

        return "text_columns"

    def _is_boolean(self, series: pd.Series) -> bool:
        if pd.api.types.is_bool_dtype(series):
            return True

        values = self._non_null_sample(series)
        if values.empty:
            return False

        normalized_values = {
            str(value).strip().lower()
            for value in values.unique()
        }

        boolean_sets = [
            {"true", "false"},
            {"yes", "no"},
            {"y", "n"},
            {"1", "0"},
        ]

        return any(
            normalized_values.issubset(boolean_set)
            and len(normalized_values) <= 2
            for boolean_set in boolean_sets
        )

    def _is_date(self, column: str, series: pd.Series) -> bool:
        if pd.api.types.is_datetime64_any_dtype(series):
            return True

        if pd.api.types.is_numeric_dtype(series):
            return False

        values = self._non_null_sample(series)
        if values.empty:
            return False

        parsed_values = pd.to_datetime(
            values,
            errors="coerce",
            format="mixed",
        )

        parse_ratio = parsed_values.notna().mean()
        if parse_ratio >= self.date_parse_ratio:
            return True

        return self._has_date_name(column) and parse_ratio >= 0.5

    def _is_identifier(self, column: str, series: pd.Series) -> bool:
        values = self._non_null_sample(series)
        if values.empty:
            return False

        unique_ratio = values.nunique(dropna=True) / len(values)
        if self._has_identifier_name(column):
            return unique_ratio >= 0.5 or values.nunique(dropna=True) > 20

        if pd.api.types.is_numeric_dtype(series):
            return False

        return (
            unique_ratio >= self.id_unique_ratio
            and self._code_like_ratio(values) >= 0.8
        )

    def _is_categorical(self, series: pd.Series) -> bool:
        if isinstance(series.dtype, pd.CategoricalDtype):
            return True

        values = self._non_null_sample(series)
        if values.empty:
            return False

        unique_count = values.nunique(dropna=True)
        unique_ratio = unique_count / len(values)

        return (
            unique_count <= self.categorical_unique_limit
            or unique_ratio <= self.categorical_unique_ratio
        )

    def _is_text(self, series: pd.Series) -> bool:
        values = self._non_null_sample(series)
        if values.empty:
            return False

        string_values = values.astype(str).str.strip()
        average_length = string_values.str.len().mean()
        average_words = string_values.str.split().str.len().mean()

        return average_length >= 50 or average_words >= 8

    def _non_null_sample(self, series: pd.Series) -> pd.Series:
        return series.dropna().head(self.sample_size)

    @staticmethod
    def _code_like_ratio(values: pd.Series) -> float:
        if values.empty:
            return 0.0

        string_values = values.astype(str).str.strip()
        code_like = string_values.str.match(r"^[A-Za-z0-9_.@:-]+$")
        return float(code_like.mean())

    @staticmethod
    def _has_date_name(column: str) -> bool:
        normalized = SchemaAnalyzer._normalize_column_name(column)
        date_tokens = {
            "date",
            "time",
            "datetime",
            "timestamp",
            "created",
            "updated",
            "month",
            "year",
        }
        return bool(date_tokens.intersection(normalized))

    @staticmethod
    def _has_identifier_name(column: str) -> bool:
        normalized = SchemaAnalyzer._normalize_column_name(column)
        identifier_tokens = {
            "code",
            "id",
            "identifier",
            "postal",
            "uuid",
            "guid",
            "key",
            "zip",
        }
        return bool(identifier_tokens.intersection(normalized))

    @staticmethod
    def _normalize_column_name(column: str) -> set[str]:
        return {
            token
            for token in re.split(r"[^a-z0-9]+", str(column).lower())
            if token
        }


def analyze_schema(df: pd.DataFrame) -> dict:
    return SchemaAnalyzer(df).analyze()
