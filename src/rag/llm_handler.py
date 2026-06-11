import google.generativeai as genai
import openai
import re
from src.utils.config import GEMINI_API_KEY, OPENAI_API_KEY

class LLMHandler:
    """
    Orchestrates sending prompt contexts to LLM APIs.
    Falls back to a local rules-based analytical responder when API keys are absent.
    """
    def __init__(self, provider="mock", api_key=None):
        self.provider = provider.lower()
        self.api_key = api_key
        
        # Initialize API engines
        if self.provider == "gemini" and (self.api_key or GEMINI_API_KEY):
            genai.configure(api_key=self.api_key or GEMINI_API_KEY)
        elif self.provider == "openai" and (self.api_key or OPENAI_API_KEY):
            openai.api_key = self.api_key or OPENAI_API_KEY

    def generate_response(self, query: str, retrieved_contexts: list[dict], fallback_df=None) -> str:
        """
        Generate answer based on retrieved documents and the query.
        """
        context_text = "\n\n".join([f"[Context {i+1}]: {doc['text']}" for i, doc in enumerate(retrieved_contexts)])
        
        system_prompt = (
            "You are an expert AI Business Analyst. Use the provided context to answer the user's business query. "
            "Be precise, data-driven, and format your response in clear markdown. "
            "If the answer cannot be found in the context, tell the user but provide a helpful, generalized estimation based on the context."
        )
        
        user_prompt = f"Contexts:\n{context_text}\n\nQuery: {query}"
        
        # 1. OpenAI Call
        if self.provider == "openai" and (self.api_key or OPENAI_API_KEY):
            try:
                client = openai.OpenAI(api_key=self.api_key or OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2
                )
                return response.choices[0].message.content
            except Exception as e:
                # Fallback on failure
                self.provider = "mock"
                
        # 2. Gemini Call
        if self.provider == "gemini" and (self.api_key or GEMINI_API_KEY):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
                response = model.generate_content(user_prompt)
                return response.text
            except Exception as e:
                # Fallback on failure
                self.provider = "mock"
                
        # 3. Local Analytical Mock Fallback
        return self._generate_analytical_mock(query, retrieved_contexts, fallback_df)

    def _generate_analytical_mock(self, query: str, retrieved_contexts: list[dict], df=None) -> str:
        """
        Smart, rule-based analytical responder for when no LLM API is available.
        Analyzes the dataframe and retrieved chunks to produce highly relevant, mock-AI answers.
        """
        q_lower = query.lower()
        
        # General Greeting
        if any(kw in q_lower for kw in ["hello", "hi", "hey", "who are you"]):
            return (
                "👋 Hello! I am your local **AI Business Analyst**.\n\n"
                "I can answer questions about your dataset, aggregate figures, summarize insights, "
                "or explain forecasting results. Since you are running in offline/local mode, I will answer using "
                "my rule-based analytical engine. \n\n"
                "Try asking questions like:\n"
                "- *What is the total revenue?*\n"
                "- *Show me summary stats.*\n"
                "- *What did you find in the retrieved context?*"
            )
            
        # Parse DataFrame statistics if provided
        summary_stats = ""
        if df is not None and not df.empty:
            num_rows = len(df)
            num_cols = len(df.columns)
            num_cols_list = df.select_dtypes(include=['number']).columns.tolist()
            char_cols_list = df.select_dtypes(exclude=['number']).columns.tolist()
            
            # Match specific column values
            matching_metric = None
            for col in num_cols_list:
                if any(kw in q_lower for kw in [col.lower(), "value", "sales", "revenue", "profit"]):
                    matching_metric = col
                    break
            if not matching_metric and num_cols_list:
                matching_metric = num_cols_list[0]
                
            # Answers relating to totals/sums
            if any(kw in q_lower for kw in ["total", "sum", "accumulated"]):
                if matching_metric:
                    tot = df[matching_metric].sum()
                    return f"📊 **Total Aggregation:**\nBased on your loaded data, the total sum of **{matching_metric}** across all {num_rows:,} records is **{tot:,.2f}**."
                return f"I see you're asking about sums. I found {num_rows} records, but could not determine which numeric column to aggregate."
                
            # Answers relating to average/mean
            if any(kw in q_lower for kw in ["average", "mean", "median"]):
                if matching_metric:
                    avg = df[matching_metric].mean()
                    med = df[matching_metric].median()
                    return (
                        f"📈 **Averages & Medians:**\n"
                        f"For the **{matching_metric}** column:\n"
                        f"- **Average (Mean):** {avg:,.2f}\n"
                        f"- **Median:** {med:,.2f}\n"
                        f"Computed across all {num_rows:,} rows."
                    )
            
            # Schema/Columns question
            if any(kw in q_lower for kw in ["schema", "column", "structure", "data type"]):
                cols_str = "\n".join([f"- **{col}** ({df[col].dtype})" for col in df.columns])
                return (
                    f"🗂️ **Dataset Schema Summary:**\n"
                    f"The dataset contains **{num_rows:,} rows** and **{num_cols} columns**:\n\n"
                    f"{cols_str}"
                )
                
            summary_stats = f"The dataset has {num_rows:,} rows. "
            if matching_metric:
                summary_stats += f"The primary numerical metric '{matching_metric}' averages {df[matching_metric].mean():,.2f} (Sum: {df[matching_metric].sum():,.2f})."
        
        # Fallback response using retrieved contexts
        context_snippets = []
        for i, ctx in enumerate(retrieved_contexts[:2]):
            text = ctx["text"]
            # Shorten if too long
            if len(text) > 300:
                text = text[:300] + "..."
            context_snippets.append(f"> {text.replace(chr(10), '  ')}")
            
        snippets_block = "\n\n".join(context_snippets)
        
        return (
            f"🤖 **Local Analyst Response:**\n\n"
            f"To provide a full generative response, please set a `GEMINI_API_KEY` or `OPENAI_API_KEY` in your `.env` file or the page sidebar.\n\n"
            f"However, using keyword matching and semantic retrieval, here is what I found in the records regarding your query *\"{query}\"*:\n\n"
            f"{snippets_block}\n\n"
            f"**Context stats summary:** {summary_stats or 'No additional numeric data found.'}"
        )
