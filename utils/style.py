import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        .stApp {
            background: linear-gradient(135deg, #f6f0ff 0%, #eef4ff 45%, #fff3f8 100%);
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
        .card {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(214, 209, 240, 0.75);
            border-radius: 18px;
            padding: 1.15rem 1.15rem 1rem 1.15rem;
            margin-bottom: 1.1rem;
            box-shadow: 0 10px 25px rgba(151, 156, 205, 0.18);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .card:hover {
            transform: scale(1.008);
            box-shadow: 0 12px 28px rgba(159, 167, 222, 0.22);
        }
        .section-title {
            font-size: 1.22rem;
            font-weight: 650;
            margin-bottom: 0.55rem;
            color: #373553;
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
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def end_card() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def explain(text: str) -> None:
    st.markdown(f'<div class="explain-box">{text}</div>', unsafe_allow_html=True)
