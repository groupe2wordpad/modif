from TTS.api import TTS
import os

# Charge un modèle pré-entraîné Coqui TTS (anglais par défaut, tu peux en changer)
tts = TTS(model_name="tts_models/fr/css10/vits", progress_bar=False, gpu=False)

def lancer_message_introduction():
    texte = "Bonjour et bienvenue sur l'interface N'Botumbo. Posez-moi une question sur la culture Baoulé."
    output_path = "intro.wav"
    tts.tts_to_file(text=texte, file_path=output_path)
    os.system(f'aplay {output_path}')
    print("[INFO] Message vocal lancé avec Coqui TTS.")

def changer_page(page_name):
    with open("page_state.txt", "w") as f:
        f.write(page_name)
    print(f"[INFO] Page changée : {page_name}")
