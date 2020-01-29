import paho.mqtt.client as mqtt
#imports for LED command modules
import time
import RPi.GPIO as GPIO 
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import LED_ex as LED

MQTT_SERVER = "192.168.43.130" #for Litty
#MQTT_SERVER = "192.168.0.135" #for Naruto
MQTT_PATH = "topic/serene"

# Configure the count of pixels:
PIXEL_COUNT = 8
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

def on_connect(client, userdata, flags, rc):
		print("Connected: result code " + str(rc))
		client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
	    		statement = msg.payload
			print(msg.topic + " " + str(statement))
			if (str(statement) == "Mode 1"):
    				print("mode 1")
				LED.blink_color(pixels, blink_times = 3, color=(100, 0, 0))
			else:
				print("other")
				LED.blink_color(pixels, blink_times = 3,color= (0, 0, 100))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()
