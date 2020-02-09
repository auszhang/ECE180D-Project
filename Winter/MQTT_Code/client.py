# Bluetooth imports
import os
import glob
import time
import sys
# NO BLUETOOTH FOR NOW
# from bluetooth import *
# MQTT imports
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
#imports for LED command modules
import RPi.GPIO as GPIO 
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import LED_ex as LED

sys.path.insert(1, '../IMU_Code')

#import Compass

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
base_dir = '/sys/bus/w1/devices/'

# server_sock=BluetoothSocket( RFCOMM )
# server_sock.bind(("",PORT_ANY))
# server_sock.listen(1)
# port = server_sock.getsockname()[1]
# uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
# advertise_service( server_sock, "AquaPiServer",
                   #service_id = uuid,
                   #service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   #profiles = [ SERIAL_PORT_PROFILE ], 
                    #)

MQTT_SERVER = "192.168.43.130" #for Litty
#MQTT_SERVER = "192.168.0.135" #for Naruto
listen_path = "topic/serene"
send_path = "topic/init_loc"
MY_ID = ""
LAST_WILL = ""
INITIALIZED = False
MY_CURRENT_LIGHTING = ""
# GAME VARIABLES
HAVE_POTATO = False
#HAVE_POTATO_STRING = ""


# Configure the count of pixels:
PIXEL_COUNT = 8
# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

# Game variables
# HAVE_POTATO = False
# HAVE_POTATO_STRING = ""

def on_connect(client, userdata, flags, rc):
		print("Connected: result code " + str(rc))
		client.subscribe(listen_path)

def on_message(client, userdata, msg):
		payload = msg.payload
		statement = str(payload)
		print("RPi received")
		print(msg.topic + " " + statement)
		print(statement.split(";"))
		if "RECEIVE" or "FAILED_TO_PASS" in statement:
			data = statement.split(";")
			if MY_ID == str(data[0]):
				print("RECOGNIZED MY ID")
				global HAVE_POTATO
				HAVE_POTATO  = True

while True:
	#print("Waiting for connection on RFCOMM channel %d")% port

	#client_sock, client_info = server_sock.accept()
	#print("Accepted connection from ", client_info)
	try:
		send_data =  ";"
		if not INITIALIZED:
			# Get user data from commandline
			my_name = raw_input("Enter your name: ")
			MY_ID = str(hash(my_name))
			print("Your id is: " + MY_ID)
			my_pos = raw_input("Enter your position (number between 1 and 4): ")
			# Initialize MQTT
			client = mqtt.Client()
			LAST_WILL = MY_ID + "DIED"
			client.on_connect=on_connect
			client.on_message=on_message
			client.will_set(send_path,str.encode(LAST_WILL),0,False)
			client.connect(MQTT_SERVER, 1883, 60)
			client.loop_start()
			# Initial payload with client location, name, and id
			send_data = send_data.join([my_pos,my_name,MY_ID])
			publish.single(send_path, send_data, hostname = MQTT_SERVER)
			INITIALIZED = True
		if HAVE_POTATO:
			print("Received potato!")
			pass_pos = raw_input("Enter which direction to pass (R, L, or A): ")
			position = ""
			if pass_pos == "R":
				position = "RIGHT"
			elif pass_pos == "L":
				position = "LEFT"
			elif pass_pos == "A":
				position = "ACROSS"
			# Passing payload with client id, keyword, and position to pass to
			send_data = send_data.join([MY_ID,"PASS_POTATO",position])
			publish.single(send_path, send_data, hostname = MQTT_SERVER)
			print("Passing potato!")
			HAVE_POTATO = False
		#data = client_sock.recv(1024)
		#if len(data) == 0:
			#break
		#print("received [%s]") % data
		#data_array = data.split(";")
		#if len(data_array) == 3:
			# Parse client data from Bluetooth data.
			#my_name = data_array[0]
			#my_row = data_array[1]
			#my_col = data_array[2]
			# Generate my client ID, set last will.
			#MY_ID = str(hash(my_name))
                        #if not INITIALIZED:
                            #client = mqtt.Client()
                            #LAST_WILL = MY_ID + "DIED"
                            #client.on_connect=on_connect
                            #client.on_message=on_message
                            #client.will_set(send_path,str.encode(LAST_WILL),0,False)
                            #client.connect(MQTT_SERVER, 1883, 60)
                            #client.loop_start()
                            #INITIALIZED = True
			# Send payload to server.
			#send_data = ";"
			#send_data = send_data.join([my_row,my_col,my_name,"",MY_ID])
			#publish.single(send_path, send_data, hostname = MQTT_SERVER)

	except IOError:
		pass

	except KeyboardInterrupt:

		print("disconnected")

		client_sock.close()
		server_sock.close()
		print("all done")

		break
