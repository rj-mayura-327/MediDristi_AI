"""
backend/chatbot.py
------------------
Conversational healthcare assistant using xAI Grok via LangChain.
"""

from .llm import get_llm


class ReportChatAssistant:
    """Chat assistant grounded in the uploaded medical report context."""

    def __init__(self, report_context: str):
        self.report_context = report_context
        self.chat_history: list[tuple[str, str]] = []
        self.llm = get_llm(temperature=0.3)

    def ask(self, user_input: str) -> str:
        """Send a question and get a Groq-powered response."""
        history_text = "\n".join(
            f"{role}: {msg}" for role, msg in self.chat_history
        )

        prompt = (
            "You are MediDrishti AI, a medical report assistant powered by xAI Grok.\n"
            "Answer using the report context below. Be clear, professional, and patient-friendly.\n\n"
            f"Report context:\n{self.report_context}\n\n"
            f"Previous conversation:\n{history_text}\n\n"
            f"User question:\n{user_input}\n\n"
            "Provide an answer that references the report values, explains the medical meaning, "
            "suggests care when appropriate, and is easy for a non-medical person to understand."
        )

        try:
            response = self.llm.invoke(prompt)
            answer = response.content
            self.chat_history.append(("User", user_input))
            self.chat_history.append(("Assistant", answer))
            return answer
        except Exception as e:
            return f"Error processing your question: {str(e)}"
