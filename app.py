import streamlit as st
from groq import Groq

# ----------------------------
# Nastavitve strani
# ----------------------------
st.set_page_config(
    page_title="Maine Royal Chatbot",
    page_icon=None,
    layout="centered"
)

st.title("Maine Royal Chatbot")
st.write("Pametni klepetalnik za vprašanja o mačkah in izdelkih Maine Royal.")

# ----------------------------
# Groq API ključ iz Streamlit Secrets
# ----------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------------------
# Spomin znotraj seje
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Si prijazen asistent za podjetje Maine Royal. "
                "Odgovarjaš samo na vprašanja o mačkah in izdelkih Maine Royal. "
                "Če uporabnik vpraša kaj drugega, vljudno povej, da nimaš informacij. "
                "Odgovarjaš izključno v slovenščini, slovnično pravilno."
            )
        }
    ]

# ----------------------------
# Prikaz zgodovine pogovora
# ----------------------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ----------------------------
# Vnos uporabnika
# ----------------------------
user_input = st.chat_input("Vpiši svoje vprašanje...")

if user_input:
    # Dodamo uporabnikov vnos v zgodovino
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Klic Groq API
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        ai_text = response.choices[0].message.content

        # Shranimo AI odgovor v zgodovino
        st.session_state.messages.append({"role": "assistant", "content": ai_text})

        # Prikaz odgovora
        with st.chat_message("assistant"):
            st.markdown(ai_text)

    except Exception as e:
        st.error(f"Prišlo je do napake: {e}")