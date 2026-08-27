import streamlit as st
from ui.navbar import render_navbar
from ui.home import render_home
from ui.analyzer_page import render_analyzer

st.set_page_config(page_title="Variant Analyzer", page_icon="🧬", layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-left: 3rem;
            padding-right: 3rem;
            max-width: 100%;
        }
        div[data-testid="stHorizontalBlock"] {
            align-items: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

render_navbar()

if st.session_state.page == "home":
    render_home()
else:
    render_analyzer()