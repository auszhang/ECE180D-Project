import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import * from server_helpers
MQTT_SERVER = "192.168.43.130"
#port = 1883
send_path = "topic/serene"
listen_path = "topic/init_loc"
rec_client_strings = []
MAX_CLIENTS = 1

def on_publish(client,userdata,result):
	print("LED sequence sent")
	pass

def on_connect(client, userdata, flags, rc):
	print("Connected: result code " + str(rc))
	client.subscribe(listen_path)

def on_message(client, userdata, msg):
    statement = msg.payload
    rec_client_strings.append(statement)
    print(msg.topic + " " + str(statement))
    time.sleep(5)
    if len(rec_client_strings) == MAX_CLIENTS:
        client_data = parse_from_strings(rec_client_strings)
        grid, _ = localize_all(client_data)
        light_asgns = assign_lighting(grid)
        client.publish(send_path, light_asgns)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()
