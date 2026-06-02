import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Fix: OMP duplicate libiomp5md.dll error
from datetime import datetime

import streamlit as st

# --- PAGE CONFIG must be the very first Streamlit call ---
st.set_page_config(
    page_title="MediDrishti AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)

# --- Load env variables BEFORE anything else ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    st.error(f"Failed to load .env: {e}")

# --- Check API key IMMEDIATELY - visible error before CSS hides anything ---
_xai_api_key = os.getenv("XAI_API_KEY", "").strip()
_placeholders = {"your_xai_api_key_here", "xai-put-your-real-key-here", "", "your-key-here"}
if _xai_api_key in _placeholders:
    st.error("⚠️ XAI_API_KEY not set in your .env file.")
    st.markdown("""
    **To fix this:**
    1. Open the file `.env` in the project folder
    2. Replace the placeholder with your real xAI Grok key
    3. Get your key at: https://console.x.ai/
    4. Save `.env` and restart: `streamlit run app.py`

    Example `.env` content:
    ```
    XAI_API_KEY=xai-yourrealkeyhere
    ```
    """)
    st.stop()

# --- Hide all Streamlit chrome (only runs when API key is valid) ---
st.markdown(
    """
    <style>
        header[data-testid="stHeader"]  { display: none !important; }
        footer                          { display: none !important; }
        [data-testid="stStatusWidget"]  { display: none !important; }
        [data-testid="stDeployButton"]  { display: none !important; }
        #MainMenu                       { display: none !important; }
        .block-container                { padding-top: 1.5rem !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Backend imports wrapped so errors are visible ---
try:
    from backend.llm import get_llm
    from backend.analyzer import analyze_parameters, generate_health_summary
    from backend.chatbot import ReportChatAssistant
    from backend.diet_engine import generate_diet_recommendations
    from backend.precaution_engine import generate_precaution_plan
    from backend.report_parser import (
        ALLOWED_EXTENSIONS,
        extract_report_text,
        parse_medical_parameters,
        validate_report_file,
    )
    from frontend.ui import (
        load_styles,
        render_list,
        render_metric_card,
        render_page_header,
        render_report_status,
    )
except Exception as e:
    st.error(f"Import error: {e}")
    st.exception(e)
    st.stop()


def initialize_session() -> None:
    keys = [
        "uploaded_file", "report_text", "parameters",
        "analysis_results", "health_summary", "diet_recommendations",
        "precaution_plan", "chat_assistant", "summary_text",
    ]
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = None


def build_report_summary() -> str:
    lines = [
        "MediDrishti AI Report Summary",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    if st.session_state.health_summary:
        h = st.session_state.health_summary
        lines += [
            f"Health Score: {h['health_score']}",
            f"Risk Level: {h['risk_level']}", "",
            "Key Findings:",
            *[f"- {i}" for i in h["key_findings"]], "",
            "Positive Findings:",
            *[f"- {i}" for i in h["positive_findings"]], "",
            "Areas of Concern:",
            *[f"- {i}" for i in h["areas_of_concern"]], "",
        ]
    if st.session_state.analysis_results:
        lines.append("Detailed Parameter Summary:")
        for item in st.session_state.analysis_results:
            lines.append(
                f"- {item['parameter']}: {item['value']} ({item['status']}). {item['simple_explanation']}"
            )
    return "\n".join(lines)


def upload_page() -> None:
    render_page_header("MediDrishti AI", "AI-powered medical report analysis for better health decisions.")
    st.markdown("Upload a PDF or image report and let MediDrishti extract insights instantly.")

    uploaded_file = st.file_uploader(
        "Upload your medical report",
        type=list(ALLOWED_EXTENSIONS),
        accept_multiple_files=False,
    )

    if uploaded_file is not None:
        if not validate_report_file(uploaded_file.name):
            st.error("Please upload a valid PDF or image file.")
            return
        try:
            with st.spinner("Analyzing report..."):
                raw_text = extract_report_text(uploaded_file)
                if not raw_text:
                    st.warning("File uploaded but no text could be extracted.")
                    return
                parsed_data = parse_medical_parameters(raw_text)
                analysis_results = analyze_parameters(parsed_data)
                summary = generate_health_summary(analysis_results)
                diet_recommendations = generate_diet_recommendations(analysis_results)
                precaution_plan = generate_precaution_plan(analysis_results)
                assistant = ReportChatAssistant(report_context=raw_text)

            st.session_state.uploaded_file = uploaded_file.name
            st.session_state.report_text = raw_text
            st.session_state.parameters = parsed_data
            st.session_state.analysis_results = analysis_results
            st.session_state.health_summary = summary
            st.session_state.diet_recommendations = diet_recommendations
            st.session_state.precaution_plan = precaution_plan
            st.session_state.chat_assistant = assistant
            st.session_state.summary_text = build_report_summary()
            render_report_status("Report uploaded and analyzed successfully!")
        except Exception as e:
            st.error(f"Upload failed: {e}")
            st.exception(e)


def dashboard_page() -> None:
    render_page_header("Analysis Dashboard")
    if not st.session_state.analysis_results:
        st.info("Upload a medical report first to view your dashboard.")
        return

    health = st.session_state.health_summary
    st.markdown("### Health Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card("Health Score", health["health_score"], "AI score based on report values.")
    with col2:
        render_metric_card("Risk Level", health["risk_level"], "Current risk estimate.")
    with col3:
        render_metric_card("Findings", str(len(health["key_findings"])), "Note-worthy items detected.")

    with st.expander("Parameter Insights"):
        for item in st.session_state.analysis_results:
            st.markdown(f"#### {item['parameter']}")
            st.write(f"**Value:** {item['value']}")
            st.write(f"**Range:** {item['normal_range']}")
            st.write(f"**Status:** {item['status']}")
            st.write(f"**Medical Explanation:** {item['medical_explanation']}")
            st.write(f"**Simple Explanation:** {item['simple_explanation']}")
            st.divider()

    render_list("Positive Findings", health["positive_findings"])
    render_list("Areas of Concern", health["areas_of_concern"])


def diet_page() -> None:
    render_page_header("Diet Recommendations")
    if not st.session_state.diet_recommendations:
        st.info("Upload a report to unlock personalized diet guidance.")
        return

    diet = st.session_state.diet_recommendations
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ Foods to Include")
        for item in diet["include"]:
            st.write(f"• {item}")
        st.markdown("### 💧 Hydration")
        for item in diet["hydration"]:
            st.write(f"• {item}")
    with col2:
        st.markdown("### ❌ Foods to Limit")
        for item in diet["limit"]:
            st.write(f"• {item}")
        st.markdown("### 🥗 Nutritional Suggestions")
        for item in diet["nutrition"]:
            st.write(f"• {item}")


def precautions_page() -> None:
    render_page_header("Health Precautions")
    if not st.session_state.precaution_plan:
        st.info("Upload a report first to generate precautions.")
        return

    plan = st.session_state.precaution_plan
    col1, col2 = st.columns(2)
    with col1:
        render_list("Daily Precautions", plan["daily_precautions"])
        render_list("Lifestyle Changes", plan["lifestyle_changes"])
    with col2:
        render_list("Monitoring Recommendations", plan["monitoring_recommendations"])
        render_list("Medical Follow-Up Suggestions", plan["medical_follow_up"])


def chat_page() -> None:
    render_page_header("Chat With Report")
    if not st.session_state.chat_assistant:
        st.info("Upload a report to start a conversation with the assistant.")
        return

    user_input = st.text_area("Ask a question about your report", height=120)
    if st.button("Send") and user_input.strip():
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat_assistant.ask(user_input)
                st.markdown("### Assistant Response")
                st.write(response)
            except Exception as e:
                st.error(f"Chat failed: {e}")
                st.exception(e)


def download_page() -> None:
    render_page_header("Report Summary Download")
    if not st.session_state.summary_text:
        st.info("Upload a medical report to generate a downloadable summary.")
        return

    st.download_button(
        label="⬇️ Download Report Summary",
        data=st.session_state.summary_text,
        file_name="medidristi_report_summary.txt",
        mime="text/plain",
    )


# --- Load styles and session ---
load_styles()
initialize_session()

# --- Sidebar navigation ---
page = st.sidebar.selectbox(
    "Navigation",
    [
        "Upload Report",
        "Analysis Dashboard",
        "Diet Recommendations",
        "Precautions",
        "Chat Assistant",
        "Report Summary Download",
    ],
)

if page == "Upload Report":
    upload_page()
elif page == "Analysis Dashboard":
    dashboard_page()
elif page == "Diet Recommendations":
    diet_page()
elif page == "Precautions":
    precautions_page()
elif page == "Chat Assistant":
    chat_page()
elif page == "Report Summary Download":
    download_page()
