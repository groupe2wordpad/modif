# main.py

from electronique import initialiser_gpio, nettoyer_gpio, personne_detectee, allumer_led, eteindre_led
from informatique import lancer_message_introduction, changer_page
from flask import Flask, request, jsonify
import threading
import time
import os
import requests

app = Flask(__name__)

# --- INITIALISATION GPIO ---
initialiser_gpio()
print("[MAIN] ✅ GPIO initialisés.")

# --- THREAD : Détection de présence ---
def detection_loop():
    print("[MAIN] 🎯 Attente de détection...")
    while True:
        if personne_detectee():
            print("[MAIN] ✅ Présence détectée !")
            allumer_led()
            time.sleep(3)

            lancer_message_introduction()
            changer_page("interaction")
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

def traiter_question_rasa_et_vocaliser(question):
    try:
        response = requests.post(
            "https://referentiel-rasa.onrender.com/webhooks/rest/webhook",
            json={"sender": "user", "message": question},
            timeout=10
        )
        response.raise_for_status()
        messages = response.json()

        if not isinstance(messages, list) or not messages or "text" not in messages[0]:
            print("[RASA] ⚠️ Réponse vide ou mal formatée :", messages)
            return

        texte_reponse = messages[0]["text"]
        print(f"[RASA] 🧠 Réponse : {texte_reponse}")

        os.system(f'espeak -v fr "{texte_reponse}"')
        changer_page("aboya")

    except Exception as e:
        print(f"[ERROR] ❌ Exception dans le traitement Rasa : {e}")

# --- Lancement Flask + Thread capteur ---
if __name__ == "__main__":
    try:
        threading.Thread(target=detection_loop).start()
        app.run(host="0.0.0.0", port=6000, debug=True)
    except KeyboardInterrupt:
        nettoyer_gpio()
        print("[MAIN] 🔌 Arrêt manuel.")
    finally:
        nettoyer_gpio()
