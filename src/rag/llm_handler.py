import os

from dotenv import load_dotenv
import google.generativeai as genai


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


class LLMHandler:

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY not found in .env file"
            )

        genai.configure(
            api_key=api_key
        )

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    # ==========================================
    # SUMMARY CONTEXT QUESTION ANSWERING
    # ==========================================

    def ask_question(
        self,
        context,
        question
    ):

        prompt = f"""
You are an expert Business Analyst.

Use ONLY the information provided in the dataset context.

DATASET CONTEXT

{context}

USER QUESTION

{question}

Instructions:

1. Answer the question directly.
2. Explain the business meaning.
3. Provide recommendations if applicable.
4. Be concise and professional.
5. Do not make up information not present in the dataset.

Format:

Direct Answer:
...

Business Interpretation:
...

Recommendation:
...
"""

        try:

            response = self.model.generate_content(
                prompt
            )

            return response.text

        except Exception as e:

            return (
                f"Error generating response: "
                f"{str(e)}"
            )

    # ==========================================
    # RAG QUESTION ANSWERING
    # ==========================================

    def ask_rag_question(
        self,
        retrieved_docs,
        question
    ):

        context = "\n".join(
            retrieved_docs
        )

        prompt = f"""
You are a Senior Business Analyst.

Answer ONLY using the retrieved records below.

RETRIEVED RECORDS

{context}

QUESTION

{question}

Instructions:

1. Give a direct answer.
2. Explain the business meaning.
3. Give business recommendations.
4. Use only the retrieved records.
5. Do not invent information.

Format:

Direct Answer:
...

Business Interpretation:
...

Recommendation:
...
"""

        try:

            response = self.model.generate_content(
                prompt
            )

            return response.text

        except Exception as e:

            return (
                f"Error generating RAG response: "
                f"{str(e)}"
            )

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================

    def summarize_dataset(
        self,
        context
    ):

        prompt = f"""
You are a Senior Business Analyst.

Create an executive summary from the dataset information below.

DATASET CONTEXT

{context}

Provide:

1. Dataset Overview
2. Key Findings
3. Risks
4. Opportunities
5. Recommendations
"""

        try:

            response = self.model.generate_content(
                prompt
            )

            return response.text

        except Exception as e:

            return (
                f"Error generating summary: "
                f"{str(e)}"
            )

    # ==========================================
    # GENERIC ANALYSIS METHOD
    # ==========================================

    def analyze_business_problem(
        self,
        context,
        problem_statement
    ):

        prompt = f"""
You are a Business Strategy Consultant.

Dataset Context:

{context}

Business Problem:

{problem_statement}

Provide:

1. Problem Analysis
2. Root Cause
3. Impact
4. Recommendations
5. Next Actions
"""

        try:

            response = self.model.generate_content(
                prompt
            )

            return response.text

        except Exception as e:

            return (
                f"Error generating analysis: "
                f"{str(e)}"
            )