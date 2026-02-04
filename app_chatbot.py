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

    div {
    color: black !important;
    }
    .stApp {
        background-color: #f6f3ee;
        color: #2f2a25;
    }

    .stBottom div {
        background-color: #f6f3ee;
    }

    textarea { 
    color: black !important;
    }

    header {
    background-color: #AC9362 !important;}

  

    .stChatInput {
    border-radius: 8px;
    border: 1px solid black !important;
    }

    .stChatInput div {
    border-radius: 8px;
    border: transparent !important;}

    span {
        color: black !important;
        }

        p {
        color: black !important
    }

    .stMain {
    max-height:500px
    }

    .user-msg {
        color: black !important
    }

    [data-testid="stLayoutWrapper"]:nth-of-type(even) .stChatMessage {
        background-color: #f6f3ee !important; 
        }

        [data-testid="stLayoutWrapper"]:nth-of-type(odd) .stChatMessage {
        background-color: #AC9362 !important; 
        }

        

    .stChatMessage [data-testid="stChatMessageAvatarAssistant"] {
        background-color: white !important;
    }

     .stChatMessage [data-testid="stChatMessageAvatarUser"] {
        background-color: #b7dca4 !important;
    }


    textarea {
        border-radius: 6px !important;
    }
    
    textarea::placeholder {
        color: black !important;
        opacity: 1 !important;
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
