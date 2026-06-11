# AI Business Analyst

An interactive, AI-powered business intelligence (BI) dashboard built with Streamlit. The application allows business analysts and decision-makers to upload raw datasets (CSV/Excel), perform data profiling, run exploratory data analysis (EDA), detect business anomalies, forecast future trends, generate summary reports, and chat with their data using a RAG (Retrieval-Augmented Generation) chatbot.

## Features

1. **Data Ingestion & Cleaning**:
   - Supports CSV and Excel formats.
   - Automatically handles delimiters, data encoding, and header validation.
   - Clean data wizard for duplicate removal, missing value imputation, and data type standardizations.

2. **Data Profiling**:
   - Computes statistical summaries, missingness percentages, uniqueness metrics, and data types.
   - Provides a comprehensive "Data Quality Score".

3. **Interactive EDA**:
   - Build custom Plotly visualizations (scatter, line, bar, box, histogram, correlation heatmap).
   - Customize dimensions, metrics, and grouping categories dynamically.

4. **KPI Engine**:
   - Automatically identifies columns representing core metrics (revenue, transactions, dates, categories).
   - Computes performance indicators (MoM growth, running totals, cumulative values).

5. **Anomaly Detection**:
   - Detects outliers, sudden spikes/drops, and pattern shifts using Isolation Forests and standard Z-score statistical bounds.
   - Isolates anomalous rows with natural language explanations.

6. **Time-Series Forecasting**:
   - Implements regression/autoregressive trends for multi-period forecasting.
   - Generates confidence intervals and overlays them on historical performance using interactive Plotly charts.

7. **RAG-Powered AI Chat**:
   - Parses tabular data, transforms row statistics into contextual text chunks, and builds semantic embeddings.
   - Employs an in-memory vector database for query-relevant retrieval.
   - Interfaces with LLM APIs (Gemini/OpenAI) using the user's API Key.
   - Falls back to a smart local heuristics-based query answerer when API keys are absent.

8. **Automated Insights & Export**:
   - Generates natural language analysis reports.
   - Exports the analysis as downloadable reports.

---

## Directory Structure

```
ai-business-analyst/
│
├── data/                    # Local storage for raw, processed, and embeddings data
│   ├── raw/
│   ├── processed/
│   └── embeddings/
│
├── notebooks/                # Experimental Jupyter Notebooks
│
├── src/                     # Core Business Logic Package
│   ├── __init__.py
│   ├── ingestion/           # Data ingestion (loaders)
│   ├── profiling/           # Data profiling and quality scoring
│   ├── preprocessing/       # Data cleaning and manipulation
│   ├── eda/                 # Interactive visual layouts and data aggregators
│   ├── insights/            # Automated narrative generators
│   ├── kpi/                 # Automated KPI calculations
│   ├── anomaly_detection/   # Outlier and anomaly engines
│   ├── forecasting/         # Prediction models and historical forecasting
│   ├── rag/                 # Vector stores, retrievers, and LLM orchestration
│   ├── reports/             # HTML report compilers
│   └── utils/               # Configs and auxiliary utilities
│
├── app/                     # Streamlit Frontend Multi-page Application
│   ├── pages/               # Individual functional pages
│   └── main.py              # Main landing and configuration page
│
├── reports/                 # Exported analyst reports
├── screenshots/             # Screenshots of application dashboard
├── tests/                   # Pytest suite
│
├── requirements.txt         # Core dependencies
├── README.md                # System documentation
├── .gitignore               # Git ignored patterns
└── architecture.png         # Project architecture diagram
```

---

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd ai-business-analyst
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your API Keys (optional; the app will fall back to smart local algorithms if missing):
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the Application**:
   ```bash
   streamlit run app/main.py
   ```

6. **Run Unit Tests**:
   ```bash
   pytest
   ```
