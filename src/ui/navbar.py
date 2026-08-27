import streamlit as st
from i18n import t


def _set_page(page):
    st.session_state.page = page


def render_navbar():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "lang" not in st.session_state:
        st.session_state.lang = "en"

    st.markdown(
        """
        <style>
            div[data-testid="stHorizontalBlock"] {
                align-items: center !important;
            }
            div[data-testid="stHorizontalBlock"] h3 {
                margin: 0 !important;
                padding: 0 !important;
            }
            div.stButton > button {
                border: none !important;
                box-shadow: none !important;
                font-size: 1.15rem !important;
                font-weight: 600 !important;
                padding: 0.5rem 1.2rem !important;
                background-color: transparent !important;
                color: #111827 !important;
            }
            div.stButton > button:hover {
                background-color: #F3F4F6 !important;
                color: #111827 !important;
            }
            div.stButton > button[kind="primary"] {
                background-color: #EF4444 !important;
                color: white !important;
            }
            div.stButton > button[kind="primary"]:hover {
                background-color: #DC2626 !important;
                color: white !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col_title, _, col_home, col_analyzer, _, col_lang = st.columns(
        [2, 2, 1, 1, 2, 1]
    )

    with col_title:
        st.markdown("### 🧬 Variant Analyzer")

    with col_home:
        st.button(
            t("nav_home"),
            on_click=_set_page,
            args=("home",),
            key="btn_home",
            type="primary" if st.session_state.page == "home" else "secondary",
            width="stretch",
        )

    with col_analyzer:
        st.button(
            t("nav_analyzer"),
            on_click=_set_page,
            args=("analyzer",),
            key="btn_analyzer",
            type="primary" if st.session_state.page == "analyzer" else "secondary",
            width="stretch",
        )

    with col_lang:
        st.segmented_control(
            "lang",
            options=["en", "ro"],
            format_func=lambda k: k.upper(),
            key="lang",
            label_visibility="collapsed",
        )

    st.divider()