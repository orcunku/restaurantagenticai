
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="HostAI | Restaurant Front Desk",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# REMOVE STREAMLIT UI / PADDING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        [data-testid="stHeader"] {
            display: none;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        [data-testid="stStatusWidget"] {
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

        [data-testid="stMain"] {
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

# ---------------------------------------------------------
# EXACT HOSTAI APPLICATION
# ---------------------------------------------------------

HOSTAI_URL = "https://YOUR-PUBLIC-HOSTAI-URL.com"

components.iframe(
    HOSTAI_URL,
    height=1400,
    scrolling=True,
)

