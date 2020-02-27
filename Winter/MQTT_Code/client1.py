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

#import IMU code
sys.path.insert(1, '../IMU_Code')
import GestureRecognition

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

#GPIO.setup(17, GPIO.OUT)
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
# GAME VARIABLES
HAVE_POTATO = False
SERVER_TIME = 0
TURN_START_TIME = 0
FAILED = False


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
		#print("RPi received")
		#print(msg.topic + " " + statement)
		#print(statement.split(";"))
		global HAVE_POTATO
		global SERVER_TIME
		global FAILED      
		if "RECEIVE" or "FAILED_TO_PASS" in statement:
				data = statement.split(";")
				if MY_ID == str(data[0]):
						#print("RECOGNIZED MY ID")
						HAVE_POTATO  = True
						if "RECEIVE" in statement:
								FAILED = False                 
								SERVER_TIME = int(data[2]) # Update max timer duration
						if "FAILED_TO_PASS" in statement:
								FAILED = True   

def check_time(timer_length, time_elapsed, num):
		approx = time_elapsed * num / timer_length
		if time_elapsed < timer_length:
				for i in range(1,num+1):
						if approx >= i-0.05 and approx < i + 0.05:
								print(str(i) + "interval passed")
								if i >= num-1:
										print("Final or 2nd to last warning!")
										LED.final_warning_lights(pixels)
								else:
    									LED.timer_interval_lights(pixels)
				LED.have_potato_lights(pixels) #reset after interval flash!
				GPIO.output(12, 1)

				return False
		else:
				print("Time's up!")
				LED.eliminated_lights(pixels)
				GPIO.output(12, 0)
				return True	

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
			# LIGHTING SCHEME FOR NO POTATO

			#TO DO: add elimination lights if person was eliminated
			LED.no_potato_lights(pixels)
			GPIO.output(12, 0)
		if HAVE_POTATO:
			print("Received potato!")
			# pass_pos = raw_input("Enter which direction to pass (R, L, or A): ")s
			
			# LIGHTING SCHEME FOR WITH POTATO
			LED.have_potato_lights(pixels)
			# TURN ON VIBRATION MOTOR
			GPIO.output(12, 1)

			pass_pos = GestureRecognition.read()
			#ADDED TIMER CAPABILITY
			len_timer = SERVER_TIME
			num_intervals = 4
			if not FAILED:
					timesup = check_time(len_timer, 0, num_intervals)
					start_time = time.time()
					TURN_START_TIME = start_time # Reset timer
			else:
					start_time = TURN_START_TIME # Retain timer from last pass
			while pass_pos=="X" and timesup == False:
					timesup = check_time(len_timer, time.time() - start_time, num_intervals)
					if timesup:
							sys.exit()
					else:
							pass_pos = GestureRecognition.read()

			
			position = ""
			if pass_pos == "R" or pass_pos == "r":
				position = "RIGHT"
			elif pass_pos == "L" or pass_pos == "l":
				position = "LEFT"
			elif pass_pos == "A" or pass_pos == "a":
				position = "ACROSS"
			
			# Passing payload with client id, keyword, and position to pass to
			send_data = send_data.join([MY_ID,"PASS_POTATO",position])
			publish.single(send_path, send_data, hostname = MQTT_SERVER)
			print("Passing potato or time is up!")
			if not timesup:
				# LIGHTING SCHEME FOR NO POTATO
				LED.no_potato_lights(pixels)
				# TURN VIBRATION MOTOR OFF
				GPIO.output(12, 0)
			HAVE_POTATO = False

	except IOError:
		pass

	except KeyboardInterrupt:

		print("disconnected")
		LED.eliminated_lights(pixels)
		GPIO.output(12, 0)
		client_sock.close()
		server_sock.close()
		print("all done")

		break
