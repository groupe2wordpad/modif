# electronique.py

import RPi.GPIO as GPIO
import time

# --- Configuration Générale ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Numérotation BCM (broches GPIO)

BROCHE_TRIG = 23
BROCHE_ECHO = 24
BROCHE_LED = 17

DISTANCE_DETECTION_CM = 9

def initialiser_gpio():
    print("[GPIO] Initialisation des broches...")
    GPIO.cleanup()  # Reset au cas où une session GPIO est restée active
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(BROCHE_TRIG, GPIO.OUT)
    GPIO.output(BROCHE_TRIG, False)

    GPIO.setup(BROCHE_ECHO, GPIO.IN)
    GPIO.setup(BROCHE_LED, GPIO.OUT)
    GPIO.output(BROCHE_LED, GPIO.LOW)

    time.sleep(0.5)

def nettoyer_gpio():
    print("[GPIO] Nettoyage des broches...")
    GPIO.cleanup()

def mesurer_distance():
    GPIO.output(BROCHE_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(BROCHE_TRIG, False)

    debut = time.time()
    timeout = debut + 1
    while GPIO.input(BROCHE_ECHO) == 0 and time.time() < timeout:
        debut = time.time()

    if time.time() >= timeout:
        return 9999.99

    fin = time.time()
    timeout = fin + 1
    while GPIO.input(BROCHE_ECHO) == 1 and time.time() < timeout:
        fin = time.time()

    if time.time() >= timeout:
        return 9999.99

    duree = fin - debut
    distance = round(duree * 34300 / 2, 2)
    return distance

def allumer_led():
    GPIO.output(BROCHE_LED, GPIO.HIGH)

def eteindre_led():
    GPIO.output(BROCHE_LED, GPIO.LOW)

def personne_detectee():
    distance = mesurer_distance()
    print(f"[CAPTEUR] Distance mesurée : {distance} cm")
    return distance < DISTANCE_DETECTION_CM
