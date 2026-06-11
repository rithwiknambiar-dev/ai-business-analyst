import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.ingestion.data_loader import DataLoader
from src.eda.exploratory_analysis import ExploratoryAnalysis


df = DataLoader.load_data()

eda = ExploratoryAnalysis(df)

report = eda.generate_eda_report()

print("\nEDA REPORT\n")

for section, values in report.items():

    print(f"\n{section.upper()}")

    print(values)