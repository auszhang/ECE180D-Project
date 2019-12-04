
# Bluetooth imports
import os
import glob
import time
from bluetooth import *
# MQTT imports
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
#imports for LED command modules
import RPi.GPIO as GPIO 
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import LED_ex as LED

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
base_dir = '/sys/bus/w1/devices/'

MQTT_SERVER = "192.168.43.130" #for Litty
listen_path = "topic/serene"
send_path = "topic/init_loc"

# Configure the count of pixels:
PIXEL_COUNT = 8
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

def on_connect(client, userdata, flags, rc):
		print("Connected: result code " + str(rc))
		client.subscribe(listen_path)
		publish.single(send_path, '123', hostname = MQTT_SERVER) #Serene testing something

def on_message(client, userdata, msg):
	    		statement = msg.payload
			print("RPi received")
			print(msg.topic + " " + str(statement))
			if (str(statement) == "Mode 1"):
    				print("Mode 1")
				LED.blink_color(pixels, blink_times = 3, color=(100, 0, 0))
			else:
				LED.enact_lights_basic(pixels, str(statement))

# Initialize MQTT client.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)
# Start MQTT client in separate thread.
# client.loop_start() #commented out by serene
client.loop_forever()