import sys
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.schema.schema_analyzer import SchemaAnalyzer, analyze_schema


def test_analyze_schema_detects_mixed_business_dataset():
    df = pd.DataFrame(
        {
            "Employee ID": [101, 102, 103, 104],
            "Department": ["Engineering", "Sales", "Engineering", "HR"],
            "Hire Date": [
                "2024-01-15",
                "2023-06-30",
                "2022-03-10",
                "2024-11-01",
            ],
            "Salary": [90000, 76000, 88000, 65000],
            "Is Active": ["Yes", "No", "Yes", "Yes"],
            "Notes": [
                "Consistently leads cross-functional planning with careful documentation.",
                "Recently transferred teams and is ramping on a new operational workflow.",
                "Mentors analysts and maintains detailed handoff notes for stakeholders.",
                "Coordinates hiring loops and writes thorough candidate evaluation summaries.",
            ],
        }
    )

    schema = analyze_schema(df)

    assert schema["id_columns"] == ["Employee ID"]
    assert schema["categorical_columns"] == ["Department"]
    assert schema["date_columns"] == ["Hire Date"]
    assert schema["numeric_columns"] == ["Salary"]
    assert schema["boolean_columns"] == ["Is Active"]
    assert schema["text_columns"] == ["Notes"]


def test_analyze_schema_preserves_superstore_column_classification():
    df = pd.DataFrame(
        {
            "Order ID": ["CA-2024-001", "CA-2024-002", "CA-2024-003"],
            "Order Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "Postal Code": [94105, 10001, 98101],
            "Region": ["West", "East", "West"],
            "Category": ["Technology", "Furniture", "Technology"],
            "Segment": ["Consumer", "Corporate", "Consumer"],
            "Sales": [250.5, 100.0, 320.75],
            "Profit": [42.0, -5.0, 80.5],
            "Quantity": [2, 1, 4],
            "Discount": [0.0, 0.2, 0.1],
        }
    )

    schema = SchemaAnalyzer(df).analyze()

    assert schema["id_columns"] == ["Order ID", "Postal Code"]
    assert schema["date_columns"] == ["Order Date"]
    assert schema["categorical_columns"] == ["Region", "Category", "Segment"]
    assert schema["numeric_columns"] == ["Sales", "Profit", "Quantity", "Discount"]


def test_analyze_schema_detects_healthcare_style_columns():
    df = pd.DataFrame(
        {
            "patient_id": ["P001", "P002", "P003", "P004"],
            "visit_timestamp": pd.to_datetime(
                ["2025-02-01", "2025-02-03", "2025-02-04", "2025-02-08"]
            ),
            "diagnosis": ["Flu", "Diabetes", "Flu", "Hypertension"],
            "readmitted": [True, False, False, True],
            "length_of_stay": [2, 5, 1, 7],
            "clinical_summary": [
                "Patient reported fever and cough with mild fatigue over several days.",
                "Routine follow-up showed stable glucose levels after medication changes.",
                "Short observation visit completed with symptoms improving by discharge.",
                "Blood pressure remained elevated and required adjusted treatment planning.",
            ],
        }
    )

    schema = analyze_schema(df)

    assert schema["id_columns"] == ["patient_id"]
    assert schema["date_columns"] == ["visit_timestamp"]
    assert schema["categorical_columns"] == ["diagnosis"]
    assert schema["boolean_columns"] == ["readmitted"]
    assert schema["numeric_columns"] == ["length_of_stay"]
    assert schema["text_columns"] == ["clinical_summary"]
