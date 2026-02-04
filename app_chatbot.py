import streamlit as st
from groq import Groq

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Maine Royal Chatbot",
    layout="centered"
)

# ----------------------------
# Custom CSS (visual styling + height control)
# ----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f6f3ee;
        color: #2f2a25;
    }

    .stBottom div {
        background-color: #f6f3ee;
    }

    span {
        color: black !important;
        }

        p {
        color: black !important
    }

    .user-msg {
        color: black !important
    }

    .stChatMessage.user {
        background-color: #eef3ea;
    }

    .stChatMessage.assistant {
        background-color: #ffffff;
    }

    .chat-container {
        max-height: 350px;
        overflow-y: auto;
        padding-right: 4px;
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
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Title and description
# ----------------------------
st.title("Maine Royal Chatbot")
st.write("Klepetalnik za vprašanja o mačkah pasme Maine Coon.")

# ----------------------------
# Groq API
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
                "Si prijazen asistent za spletno stran Svet Maine Coon. "
                "Odgovarjaš izključno na vprašanja o mačkah pasme Maine Coon, "
                "njihovih značilnostih, negi in prehrani. "
                "Če vprašanje ni povezano s to temo, vljudno povej, "
                "da za to področje nimaš informacij. "
                "Odgovarjaš samo v slovenščini."
            )
        }
    ]

# ----------------------------
# Chat history (limited height)
# ----------------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# User input
# ----------------------------
user_input = st.chat_input("Zastavi vprašanje o Maine Coon mačkah...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        ai_text = response.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_text}
        )

        st.rerun()

    except Exception as e:
        st.error("Prišlo je do napake pri komunikaciji s strežnikom.")
