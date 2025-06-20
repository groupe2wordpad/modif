import os
import subprocess

def lancer_message_introduction():
    texte = "Bonjour et bienvenue sur l'interface N'Botumbo. Posez-moi une question sur la culture Baoulé."
    # RHVoice nécessite un appel via subprocess
    subprocess.run(['RHVoice-test', '-p', 'anna'], input=texte.encode('utf-8'))
    print("[INFO] Message vocal lancé avec RHVoice.")

def changer_page(page_name):
    with open("page_state.txt", "w") as f:
        f.write(page_name)
    print(f"[INFO] Page changée : {page_name}")
