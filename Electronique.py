# electronique.py

import RPi.GPIO as GPIO
import time

# --- Constantes de broches (mode BCM) ---
BROCHE_TRIG = 23
BROCHE_ECHO = 24
BROCHE_LED = 17

DELAI_EXTINCTION_SECONDES = 2
DISTANCE_DETECTION_CM = 9

gpio_initialise = False  # Pour éviter double initialisation

def initialiser_gpio():
    global gpio_initialise
    if gpio_initialise:
        return  # Évite de réinitialiser si déjà fait

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # ✅ IMPORTANT : Définit le mode BCM

    # Configuration des broches
    GPIO.setup(BROCHE_TRIG, GPIO.OUT)
    GPIO.setup(BROCHE_ECHO, GPIO.IN)
    GPIO.output(BROCHE_TRIG, False)

    GPIO.setup(BROCHE_LED, GPIO.OUT)
    GPIO.output(BROCHE_LED, GPIO.LOW)

    time.sleep(0.5)
    gpio_initialise = True
    print("[GPIO] ✅ Initialisation terminée.")

def nettoyer_gpio():
    GPIO.cleanup()
    print("[GPIO] 🧹 Nettoyage terminé.")

def mesurer_distance():
    GPIO.output(BROCHE_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(BROCHE_TRIG, False)

    debut = time.time()
    timeout = debut + 1
    while GPIO.input(BROCHE_ECHO) == 0 and time.time() < timeout:
        debut = time.time()

    fin = time.time()
    timeout = fin + 1
    while GPIO.input(BROCHE_ECHO) == 1 and time.time() < timeout:
        fin = time.time()

    duree = fin - debut
    distance = round(duree * 34300 / 2, 2)
    return distance if distance < 1000 else 9999.99  # Évite valeur absurde

def allumer_led():
    GPIO.output(BROCHE_LED, GPIO.HIGH)

def eteindre_led():
    GPIO.output(BROCHE_LED, GPIO.LOW)

def personne_detectee():
    """Renvoie True si une personne est détectée à moins de DISTANCE_DETECTION_CM"""
    distance = mesurer_distance()
    print(f"[SENSOR] 📏 Distance mesurée : {distance} cm")
    return distance < DISTANCE_DETECTION_CM
