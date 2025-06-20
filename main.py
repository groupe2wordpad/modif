from electronique import initialiser_gpio, nettoyer_gpio, personne_detectee, allumer_led, eteindre_led
from informatique import lancer_message_introduction, changer_page
from flask import Flask, request, jsonify
import threading
import time
import os
import subprocess
import json

# Import et initialisation Coqui TTS
from TTS.api import TTS
tts = TTS(model_name="tts_models/fr/css10/vits", progress_bar=False, gpu=False)

app = Flask(__name__)

# --- INITIALISATION GPIO ---
initialiser_gpio()

# --- THREAD : Détection de présence ---
def detection_loop():
    print("[MAIN] 🎯 Attente de détection...")
    while True:
        if personne_detectee():
            print("[MAIN] ✅ Présence détectée !")
            allumer_led()
            time.sleep(3)  # temporisation volontaire

            # Message vocal d’intro
            lancer_message_introduction()

            # Passage à la page 2
            changer_page("interaction")

            # Optionnel : arrêter la détection si besoin (sinon boucle continue)
            break

        else:
            eteindre_led()
        time.sleep(0.5)

# --- TRAITEMENT : Réception question et réponse via Rasa ---
@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("message", "").strip()

    if not question:
        return jsonify({"error": "Aucune question reçue"}), 400

    print(f"[MAIN] 📨 Question reçue : {question}")
    threading.Thread(target=traiter_question_rasa_et_vocaliser, args=(question,)).start()
    return jsonify({"status": "ok"})

def traiter_question_rasa_et_vocaliser(question, mode="rhvoice"):  # ou "gtts"
    try:
        print(f"[RASA] ➡️ Envoi de la question à Rasa : {question}")
        response = subprocess.run(
            ["curl", "-X", "POST", "http://localhost:5005/webhooks/rest/webhook",
             "-H", "Content-Type: application/json",
             "-d", f'{{"sender": "user", "message": "{question}"}}'],
            capture_output=True, text=True
        )

        if response.returncode != 0:
            print("[RASA] ❌ Erreur appel Rasa :", response.stderr)
            return

        messages = json.loads(response.stdout)
        if not messages or "text" not in messages[0]:
            print("[RASA] ⚠️ Réponse vide ou mal formatée :", messages)
            return

        texte_reponse = messages[0]["text"]
        print(f"[RASA] 🧠 Réponse : {texte_reponse}")

        # Choix du moteur vocal
        if mode == "gtts":
            from gtts import gTTS
            tts = gTTS(text=texte_reponse, lang='fr')
            tts.save("response.mp3")
            os.system("mpg123 response.mp3")

        elif mode == "rhvoice":
            subprocess.run(['RHVoice-test', '-p', 'anna'], input=texte_reponse.encode('utf-8'))

        else:
            print("[TTS] ⚠️ Moteur vocal non reconnu :", mode)
            return

        changer_page("aboya")

    except Exception as e:
        print(f"[ERROR] ❌ Exception dans le traitement Rasa : {e}")


# --- Lancement de Flask + thread capteur ---
if __name__ == "__main__":
    try:
        threading.Thread(target=detection_loop).start()
        app.run(host="0.0.0.0", port=6000, debug=True)
    except KeyboardInterrupt:
        nettoyer_gpio()
        print("[MAIN] 🔌 Arrêt manuel.")
