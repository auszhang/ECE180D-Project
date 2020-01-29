#CURRENTLY USING LAPTOP AS MAIN PUBLISHER, DON'T NEED THIS
import paho.mqtt.publish as publish
MQTT_SERVER = "192.168.43.130" #laptop IP
MQTT_PATH = "topic/serene"
publish.single(MQTT_PATH, "go bruins", hostname = MQTT_SERVER)

