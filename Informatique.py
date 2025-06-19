import requests
import time
import os

URL_BASE = "http://192.168.158.231:5000"  

def lancer_message_introduction():
    texte = "Bonjour et bienvenue sur l'interface N'Botumbo. Posez-moi une question sur la culture Baoulé."
    os.system(f'espeak -v fr "{texte}"')  # ou utiliser pyttsx3 si installé
    print("[INFO] Message vocal lancé.")

def changer_page(page_name):
    """Change l'état de la page visible (repos, interaction, aboya, media...)"""
    with open("page_state.txt", "w") as f:
        f.write(page_name)
    print(f"[INFO] Page changée : {page_name}")

