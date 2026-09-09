import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="HostAI | Restaurant Front Desk",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        [data-testid="stHeader"] {
            display: none;
        }

        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }

        [data-testid="stAppViewContainer"] {
            padding: 0 !important;
            margin: 0 !important;
        }

        iframe {
            border: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

HOSTAI_URL = "https://zany-engine-wrpvvjwq75wq2gv9-8001.app.github.dev/"

components.iframe(
    HOSTAI_URL,
    height=1600,
    scrolling=True,
)

