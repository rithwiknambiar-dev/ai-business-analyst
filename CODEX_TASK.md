\# Project Refactor Request



\## Project Name



AI Business Analyst Platform



\## Current State



The application currently works well for a Superstore-style sales dataset.



Existing features:



\- CSV Upload

\- Data Quality Analysis

\- Data Profiling

\- Exploratory Data Analysis (EDA)

\- Dashboard

\- Business Insights

\- Forecasting

\- Anomaly Detection

\- RAG

\- FAISS Vector Search

\- Gemini AI Chat

\- Report Generation



The project is functional and stable.



\---



\# Problem



Several modules assume specific business columns such as:



\- Sales

\- Profit

\- Region

\- Category

\- Segment



This prevents the system from becoming a true universal AI Data Analyst.



Example:



The current implementation works well for:



Sales Dataset



But should also support:



HR Dataset

Healthcare Dataset

Telecom Dataset

Banking Dataset

Manufacturing Dataset

Any arbitrary CSV



without code changes.



\---



\# Goal



Transform the project from:



AI Business Analyst for Sales Data



into:



Universal AI Data Analyst Platform



The platform must support ANY uploaded CSV.



\---



\# Requirements



\## 1. Universal Schema Intelligence



Create:



src/schema/schema\_analyzer.py



Responsibilities:



Detect:



\- Numeric Columns

\- Categorical Columns

\- Date Columns

\- Text Columns

\- Identifier Columns



Return structured metadata.



Example:



{

&#x20;   "numeric\_columns": \[],

&#x20;   "categorical\_columns": \[],

&#x20;   "date\_columns": \[],

&#x20;   "text\_columns": \[],

&#x20;   "id\_columns": \[]

}



\---



\## 2. Dataset Understanding Layer



Create:



src/schema/dataset\_understanding.py



Responsibilities:



Generate:



\- Dataset Summary

\- Dataset Type Guess

\- Key Metrics

\- Key Dimensions

\- Potential Questions



Examples:



Sales Dataset

HR Dataset

Healthcare Dataset

Financial Dataset

Generic Dataset



\---



\## 3. Universal RAG



Refactor:



src/rag/rag\_engine.py



Current implementation uses hardcoded fields.



Remove assumptions about:



\- Sales

\- Profit

\- Region

\- Category



Instead:



Build documents dynamically from ALL columns.



Example:



for column in df.columns:

&#x20;   document += f"{column}: {value}\\n"



The RAG system must work for any CSV schema.



\---



\## 4. Document Builder



Create:



src/rag/document\_builder.py



Responsibilities:



Generate:



\- Row Documents

\- Dataset Summary Documents

\- Column Summary Documents



These should be embedded into FAISS.



\---



\## 5. Context Builder Refactor



Refactor:



src/rag/context\_builder.py



Context should include:



\- Dataset Summary

\- Schema Summary

\- Column Information

\- Key Insights

\- Retrieved Records



before sending data to Gemini.



\---



\## 6. Insight Generator Refactor



Refactor:



src/insights/insight\_generator.py



Remove sales-specific logic.



Generate dynamic insights based on:



\- Numeric Columns

\- Categorical Columns

\- Correlations

\- Missing Data

\- Outliers

\- Trends



The system should work on any dataset.



\---



\## 7. Dynamic Dashboard



Refactor:



app/pages/dashboard.py



Dashboard should automatically generate:



\- KPI Cards

\- Top Categories

\- Distributions

\- Correlation Charts

\- Trend Charts



based on detected schema.



No hardcoded Sales/Profit assumptions.



\---



\## 8. AI Chat Refactor



Refactor:



src/rag/llm\_handler.py



Prompt should state:



"You are an expert data analyst.



Do not assume sales, profit, region, category, or business-specific fields.



Use only the provided dataset schema, insights, and retrieved context."



\---



\## 9. Forecasting



Forecasting should:



\- Automatically detect date columns

\- Automatically detect candidate metrics

\- Work for any dataset containing dates and numeric values



\---



\## 10. Anomaly Detection



Anomaly detection should:



\- Work on all numeric columns

\- Not assume business-specific fields



\---



\# UI Improvements



Improve Streamlit application.



Pages:



\- Home

\- Dataset Overview

\- Analytics Dashboard

\- Data Quality

\- Forecasting

\- Anomaly Detection

\- AI Insights

\- AI Analyst Chat

\- Executive Reports

\- Dataset Metadata



Requirements:



\- Professional layout

\- Modern design

\- Consistent styling

\- Error handling

\- Loading indicators

\- Empty state handling



\---



\# Important Constraints



DO NOT BREAK EXISTING FUNCTIONALITY.



The application must continue working with:



Superstore Dataset



while also supporting arbitrary CSV files.



\---



\# Deliverables



1\. Detailed migration plan

2\. List of files modified

3\. New files created

4\. Refactored code

5\. Updated tests

6\. Verification checklist



\---



\# First Step



DO NOT MODIFY CODE IMMEDIATELY.



First:



1\. Analyze repository.

2\. Identify all hardcoded assumptions.

3\. Produce migration plan.

4\. Wait for approval.



Only then start implementation.

