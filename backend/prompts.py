"""
backend/prompts.py
------------------
LangChain prompt templates for MediDrishti AI (xAI Grok).
"""

from langchain.prompts import ChatPromptTemplate, PromptTemplate

# ---------------------------------------------------------------------------
# Plain string prompts (used directly in chatbot.py)
# ---------------------------------------------------------------------------

MEDICAL_ANALYSIS_PROMPT = (
    "You are a clinical medical report assistant powered by xAI Grok. "
    "Extract key lab parameters and analyze them. "
    "For each parameter provide: name, value, normal_range, "
    "status (Normal/High/Low), medical_explanation, and simple_explanation."
)

CHAT_SYSTEM_PROMPT = (
    "You are MediDrishti AI, a medical report assistant powered by xAI Grok. "
    "Answer using the report context. Keep explanations clear, "
    "professional, and patient-friendly."
)

# ---------------------------------------------------------------------------
# LangChain PromptTemplate (available for chain-based usage)
# ---------------------------------------------------------------------------

report_analysis_prompt = PromptTemplate(
    input_variables=["report_context"],
    template=(
        "You are a clinical medical assistant powered by xAI Grok.\n"
        "Analyze the following medical report and extract key parameters.\n\n"
        "Report:\n{report_context}\n\n"
        "For each parameter found, provide:\n"
        "- Parameter name\n"
        "- Value\n"
        "- Normal range\n"
        "- Status (Normal / High / Low)\n"
        "- Medical explanation\n"
        "- Simple explanation for the patient\n"
    ),
)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are MediDrishti AI, a medical report assistant powered by xAI Grok. "
            "Answer using the report context. Be clear, professional, and patient-friendly.",
        ),
        (
            "human",
            "Report context:\n{report_context}\n\n"
            "Previous conversation:\n{chat_history}\n\n"
            "User question:\n{user_input}",
        ),
    ]
)
