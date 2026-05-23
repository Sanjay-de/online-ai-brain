import streamlit as st
import google.generativeai as genai
import asyncio

# --- FIX FOR THE RUNTIME ERROR ---
# This forces an active event loop inside Streamlit's execution thread
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
# ---------------------------------

st.set_page_config(page_title="Cloud Second Brain", layout="wide")
st.title("🌐 My Cloud-Based Second Brain")
st.caption("Online | Powered by Gemini API | Hosted in the Cloud")

# Sidebar for Secure API Entry
st.sidebar.header("🔑 Authentication")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
st.sidebar.markdown("[Get a free API Key here](https://aistudio.google.com/)")

# Task Selection
task_type = st.selectbox(
    "What are we doing today?",
    ["General Chat", "Fix My Code", "Summarize Meeting Notes", "Draft an Email"]
)

user_input = st.text_area("Paste your text or prompt here:", height=250)
generate_btn = st.button("🚀 Process with Cloud AI", type="primary")

if generate_btn:
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar to proceed.")
    elif not user_input.strip():
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Processing via Cloud API..."):
            try:
                # Configure the cloud client
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # Structure the instruction prompt
                full_prompt = f"Task: {task_type}\nInput: {user_input}"
                
                # Fetch response from Google Cloud Servers
                response = model.generate_content(full_prompt)
                
                st.markdown("### Cloud AI Response:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
