import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.ingestion.data_loader import DataLoader
from src.eda.exploratory_analysis import ExploratoryAnalysis
from src.insights.insight_generator import InsightGenerator
from src.rag.context_builder import ContextBuilder


df = DataLoader.load_data()

eda = ExploratoryAnalysis(df)

eda_report = eda.generate_eda_report()

insights = InsightGenerator(
    eda_report
).generate_all_insights()

context = ContextBuilder(
    eda_report,
    insights
).build_context()

print(context)