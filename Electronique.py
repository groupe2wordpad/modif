# electronique.py

import RPi.GPIO as GPIO
import time

# --- Configuration Générale ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

BROCHE_TRIG = 23
BROCHE_ECHO = 24
BROCHE_LED = 17

DELAI_EXTINCTION_SECONDES = 2
DISTANCE_DETECTION_CM = 9

def initialiser_gpio():
    GPIO.setup(BROCHE_TRIG, GPIO.OUT)
    GPIO.setup(BROCHE_ECHO, GPIO.IN)
    GPIO.output(BROCHE_TRIG, False)
    time.sleep(0.5)

    GPIO.setup(BROCHE_LED, GPIO.OUT)
    GPIO.output(BROCHE_LED, GPIO.LOW)

def nettoyer_gpio():
    GPIO.cleanup()

def mesurer_distance():
    GPIO.output(BROCHE_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(BROCHE_TRIG, False)

    debut = time.time()
    while GPIO.input(BROCHE_ECHO) == 0:
        debut = time.time()
        if time.time() - debut > 1:
            return 9999.99

    fin = time.time()
    while GPIO.input(BROCHE_ECHO) == 1:
        fin = time.time()
        if time.time() - fin > 1:
            return 9999.99

    duree = fin - debut
    distance = round(duree * 34300 / 2, 2)
    return distance

def allumer_led():
    GPIO.output(BROCHE_LED, GPIO.HIGH)

def eteindre_led():
    GPIO.output(BROCHE_LED, GPIO.LOW)

def personne_detectee():
    """Renvoie True si quelqu’un est détecté à moins de DISTANCE_DETECTION_CM"""
    distance = mesurer_distance()
    print(f"Distance mesurée : {distance} cm")
    return distance < DISTANCE_DETECTION_CM
