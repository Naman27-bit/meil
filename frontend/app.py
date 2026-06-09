import os
import streamlit as st
import sys
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
api_key = os.environ.get("GROQ_API_KEY")

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from main import get_answer

st.set_page_config(
    page_title="Tanman Restro Chatbot",
    page_icon="🍕",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Nunito:wght@400;500;600;700&display=swap');

    html, body, [class*="css"],
    p, span, div, label, input, textarea, button,
    .stMarkdown, .stText, .stCaption,
    [data-testid="stChatMessageContent"],
    [data-testid="stChatMessageContent"] * {
        font-family: 'Nunito', sans-serif !important;
        color: #1a1a2e;
    }

    .stApp {
        background: linear-gradient(135deg, #fef9f0 0%, #fff4e6 50%, #fef0f5 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f4ff 0%, #e8f0fe 100%);
        border-right: 2px solid #c7d7f5;
    }

    [data-testid="stSidebar"] * {
        color: #1a1a2e !important;
        font-family: 'Nunito', sans-serif !important;
    }

    h1, .stTitle, [data-testid="stHeadingWithActionElements"] h1 {
        font-family: 'Playfair Display', serif !important;
        color: #e05a00 !important;
        font-size: 2.4rem !important;
        font-weight: 700 !important;
    }

    h2, h3, h4 {
        font-family: 'Nunito', sans-serif !important;
        color: #2c3e7a !important;
        font-weight: 700 !important;
    }

    [data-testid="stChatMessage"] {
        background: #ffffff;
        border: 1px solid #dde8ff;
        border-radius: 14px;
        margin: 6px 0;
        padding: 4px 8px;
    }

    [data-testid="stChatInput"] {
        background: #ffffff !important;
        border: 2px solid #4a90d9 !important;
        border-radius: 12px !important;
    }

    [data-testid="stChatInput"] textarea {
        background: #ffffff !important;
        color: #1a1a2e !important;
        font-size: 15px !important;
        font-family: 'Nunito', sans-serif !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #4a90d9, #2c6fba);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 600 !important;
    }

    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/restaurant.png", width=48)
    st.title("TanuShree")
    st.markdown("*Your AI-powered restaurant assistant*")
    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 🤖 Model Used")
    MODEL = {
        "llama-3.1-8b-instant (Fast ✅)": "llama-3.1-8b-instant"
    }

    selected_label = st.selectbox("🤖 Selected Model", list(MODEL.keys()), index=0)
    selected_model = MODEL[selected_label]
    st.caption(f"Model ID: `{selected_model}`")

    st.markdown("---")
    st.markdown("### 🔑 Groq API Key")
    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Free key at https://console.groq.com"
    )
    if api_key_input:
        os.environ["GROQ_API_KEY"] = api_key_input.strip()
        st.success("✅ Key set!")

    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.markdown("**Naman Kumar**")
    st.markdown("Built with **Streamlit** + **Groq** + **Llama 3**")

col1, col2 = st.columns([3, 1])
with col1:
    st.title("🍕 Tanman Restro Assistant")
    st.caption("Ask me anything about our menu, reviews, hours & more!")
with col2:
    st.image("https://i.postimg.cc/LsPyp4bn/Whats-App-Image-2026-05-26-at-7-21-45-PM.jpg", width=120)

st.markdown("---")
st.markdown(
    "👋 Hi! I'm **TanuShree**, your AI Restaurant Assistant. "
    "Ask me about our **menu**, **specials**, **hours**, or anything else! 🍜🍣"
)
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask me about food, menu, hours... 🍕")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Wait! I'm thinking... 🤔"):
            try:
                response = get_answer(user_input, model_name=selected_model)
            except Exception as e:
                response = f"❌ Error: {str(e)}"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
