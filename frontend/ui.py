import streamlit as st
from datetime import datetime


def load_styles() -> None:
    try:
        with open("assets/style.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def render_sidebar_brand() -> None:
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <span class="brand-icon">🏥</span>
            <span class="brand-name">MediDrishti AI</span>
            <span class="brand-tagline">Powered by Groq AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str = "", icon: str = "") -> None:
    st.markdown(
        f"""
        <div class="page-header fade-up">
            <h1>{icon + " " if icon else ""}{title}</h1>
            {"<p>" + subtitle + "</p>" if subtitle else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-section fade-up">
            <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.75rem;">
                <span style="font-size:3rem;">🏥</span>
                <div>
                    <div class="hero-title">MediDrishti <span>AI</span></div>
                    <div class="hero-subtitle">Understand your health report in simple language.</div>
                </div>
            </div>
            <div class="hero-features">
                <span class="hero-feature-pill">✓ Easy-to-read explanations</span>
                <span class="hero-feature-pill">✓ Personalized diet recommendations</span>
                <span class="hero-feature-pill">✓ Health precautions</span>
                <span class="hero-feature-pill">✓ AI-powered assistance</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, description: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card fade-up">
            <div class="metric-title">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_parameter_card(item: dict) -> None:
    status = item["status"].lower()
    badge_class = "normal" if status == "normal" else ("high" if status == "high" else "low")
    status_label = (
        "✅ Healthy" if status == "normal"
        else ("🔴 Critical" if status == "high" else "🟡 Attention Needed")
    )
    st.markdown(
        f"""
        <div class="param-card {badge_class} fade-up">
            <div class="param-header">
                <span class="param-name">🔬 {item['parameter']}</span>
                <span class="status-badge {badge_class}">{status_label}</span>
            </div>
            <div style="display:flex; gap:1.5rem; margin-bottom:0.5rem; flex-wrap:wrap;">
                <span style="font-size:0.85rem; color:#6B7280;">
                    <strong style="color:#1F2937;">Value:</strong> {item['value']}
                </span>
                <span style="font-size:0.85rem; color:#6B7280;">
                    <strong style="color:#1F2937;">Normal Range:</strong> {item['normal_range']}
                </span>
            </div>
            <div class="param-explanation">{item['simple_explanation']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_diet_section(title: str, icon: str, items: list, color: str = "#14B8A6") -> None:
    items_html = "".join(
        f'<div class="diet-item"><span style="color:{color}; font-size:1rem;">•</span>{item}</div>'
        for item in items
    )
    st.markdown(
        f"""
        <div class="diet-card fade-up">
            <div class="diet-card-title" style="color:{color};">{icon} {title}</div>
            {items_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_precaution_section(title: str, icon: str, items: list) -> None:
    items_html = "".join(
        f'<div class="precaution-item"><div class="precaution-dot"></div><span>{item}</span></div>'
        for item in items
    )
    st.markdown(
        f"""
        <div class="precaution-card fade-up">
            <div style="font-size:1rem; font-weight:700; color:#1F2937; margin-bottom:0.75rem;">
                {icon} {title}
            </div>
            {items_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_message(role: str, message: str) -> None:
    is_user = role == "user"
    bubble_class = "user-bubble" if is_user else "ai-bubble"
    msg_class = "user" if is_user else ""
    avatar = "👤" if is_user else "🤖"
    avatar_class = "user-av" if is_user else "ai-av"
    time_str = datetime.now().strftime("%H:%M")
    st.markdown(
        f"""
        <div class="chat-message {msg_class}">
            <div class="chat-avatar {avatar_class}">{avatar}</div>
            <div>
                <div class="chat-bubble {bubble_class}">{message}</div>
                <div class="chat-time">{time_str}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_report_status(text: str) -> None:
    st.success(text)


def render_list(title: str, items: list) -> None:
    if items:
        items_html = "".join(
            f'<div class="precaution-item"><div class="precaution-dot"></div><span>{i}</span></div>'
            for i in items
        )
        st.markdown(
            f"""
            <div class="precaution-card">
                <div style="font-weight:700; color:#1F2937; margin-bottom:0.6rem;">{title}</div>
                {items_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_section(title: str) -> None:
    st.subheader(title)


def render_section_label(text: str) -> None:
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def render_ai_badge(text: str = "AI Generated") -> None:
    st.markdown(f'<span class="ai-badge">✨ {text}</span>', unsafe_allow_html=True)
