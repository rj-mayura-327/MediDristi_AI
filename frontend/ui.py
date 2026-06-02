import streamlit as st


def load_styles() -> None:
    try:
        with open("assets/style.css", "r", encoding="utf-8") as style:
            st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def render_page_header(title: str, subtitle: str = "") -> None:
    st.title(title)
    if subtitle:
        st.write(subtitle)


def render_metric_card(label: str, value: str, description: str = "") -> None:
    st.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-title'>{label}</div>
            <div class='metric-value'>{value}</div>
            <div class='metric-description'>{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_report_status(status_text: str) -> None:
    st.success(status_text)


def render_section(title: str) -> None:
    st.subheader(title)


def render_list(title: str, items: list) -> None:
    if items:
        st.markdown(f"**{title}**")
        for item in items:
            st.write(f"• {item}")
    else:
        st.write(f"No {title.lower()} available.")
