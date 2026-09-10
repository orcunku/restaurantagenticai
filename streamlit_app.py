import os
import streamlit as st
import streamlit.components.v1 as components
from build_template import compile_standalone_html

# 1. Force Streamlit to use maximum screen space
st.set_page_config(
    page_title="European AI Front Desk",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS overrides to remove default Streamlit gaps and margins
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding: 0rem !important;
            margin: 0rem !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Load or build the inlined HTML template
@st.cache_data
def get_compiled_html():
    try:
        return compile_standalone_html()
    except Exception as e:
        st.error(f"Error compiling template: {e}")
        return "<h1>Error loading template files.</h1>"

html_content = get_compiled_html()

# 4. Render identical HTML UI via component iframe
components.html(html_content, height=1000, scrolling=True)