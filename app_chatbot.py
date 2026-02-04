import streamlit as st
from groq import Groq

# ----------------------------
# Page config (embed-friendly)
# ----------------------------
st.set_page_config(
    page_title="Maine Royal Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# Hide Streamlit UI junk
# ----------------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Custom styling (SAFE)
# ----------------------------
st.markdown("""
<style>
body {
    background-color: #f6f3ee;
    color: #2f2a25;
}

.chat-wrapper {
    max-height: 320px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #d6d0c8;
    border-radius: 8px;
    background-color: #ffffff;
    margin-bottom: 8px;
}

.user-msg {
    background-color: #eef3ea;
    padding: 8px;
    border-radius: 6px;
    margin-bottom: 6px;
}

.ai-msg {
    background-color: #ffffff;
    padding: 8px;
    border-radius: 6px;
    border: 1px solid #d6d0c8;
    margin-bottom: 6px;
}

textarea {
    border-radius: 6px !important;
}

button {
    background-color: #b7dca4 !important;
    color: #2f2a25 !important;
    border-radius: 6px !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Title
# ----------------------------
st.markdown("### 🐾 Maine Royal Chatbot")
st.write("Vprašanja o mačkah pasme **Maine Coon** in Maine Royal izdelkih.")

# ----------------------------
# Groq client
# ----------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------------------
# Session memory
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Si prijazen asistent za podjetje Maine Royal. "
                "Odgovarjaš samo na vprašanja o mačkah pasme Maine Coon "
                "in izdelkih Maine Royal. "
                "Vedno odgovarjaš v slovenščini."
            )
        }
    ]

# ----------------------------
# Chat history (OWN container)
# ----------------------------
with st.container():
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-msg">{msg["content"]}</div>',
                unsafe_allow_html=True
            )
        elif msg["role"] == "assistant":
            st.markdown(
                f'<div class="ai-msg">{msg["content"]}</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Input
# ----------------------------
user_input = st.chat_input("Zastavi vprašanje o Maine Coon mačkah...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    ai_text = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_text})

    st.rerun()
