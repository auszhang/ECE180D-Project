#ARCHIVED, NOT FOR CURRENT USE
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.LOW) # turn on
sleep(50)
GPIO.output(16, GPIO.HIGH) # turn off
sleep(50)
