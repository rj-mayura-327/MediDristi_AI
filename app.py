import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from datetime import datetime

import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MediDrishti AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)

# --- Load env ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    st.error(f"Failed to load .env: {e}")

# --- API key check ---
_key = os.getenv("XAI_API_KEY", "").strip()
_placeholders = {
    "", "your_xai_api_key_here", "xai-put-your-real-key-here",
    "PASTE_YOUR_REAL_XAI_KEY_HERE", "your-key-here",
}
if _key in _placeholders:
    st.error("⚠️ API key not set in your .env file.")
    st.markdown("""
    **To fix:** Open `.env` and set your Groq key:
    ```
    XAI_API_KEY=gsk_yourrealgroqkeyhere
    ```
    Get a free key at: https://console.groq.com/
    """)
    st.stop()

# --- Backend imports ---
try:
    from backend.llm import get_llm
    from backend.analyzer import analyze_parameters, generate_health_summary
    from backend.chatbot import ReportChatAssistant
    from backend.diet_engine import generate_diet_recommendations
    from backend.precaution_engine import generate_precaution_plan
    from backend.report_parser import (
        ALLOWED_EXTENSIONS, extract_report_text,
        parse_medical_parameters, validate_report_file,
    )
    from frontend.ui import (
        load_styles, render_sidebar_brand, render_hero,
        render_page_header, render_metric_card, render_parameter_card,
        render_diet_section, render_precaution_section,
        render_chat_message, render_report_status,
        render_list, render_section_label, render_ai_badge,
    )
except Exception as e:
    st.error(f"Import error: {e}")
    st.exception(e)
    st.stop()

# --- Load styles ---
load_styles()

# --- Session state ---
def initialize_session() -> None:
    keys = [
        "uploaded_file", "report_text", "parameters",
        "analysis_results", "health_summary", "diet_recommendations",
        "precaution_plan", "chat_assistant", "summary_text",
        "chat_history",
    ]
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = None
    if st.session_state.chat_history is None:
        st.session_state.chat_history = []

initialize_session()


def build_report_summary() -> str:
    lines = [
        "MediDrishti AI — Health Report Summary",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    if st.session_state.health_summary:
        h = st.session_state.health_summary
        lines += [
            f"Health Score : {h['health_score']}",
            f"Risk Level   : {h['risk_level']}", "",
            "Key Findings:",
            *[f"  - {i}" for i in h["key_findings"]], "",
            "Positive Findings:",
            *[f"  - {i}" for i in h["positive_findings"]], "",
            "Areas of Concern:",
            *[f"  - {i}" for i in h["areas_of_concern"]], "",
        ]
    if st.session_state.analysis_results:
        lines.append("Detailed Parameters:")
        for item in st.session_state.analysis_results:
            lines.append(
                f"  {item['parameter']}: {item['value']} "
                f"[{item['status']}] — {item['simple_explanation']}"
            )
    return "\n".join(lines)


# ================================================================
# SIDEBAR
# ================================================================
render_sidebar_brand()

st.sidebar.markdown("---")

PAGES = {
    "📄 Upload Report":       "upload",
    "📊 Analysis Dashboard":  "dashboard",
    "🥗 Diet Recommendations": "diet",
    "⚠️ Precautions":         "precautions",
    "💬 Ask MediDrishti":     "chat",
    "⬇️ Download Summary":    "download",
}

page_label = st.sidebar.radio(
    "Navigate",
    list(PAGES.keys()),
    label_visibility="collapsed",
)
page = PAGES[page_label]

# Upload status in sidebar
st.sidebar.markdown("---")
if st.session_state.uploaded_file:
    st.sidebar.markdown(
        f"""
        <div style="background:#CCFBF1; border:1px solid #14B8A6; border-radius:8px;
                    padding:0.6rem 0.8rem; font-size:0.82rem; color:#0F766E;">
            <strong>📋 Report loaded:</strong><br>{st.session_state.uploaded_file}
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.sidebar.markdown(
        """
        <div style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:8px;
                    padding:0.6rem 0.8rem; font-size:0.82rem; color:#6B7280;">
            No report uploaded yet.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ================================================================
# PAGE 1 — UPLOAD REPORT
# ================================================================
if page == "upload":
    render_hero()

    render_page_header("Upload Medical Report", "Upload your PDF or image report for instant AI analysis.", "📄")

    st.markdown(
        """
        <div style="background:#FAFAFA; border:1px solid #E5E7EB; border-radius:12px;
                    padding:1.2rem 1.5rem; margin-bottom:1.2rem;">
            <div style="display:flex; gap:1rem; flex-wrap:wrap;">
                <span style="font-size:0.85rem; color:#6B7280;">
                    📑 <strong>PDF</strong> blood reports
                </span>
                <span style="font-size:0.85rem; color:#6B7280;">
                    🖼️ <strong>JPG / PNG</strong> scanned reports
                </span>
                <span style="font-size:0.85rem; color:#6B7280;">
                    🔒 Processed locally — your data stays private
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Drop your medical report here",
        type=list(ALLOWED_EXTENSIONS),
        accept_multiple_files=False,
        label_visibility="collapsed",
    )

    col_a, col_b = st.columns([1, 5])
    with col_a:
        analyze_clicked = st.button("🔍 Analyze Report", use_container_width=True)
    with col_b:
        if st.button("🗑️ Clear Report", use_container_width=False):
            for k in ["uploaded_file", "report_text", "parameters", "analysis_results",
                      "health_summary", "diet_recommendations", "precaution_plan",
                      "chat_assistant", "summary_text", "chat_history"]:
                st.session_state[k] = None
            st.session_state.chat_history = []
            st.rerun()

    if uploaded_file and analyze_clicked:
        if not validate_report_file(uploaded_file.name):
            st.error("Please upload a valid PDF, JPG, or PNG file.")
        else:
            try:
                with st.spinner("🔬 Analyzing your report with AI..."):
                    raw_text = extract_report_text(uploaded_file)
                    if not raw_text:
                        st.warning("No text could be extracted from this file.")
                        st.stop()
                    parsed_data       = parse_medical_parameters(raw_text)
                    analysis_results  = analyze_parameters(parsed_data)
                    summary           = generate_health_summary(analysis_results)
                    diet_recs         = generate_diet_recommendations(analysis_results)
                    precaution_plan   = generate_precaution_plan(analysis_results)
                    assistant         = ReportChatAssistant(report_context=raw_text)

                st.session_state.update({
                    "uploaded_file":       uploaded_file.name,
                    "report_text":         raw_text,
                    "parameters":          parsed_data,
                    "analysis_results":    analysis_results,
                    "health_summary":      summary,
                    "diet_recommendations": diet_recs,
                    "precaution_plan":     precaution_plan,
                    "chat_assistant":      assistant,
                    "chat_history":        [],
                })
                st.session_state.summary_text = build_report_summary()
                render_report_status(f"✅ Report '{uploaded_file.name}' analyzed successfully! Navigate using the sidebar.")
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.exception(e)

    elif uploaded_file and not analyze_clicked:
        st.info(f"📋 **{uploaded_file.name}** ready — click **Analyze Report** to begin.")


# ================================================================
# PAGE 2 — ANALYSIS DASHBOARD
# ================================================================
elif page == "dashboard":
    render_page_header("Analysis Dashboard", "Your personalized health overview.", "📊")

    if not st.session_state.analysis_results:
        st.info("📄 Please upload and analyze a medical report first.")
        st.stop()

    h = st.session_state.health_summary
    render_ai_badge("AI Health Summary")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card("🎯 Health Score", h["health_score"], "Overall AI-computed score")
    with c2:
        render_metric_card("⚠️ Risk Level", h["risk_level"], "Based on abnormal parameters")
    with c3:
        render_metric_card("🔍 Findings", str(len(h["key_findings"])), "Parameters needing attention")

    st.markdown("<br>", unsafe_allow_html=True)
    render_section_label("PARAMETER ANALYSIS")

    for item in st.session_state.analysis_results:
        render_parameter_card(item)

    st.markdown("<br>", unsafe_allow_html=True)
    c4, c5 = st.columns(2)
    with c4:
        render_list("✅ Positive Findings", h["positive_findings"])
    with c5:
        render_list("⚠️ Areas of Concern", h["areas_of_concern"])


# ================================================================
# PAGE 3 — DIET RECOMMENDATIONS
# ================================================================
elif page == "diet":
    render_page_header("Diet Recommendations", "Personalized nutrition guidance based on your report.", "🥗")

    if not st.session_state.diet_recommendations:
        st.info("📄 Please upload and analyze a medical report first.")
        st.stop()

    render_ai_badge("AI Personalized")
    st.markdown("<br>", unsafe_allow_html=True)

    diet = st.session_state.diet_recommendations
    c1, c2 = st.columns(2)
    with c1:
        render_diet_section("Foods to Include", "✅", diet["include"], "#22C55E")
        st.markdown("<br>", unsafe_allow_html=True)
        render_diet_section("Hydration Tips", "💧", diet["hydration"], "#3B82F6")
    with c2:
        render_diet_section("Foods to Avoid", "❌", diet["limit"], "#EF4444")
        st.markdown("<br>", unsafe_allow_html=True)
        render_diet_section("Nutritional Suggestions", "🥗", diet["nutrition"], "#F59E0B")


# ================================================================
# PAGE 4 — PRECAUTIONS
# ================================================================
elif page == "precautions":
    render_page_header("Health Precautions", "Daily habits and doctor consultation guidance.", "⚠️")

    if not st.session_state.precaution_plan:
        st.info("📄 Please upload and analyze a medical report first.")
        st.stop()

    plan = st.session_state.precaution_plan
    c1, c2 = st.columns(2)
    with c1:
        with st.expander("🌅 Daily Precautions", expanded=True):
            render_precaution_section("Daily Precautions", "🌅", plan["daily_precautions"])
        with st.expander("🏃 Lifestyle Changes", expanded=True):
            render_precaution_section("Lifestyle Changes", "🏃", plan["lifestyle_changes"])
    with c2:
        with st.expander("📊 Monitoring Recommendations", expanded=True):
            render_precaution_section("Monitoring", "📊", plan["monitoring_recommendations"])
        with st.expander("🏥 Doctor Consultation", expanded=True):
            render_precaution_section("Doctor Consultation", "🏥", plan["medical_follow_up"])


# ================================================================
# PAGE 5 — CHAT
# ================================================================
elif page == "chat":
    render_page_header("Ask MediDrishti", "Chat with AI about your health report.", "💬")
    render_ai_badge("Powered by Groq AI")
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.chat_assistant:
        st.info("📄 Please upload and analyze a medical report first.")
        st.stop()

    # Render chat history
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            render_chat_message(msg["role"], msg["content"])
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div style="background:#F0FDF4; border:1px solid #22C55E; border-radius:12px;
                        padding:1.2rem 1.5rem; margin-bottom:1rem;">
                <strong>💬 Start a conversation!</strong><br>
                <span style="color:#6B7280; font-size:0.9rem;">Try asking:</span>
                <div style="margin-top:0.5rem; display:flex; flex-wrap:wrap; gap:0.4rem;">
                    <span style="background:white; border:1px solid #E5E7EB; border-radius:999px;
                                 padding:0.2rem 0.7rem; font-size:0.82rem; color:#374151;">
                        What does my cholesterol level mean?
                    </span>
                    <span style="background:white; border:1px solid #E5E7EB; border-radius:999px;
                                 padding:0.2rem 0.7rem; font-size:0.82rem; color:#374151;">
                        Why is my glucose high?
                    </span>
                    <span style="background:white; border:1px solid #E5E7EB; border-radius:999px;
                                 padding:0.2rem 0.7rem; font-size:0.82rem; color:#374151;">
                        What foods should I avoid?
                    </span>
                    <span style="background:white; border:1px solid #E5E7EB; border-radius:999px;
                                 padding:0.2rem 0.7rem; font-size:0.82rem; color:#374151;">
                        Explain my report simply
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Chat input
    with st.container():
        user_input = st.text_area(
            "Your message",
            placeholder="Ask anything about your health report...",
            height=90,
            label_visibility="collapsed",
        )
        col_send, col_clear = st.columns([1, 5])
        with col_send:
            send = st.button("Send 📤", use_container_width=True)
        with col_clear:
            if st.button("Clear Chat 🗑️"):
                st.session_state.chat_history = []
                st.session_state.chat_assistant.chat_history = []
                st.rerun()

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        with st.spinner("MediDrishti is thinking..."):
            try:
                response = st.session_state.chat_assistant.ask(user_input.strip())
            except Exception as e:
                response = f"Sorry, I encountered an error: {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()


# ================================================================
# PAGE 6 — DOWNLOAD
# ================================================================
elif page == "download":
    render_page_header("Download Summary", "Save your complete health report summary.", "⬇️")

    if not st.session_state.summary_text:
        st.info("📄 Please upload and analyze a medical report first.")
        st.stop()

    st.markdown(
        """
        <div class="md-card fade-up">
            <div style="font-size:1rem; font-weight:600; color:#1F2937; margin-bottom:0.4rem;">
                📋 Your health summary is ready
            </div>
            <div style="font-size:0.88rem; color:#6B7280;">
                Download a complete text summary including health score, parameter analysis,
                diet recommendations, and precautions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="⬇️ Download Health Summary (.txt)",
        data=st.session_state.summary_text,
        file_name=f"medidristi_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=False,
    )
