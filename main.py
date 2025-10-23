import streamlit as st
from google import genai
from google.genai.errors import APIError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except APIError as e:
    st.error(f"Error initializing Gemini client: {e}")
    st.stop()

# Streamlit page setup
st.set_page_config(page_title="AI Chatbot - Gemini", page_icon="🤖", layout="wide")

st.markdown(
    """
<style>
    /* Page background and fonts */
    body {
        background: #F7F9FA;
        font-family: 'Roboto', 'Segoe UI', sans-serif;
        color: #1C1E21;
    }

    /* General chat message styling */
    .chat-bubble {
        border-radius: 18px;
        padding: 14px 18px;
        margin-bottom: 10px;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* User bubble */
    .user-msg {
        background-color:  #343541; 
        color: white;
        text-align: right;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }

    /* Bot bubble */
    .ai-msg {
        background-color: #E8EAED; 
        color: #1C1E21;
        text-align: left;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }

    /* Input box style */
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 14px 20px;
        border-radius: 24px;
        border: 1px solid #DADCE0; 
        background-color: #E8EAED;
        border: 1px solid #DADCE0;
        box-shadow: 0 1px 3px rgba(60,64,67,.1);
        transition: border-color 0.3s, box-shadow 0.3s;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4285F4;
        box-shadow: 0 1px 3px rgba(60,64,67,.1), 0 4px 6px rgba(60,64,67,.15);
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #F7F9FA;
    }
    ::-webkit-scrollbar-thumb {
        background: #BCC0C4;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #9AA0A6;
    }
</style>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
<div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712139.png" width="100" style="margin-right: 15px;">
    <h1 style="margin: 0; font-family: 'Roboto', sans-serif; color: #1C1E21;">Gemini AI Chatbot</h1>
</div>
""", unsafe_allow_html=True)


# Maintain chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

def chat_with_gemini(prompt: str) -> str:
    """Send prompt to Gemini model and get response."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except APIError as e:
        return f"⚠️ API error: {e}"
    except Exception as e:
        return f"⚠️ Unexpected error: {e}"

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner("Gemini is thinking... 🤔"):
        reply = chat_with_gemini(user_input)
    st.session_state["messages"].append({"role": "assistant", "content": reply})

# Display messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='chat-bubble user-msg'><b>You:</b> {msg['content']}</div>", 
            unsafe_allow_html=True
        )
    else:
        # Clean Gemini response by removing Markdown bold symbols
        clean_content = msg['content'].replace("**", "")
        st.markdown(
            f"<div class='chat-bubble ai-msg'><b>Gemini:</b> {clean_content}</div>", 
            unsafe_allow_html=True
        )

