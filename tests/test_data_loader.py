import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.ingestion.data_loader import DataLoader
from src.profiling.data_profiler import DataProfiler
from src.preprocessing.data_cleaner import DataCleaner


def main():

    print("\nLoading Dataset...\n")

    df = DataLoader.load_data()

    print("Dataset Loaded Successfully")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn Names:\n")

    for column in df.columns:
        print(column)

    profiler = DataProfiler(df)

    profile = profiler.generate_profile()

    print("\nPROFILE REPORT\n")
    print(profile)

    cleaner = DataCleaner(df)

    cleaning_report = cleaner.generate_cleaning_report()

    print("\nDATA QUALITY REPORT\n")
    print(cleaning_report)


if __name__ == "__main__":
    main()