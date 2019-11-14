import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
MQTT_SERVER = "192.168.43.130"
#port = 1883
send_path = "topic/serene"
listen_path = "topic/init_loc"

def on_publish(client,userdata,result):
	print("LED sequence sent")
	pass

def on_connect(client, userdata, flags, rc):
	print("Connected: result code " + str(rc))
	client.subscribe(listen_path)

def on_message(client, userdata, msg):
    statement = msg.payload
    print(msg.topic + chr(11) + str(statement))
    time.sleep(5)
    client.publish(send_path, "Mode 1")
    #publish.single(send_path, "Mode 1", hostname = MQTT_SERVER)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()
