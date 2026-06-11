import os

from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()


class LLMHandler:

    def __init__(self):

        # Get API key from .env
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file"
            )

        # Configure Gemini
        genai.configure(
            api_key=api_key
        )

        # Initialize model
        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def ask_question(
        self,
        context,
        question
    ):

        prompt = f"""
You are an expert Business Analyst.

Use ONLY the information provided in the dataset context.

DATASET CONTEXT
=============================

{context}

=============================

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

    def summarize_dataset(
        self,
        context
    ):

        prompt = f"""
You are a senior Business Analyst.

Create an executive summary for the dataset.

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