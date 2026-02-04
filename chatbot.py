import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

# Naložimo API ključ iz .env datoteke
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Zgodovina pogovora
messages = [
    {
        "role": "system",
        "content": (
            "Si prijazen asistent za podjetje Maine Royal. "
            "Odgovarjaš samo na vprašanja o mačkah in izdelkih Maine Royal. "
            "Če uporabnik vpraša kaj drugega, vljudno povej, da nimaš informacij."
        )
    }
]

print("--- Klepetalnik je pripravljen! (vpiši 'stop' za izhod) ---")

while True:
    vnos = input("Vi: ")

    # Če uporabnik vpiše stop, shranimo pogovor in končamo program
    if vnos.lower() == "stop":
        with open("zgodovina_pogovora.txt", "a", encoding="utf-8") as f:
            cas = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            f.write(f"\n--- Pogovor ({cas}) ---\n")

            for msg in messages:
                f.write(f"{msg['role']}: {msg['content']}\n")

        print("Pogovor shranjen. Nasvidenje!")
        break

    # Dodamo uporabnikov vnos
    messages.append({"role": "user", "content": vnos})

    # Omejitev zgodovine na 10 sporočil
    if len(messages) > 10:
        messages.pop(1)

    try:
        # Pokličemo AI
        odgovor = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        ai_text = odgovor.choices[0].message.content
        print("\nAI:", ai_text, "\n")

        # Dodamo AI odgovor v zgodovino
        messages.append({"role": "assistant", "content": ai_text})

        # Izpis porabe žetonov
        print("Poraba žetonov:")
        print("Vprašanje:", odgovor.usage.prompt_tokens)
        print("Odgovor:", odgovor.usage.completion_tokens)
        print("Skupaj:", odgovor.usage.total_tokens, "\n")

    except Exception as e:
        print("Napaka:", e)
