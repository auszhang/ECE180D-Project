
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
MY_ID = ""
LAST_WILL = ""
INITIALIZED = False

# Configure the count of pixels:
PIXEL_COUNT = 8
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

def on_connect(client, userdata, flags, rc):
		print("Connected: result code " + str(rc))
		client.subscribe(listen_path)
		#publish.single(send_path, '123', hostname = MQTT_SERVER) #Serene testing something

def on_message(client, userdata, msg):
	    		statement = msg.payload
			print("RPi received")
			print(msg.topic + " " + str(statement))
			if (str(statement) == "Mode 1"):
    			print("Mode 1")
				LED.blink_color(pixels, blink_times = 3, color=(100, 0, 0))
			elif (("b" in statement) or ("d" in statement)):
    			print("enacting with color!!!!!!!!!!!")
				LED.enact_lights_with_color(pixels,str(statement), MY_ID)
			else:
    			LED.enact_lights_basic(pixels, str(statement), MY_ID)

# Initialize MQTT client.
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect(MQTT_SERVER, 1883, 60)
# # Start MQTT client in separate thread.
# # client.loop_start() #commented out by serene
# client.loop_forever()

while True:    
	try:
		data = raw_input("Type Name;row;col :")
		if len(data) == 0:
			break
		print("received [%s]") % data
		data_array = data.split(";")
		if len(data_array) == 3:
			# Parse client data from Bluetooth data.
			my_name = data_array[0]
			my_row = data_array[1]
			my_col = data_array[2]
			# Generate my client ID, set last will.
			MY_ID = str(hash(my_name))
                        if not INITIALIZED:
                            client = mqtt.Client()
                            LAST_WILL = MY_ID + "DIED"
                            client.on_connect=on_connect
                            client.on_message=on_message
                            client.will_set(send_path,str.encode(LAST_WILL),0,False)
                            client.connect(MQTT_SERVER, 1883, 60)
                            client.loop_start()
                            INITIALIZED = True
			# Send payload to server.
			send_data = ";"
			send_data = send_data.join([my_row,my_col,my_name,"",MY_ID])
			publish.single(send_path, send_data, hostname = MQTT_SERVER)

	except IOError:
		pass

	except KeyboardInterrupt:

		print("disconnected")
		break