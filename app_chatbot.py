import streamlit as st
from groq import Groq

# ----------------------------
# Osnovna nastavitev Streamlit strani
# ----------------------------
# Določi naslov strani in poravnavo vsebine
st.set_page_config(
    page_title="Maine Royal Chatbot",
    layout="centered"
)

# ----------------------------
# CSS stiliranje (videz + višina chata)
# ----------------------------
# Tukaj z CSS-om spreminjamo barve, robove, ozadje in izgled chata
st.markdown(
    """
    <style>

    /* Nastavi barvo besedila za vse elemente */
    div {
    color: black !important;
    }

    /* Ozadje celotne aplikacije */
    .stApp {
        background-color: #f6f3ee;
        color: #2f2a25;
    }

    /* Ozadje spodnjega dela (input polje) */
    .stBottom div {
        background-color: #f6f3ee;
    }

    /* Barva besedila v input polju */
    textarea { 
    color: black !important;
    }

    /* Barva zgornje vrstice */
    header {
    background-color: #AC9362 !important;}

    /* Zaobljeni robovi input polja */
    .stChatInput {
    border-radius: 8px;
    border: 1px solid black !important;
    }

    /* Odstrani notranje robove inputa */
    .stChatInput div {
    border-radius: 8px;
    border: transparent !important;}

    /* Barva besedila za span elemente */
    span {
        color: black !important;
        }

    /* Barva besedila za odstavke */
    p {
        color: black !important
    }

    /* Omeji maksimalno višino glavnega dela (da je chat manjši) */
    .stMain {
    max-height:500px
    }

    /* Barva besedila uporabnikovih sporočil */
    .user-msg {
        color: black !important
    }

    /* Barva ozadja za vsako drugo sporočilo (uporabnik / asistent) */
    [data-testid="stLayoutWrapper"]:nth-of-type(even) .stChatMessage {
        background-color: #f6f3ee !important; 
        }

    [data-testid="stLayoutWrapper"]:nth-of-type(odd) .stChatMessage {
        background-color: #AC9362 !important; 
        }

    /* Barva ozadja avatarja asistenta */
    .stChatMessage [data-testid="stChatMessageAvatarAssistant"] {
        background-color: white !important;
    }

    /* Barva ozadja avatarja uporabnika */
    .stChatMessage [data-testid="stChatMessageAvatarUser"] {
        background-color: #b7dca4 !important;
    }

    /* Zaobljeni robovi textarea */
    textarea {
        border-radius: 6px !important;
    }
    
    /* Barva placeholder besedila */
    textarea::placeholder {
        color: gray !important;
        opacity: 1 !important;
    }

    /* Stil gumba za pošiljanje */
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
# Naslov in opis aplikacije
# ----------------------------
# Prikaz naslova
st.title("Maine Royal Chatbot")

# Kratek opis pod naslovom
st.write("Klepetalnik za vprašanja o mačkah pasme Maine Coon.")

# ----------------------------
# Inicializacija Groq API
# ----------------------------
# Ustvari Groq client z API ključem iz Streamlit secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------------------
# Spomin pogovora (session_state)
# ----------------------------
# Če še ni shranjenih sporočil, jih inicializiramo
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            # System message določa pravila obnašanja asistenta
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
# Prikaz zgodovine pogovora
# ----------------------------
# Odpre HTML div za chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Izpiše vsa prejšnja sporočila (razen system)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Zapre HTML div za chat
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Vnos uporabnika
# ----------------------------
# Polje za vnos vprašanja
user_input = st.chat_input("Zastavi vprašanje o Maine Coon mačkah...")

if user_input:
    # Shrani uporabnikovo sporočilo v zgodovino
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    try:
        # Pošlje pogovor modelu Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        # Pridobi odgovor asistenta
        ai_text = response.choices[0].message.content

        # Shrani odgovor asistenta v zgodovino
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_text}
        )

        # Ponovno naloži aplikacijo, da se prikaže nov odgovor
        st.rerun()

    except Exception as e:
        # Prikaže napako, če pride do težave
        st.error("Prišlo je do napake pri komunikaciji s strežnikom.")
