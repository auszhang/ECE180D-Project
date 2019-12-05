import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
from server_helpers import *
from lighting_helpers import *
MQTT_SERVER = "192.168.43.130"
#port = 1883
send_path = "topic/serene"
listen_path = "topic/init_loc"
rec_client_strings = []
MIN_CLIENTS = 1
cycle = 0

def on_publish(client,userdata,result):
	print("LED sequence sent")
	pass

def on_connect(client, userdata, flags, rc):
	print("Connected: result code " + str(rc))
	client.subscribe(listen_path)

def on_message(client, userdata, msg):
    byte_statement = msg.payload
    statement = byte_statement.decode("utf-8")
    if "DIED" in statement:
        sst = statement.split(".")
        dead_client = sst[0]
        rec_copy = rec_client_strings.copy()
        for rec_client in rec_copy:
            if dead_client in rec_client:
                rec_client_strings.remove(rec_client)
    else:
        rec_client_strings.append(statement)
        print(msg.topic + " " + str(statement))
        time.sleep(2)

def assign_lighting(grid, cycle, num_clients):
    msg = ""
    if num_clients == 1:
        msg = steady_on(grid, cycle)
    elif num_clients = 2:
        msg = flash_slow(grid, cycle)
    elif num_clients = 3:
        msg = flash_fast(grid, cycle)
    elif num_clients == 4:
        msg = UCLA_light_scheme(grid, cycle)
    return msg

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(MQTT_SERVER, 1883, 60)
#client.loop_forever()
client.loop_start()
while True:
    time.sleep(5)
    if len(rec_client_strings) >= MIN_CLIENTS:
        client_data = parse_from_strings(rec_client_strings)
        grid, _ = localize_all(client_data)
        light_asgns = assign_lighting(grid, cycle, len(client_data))

        # client_id = 2
        # lighting = [[0,1,1], [0,0,0], [1,1,0]]
        #light_asgns = tell_lighting(client_id,lighting) #for Serene's testing
        # print(light_asgns)
        client.publish(send_path, light_asgns)
        # client.publish(send_path, "010101")
        cycle += 1
