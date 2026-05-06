import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        .stApp {
            background: linear-gradient(135deg, #f5eeff 0%, #eaf3ff 50%, #f7f4ff 100%);
            color: #3d3b52;
            font-family: 'Inter', sans-serif;
        }
        .block-container {
            max-width: 1080px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3, h4 {
            color: #2f2c47 !important;
            letter-spacing: 0.2px;
        }
        .hero-text {
            font-size: 1.02rem;
            line-height: 1.62;
            color: #5d5a76;
            margin-bottom: 1rem;
        }
        .edu-card {
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid #dddaf5;
            border-radius: 14px;
            padding: 1rem 1rem 0.9rem 1rem;
            margin: 0.4rem 0 0.9rem 0;
            box-shadow: 0 8px 20px rgba(146, 152, 199, 0.14);
        }
        .explain-box {
            background: #f8f7ff;
            border-left: 4px solid #a7a1df;
            border-radius: 12px;
            padding: 0.8rem 0.9rem;
            margin: 0.5rem 0 0.8rem 0;
        }
        div[data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.76);
            border-right: 1px solid rgba(212, 208, 238, 0.85);
        }
        div[data-testid="stSidebar"] * {
            color: #3f3b5b !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def start_card(title: str) -> None:
    st.markdown(f'<div class="edu-card"><h3 style="margin-top:0.1rem;">{title}</h3></div>', unsafe_allow_html=True)


def end_card() -> None:
    st.divider()


def explain(text: str) -> None:
    st.markdown(f'<div class="explain-box">{text}</div>', unsafe_allow_html=True)


def section_note(title: str, text: str) -> None:
    st.info(f"**{title}:** {text}")
