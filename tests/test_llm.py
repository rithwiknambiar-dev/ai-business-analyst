import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.ingestion.data_loader import DataLoader
from src.eda.exploratory_analysis import ExploratoryAnalysis
from src.insights.insight_generator import InsightGenerator
from src.rag.context_builder import ContextBuilder
from src.rag.llm_handler import LLMHandler


def main():

    print("\nLoading Dataset...\n")

    # Load Dataset
    df = DataLoader.load_data()

    print("Dataset Loaded Successfully")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # Generate EDA Report
    print("\nGenerating EDA Report...\n")

    eda = ExploratoryAnalysis(df)

    eda_report = eda.generate_eda_report()

    print("EDA Report Generated Successfully")

    # Generate Business Insights
    print("\nGenerating Insights...\n")

    insight_generator = InsightGenerator(
        eda_report
    )

    insights = insight_generator.generate_all_insights()

    print("Insights Generated Successfully")

    # Build Context
    print("\nBuilding AI Context...\n")

    context_builder = ContextBuilder(
        eda_report,
        insights
    )

    context = context_builder.build_context()

    print("Context Built Successfully")

    # Initialize Gemini
    print("\nInitializing Gemini...\n")

    llm = LLMHandler()

    print("Gemini Connected Successfully")

    # Test Questions
    test_questions = [

        "Which region performs best?",

        "What is the most profitable category?",

        "Summarize this business dataset.",

        "What business recommendations would you give?"
    ]

    print("\n" + "=" * 80)
    print("AI BUSINESS ANALYST TEST")
    print("=" * 80)

    for index, question in enumerate(
        test_questions,
        start=1
    ):

        print(f"\nQuestion {index}:")
        print(question)

        print("\nGenerating Response...\n")

        try:

            response = llm.ask_question(
                context,
                question
            )

            print(response)

        except Exception as e:

            print(
                f"Error: {str(e)}"
            )

        print("\n" + "-" * 80)


if __name__ == "__main__":
    main()