import time

import RPi.GPIO as GPIO

hoorn_GPIO = 17
slagboom_GPIO = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)


def openemen():
    GPIO.output(hoorn_GPIO, GPIO.LOW)


def ophangen():
    GPIO.output(hoorn_GPIO, GPIO.HIGH)


def open_slagboom():
    GPIO.output(slagboom_GPIO, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(slagboom_GPIO, GPIO.LOW)
