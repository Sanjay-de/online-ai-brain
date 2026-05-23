import streamlit as st
import google.generativeai as genai
import asyncio

# --- FIX FOR THE STREAMLIT RUNTIME ASYNC EVENT LOOP ---
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
# -----------------------------------------------------

# Configure full application view
st.set_page_config(page_title="Personal AI Chatbot", page_icon="💬", layout="centered")
st.title("💬 My Personal Cloud Chatbot")
st.caption("Active Memory Enabled | Ask Follow-up Questions Anytime")

# Sidebar Configuration for API Authentication
st.sidebar.header("🔑 Authentication")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
st.sidebar.markdown("[Get a free API Key here](https://aistudio.google.com/)")

# Add a handy reset button to wipe out chat memory and start fresh
if st.sidebar.button("🧹 Clear Chat History", type="secondary"):
    st.session_state.chat_history = []
    st.rerun()

# --- CHAT MEMORY INITIALIZATION ---
# This initializes an ongoing memory list inside Streamlit's cache
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous chat logs on screen so they don't disappear on re-render
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC MANAGER ---
# st.chat_input opens a native typing bar at the bottom of the page
if user_message := st.chat_input("Ask me anything..."):
    
    # 1. Display your newly typed message instantly on screen
    with st.chat_message("user"):
        st.markdown(user_message)
    
    # Save user message to our persistent memory bank
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    
    # 2. Check for security verification
    if not api_key:
        st.error("Please provide your Gemini API Key in the left sidebar to activate the chat session.")
    else:
        # 3. Request process from Gemini API cloud servers
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Authenticate user key
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    
                    # Convert our local session memory list into the structural format Gemini expects
                    gemini_history = []
                    for msg in st.session_state.chat_history[:-1]: # exclude the brand new prompt
                        gemini_history.append({
                            "role": "user" if msg["role"] == "user" else "model",
                            "parts": [msg["content"]]
                        })
                    
                    # Initialize an ongoing official chat instance with memory tracking
                    chat_session = model.start_chat(history=gemini_history)
                    
                    # Fetch response streaming or processing directly from cloud backend
                    response = chat_session.send_message(user_message)
                    
                    # Render response onto screen
                    st.markdown(response.text)
                    
                    # Save assistant message to memory bank
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
