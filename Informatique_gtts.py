from gtts import gTTS
import os

def lancer_message_introduction():
    texte = "Bonjour et bienvenue sur l'interface N'Botumbo. Posez-moi une question sur la culture Baoulé."
    tts = gTTS(text=texte, lang='fr')
    tts.save("intro.mp3")
    os.system("mpg123 intro.mp3")  # Assure-toi que mpg123 est installé
    print("[INFO] Message vocal lancé avec gTTS.")

def changer_page(page_name):
    with open("page_state.txt", "w") as f:
        f.write(page_name)
    print(f"[INFO] Page changée : {page_name}")
