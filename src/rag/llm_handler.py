import os

from dotenv import load_dotenv
import google.generativeai as genai


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
    # QUESTION TYPE DETECTION
    # ==========================================

    def get_question_type(
        self,
        question
    ):

        question = question.lower()

        analysis_keywords = [

            "why",
            "recommend",
            "recommendation",
            "improve",
            "strategy",
            "insight",
            "analyze",
            "analysis",
            "root cause",
            "opportunity",
            "risk",
            "forecast"
        ]

        for keyword in analysis_keywords:

            if keyword in question:

                return "analysis"

        return "fact"

    # ==========================================
    # SUMMARY CONTEXT QA
    # ==========================================

    def ask_question(
        self,
        context,
        question
    ):

        question_type = (
            self.get_question_type(
                question
            )
        )

        if question_type == "fact":

            prompt = f"""
You are an AI Data Analyst.

Answer ONLY using the dataset context.

DATASET CONTEXT

{context}

QUESTION

{question}

Rules:

1. Give a short direct answer.
2. If information is not available, clearly say so.
3. Do not provide recommendations.
4. Do not provide business interpretation.
5. Do not invent information.
"""

        else:

            prompt = f"""
You are a Senior Business Analyst.

Answer ONLY using the dataset context.

DATASET CONTEXT

{context}

QUESTION

{question}

Rules:

1. Answer the question.
2. Explain the business meaning.
3. Give recommendations if relevant.
4. Do not invent information.
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
    # RAG QA
    # ==========================================

    def ask_rag_question(
        self,
        retrieved_docs,
        question
    ):

        context = "\n".join(
            retrieved_docs
        )

        question_type = (
            self.get_question_type(
                question
            )
        )

        if question_type == "fact":

            prompt = f"""
You are an AI Data Analyst.

Use ONLY the retrieved records.

RETRIEVED RECORDS

{context}

QUESTION

{question}

Rules:

1. Answer directly.
2. Be concise.
3. If the requested information does not exist, say:
   "This information is not available in the dataset."
4. Never guess.
5. Never invent names, values or columns.
6. Do not provide recommendations.
7. Do not provide business interpretation.

Examples:

Question:
How many employees are in Sales?

Answer:
25 employees are in the Sales department.

Question:
List employee names.

Answer:
This information is not available in the dataset because no employee name field exists.
"""

        else:

            prompt = f"""
You are a Senior Business Analyst.

Use ONLY the retrieved records.

RETRIEVED RECORDS

{context}

QUESTION

{question}

Rules:

1. Answer the question.
2. Explain the business meaning.
3. Give recommendations if relevant.
4. Use only the retrieved records.
5. If information is unavailable, clearly state it.
6. Do not invent information.
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

Create an executive summary.

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
    # BUSINESS ANALYSIS
    # ==========================================

    def analyze_business_problem(
        self,
        context,
        problem_statement
    ):

        prompt = f"""
You are a Business Strategy Consultant.

DATASET CONTEXT

{context}

BUSINESS PROBLEM

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