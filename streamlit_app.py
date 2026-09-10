import streamlit as st
import httpx
import os

st.set_page_config(page_title="European AI Front Desk", page_icon="🍽️", layout="wide")

# Header section
st.title("🍽️ European AI Front Desk for Restaurants")
st.caption("Ihr digitaler Gastgeber — 24/7 AI Receptionist Demo")

# Sidebar settings
st.sidebar.header("Configuration")
restaurant_slug = st.sidebar.selectbox("Select Demo Restaurant", ["demo-bistro", "vienna-fine-dining", "tyrol-alpine-inn"])
api_base_url = st.sidebar.text_input("Backend API Base URL", os.getenv("PUBLIC_BASE_URL", "http://localhost:8000"))

st.sidebar.markdown("---")
st.sidebar.subheader("Dashboard Overview")
st.sidebar.metric(label="Est. Monthly ROI", value="€1,250")
st.sidebar.metric(label="Calls Handled (30d)", value="342")
st.sidebar.metric(label="Reservations Created", value="118")

# Chat Interface
st.subheader("💬 Live Interactive Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User prompt handling
if prompt := st.chat_input("Ask about reservations, allergens, or opening hours..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Call backend API endpoint (fallback to synthetic mode if backend is unavailable)
            response = httpx.post(
                f"{api_base_url}/demo/chat/{restaurant_slug}",
                json={"message": prompt},
                timeout=5.0
            )
            if response.status_code == 200:
                bot_response = response.json().get("response", "Thank you for reaching out!")
            else:
                bot_response = f"[Demo Mode] Guten Tag! Thank you for contacting {restaurant_slug}. We have recorded your request for '{prompt}'."
        except Exception:
            # Graceful fallback so Streamlit Cloud never crashes
            bot_response = f"[Demo Mode] Guten Tag! I am the digital receptionist for {restaurant_slug}. How can I assist you with your table booking today?"

        message_placeholder.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})