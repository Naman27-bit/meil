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

    /* Hide broken material icons text in chat avatars */
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"],
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
        display: none !important;
    }

    /* Hide keyboard_double_arrow text in sidebar toggle button */
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="collapsedControl"] span,
    [data-testid="stSidebarCollapseButton"] .material-symbols-rounded,
    [data-testid="collapsedControl"] .material-symbols-rounded,
    button[data-testid="stSidebarCollapseButton"] > span {
        font-size: 0 !important;
        visibility: hidden !important;
        width: 0 !important;
    }

    /* Style sidebar toggle button as clean circle */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        background: #e05a00 !important;
        border-radius: 50% !important;
        border: none !important;
        width: 34px !important;
        height: 34px !important;
    }
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="collapsedControl"] svg {
        fill: white !important;
        color: white !important;
    }

    html, body, [class*="css"],
    p, span, div, label, input, textarea, button,
    .stMarkdown, .stText {
        font-family: 'Nunito', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #fef9f0 0%, #fff4e6 50%, #fef0f5 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
        border-right: 2px solid #e05a00;
    }
    [data-testid="stSidebar"] * {
        color: #f0f0f0 !important;
        font-family: 'Nunito', sans-serif !important;
    }
    [data-testid="stSidebar"] h1 {
        color: #ffffff !important;
        font-size: 1.6rem !important;
    }
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #e05a00, #c44b00) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        width: 100% !important;
        padding: 0.5rem !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #e05a0044 !important;
    }

    /* Title */
    h1 {
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

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e8e8f0 !important;
        border-radius: 16px !important;
        margin: 8px 0 !important;
        padding: 10px 16px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, #fff4e6, #fef0f5) !important;
        border-color: #f0c080 !important;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        background: #ffffff !important;
        border: 2px solid #e05a00 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(224,90,0,0.15) !important;
    }
    [data-testid="stChatInput"] textarea {
        background: #ffffff !important;
        color: #1a1a2e !important;
        font-size: 15px !important;
        font-family: 'Nunito', sans-serif !important;
    }

    /* Selectbox - white bg, dark text */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
        background: #ffffff !important;
        border: 1.5px solid #e05a00 !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] [data-testid="stSelectbox"] span,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] p {
        color: #1a1a2e !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    [data-testid="stSidebar"] [data-testid="stSelectbox"] label {
        color: #f0c080 !important;
        font-weight: 700 !important;
    }

    /* Text input API Key - white bg dark text */
    [data-testid="stSidebar"] [data-testid="stTextInput"] input {
        background: #ffffff !important;
        color: #1a1a2e !important;
        border: 1.5px solid #e05a00 !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] [data-testid="stTextInput"] label {
        color: #f0c080 !important;
        font-weight: 700 !important;
    }

    /* Caption / Model ID */
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small {
        color: #aac4ff !important;
        font-size: 12px !important;
    }

    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍽️ TanuShree")
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
    selected_label = st.selectbox("Selected Model", list(MODEL.keys()), index=0)
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

# ── Main Area ─────────────────────────────────────────────
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

# ── Chat ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "🍕"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

user_input = st.chat_input("Ask me about food, menu, hours... 🍕")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🍕"):
        with st.spinner("Wait! I'm thinking... 🤔"):
            try:
                response = get_answer(user_input, model_name=selected_model)
            except Exception as e:
                response = f"❌ Error: {str(e)}"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
