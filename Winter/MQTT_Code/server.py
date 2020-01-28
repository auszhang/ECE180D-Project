import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
from server_helpers import *
from lighting_helpers import *
MQTT_SERVER = "192.168.43.130"
#port = 1883
send_path = "topic/serene"
listen_path = "topic/init_loc"
rec_client_strings = {}
MIN_CLIENTS = 1

# Variables for tracking game state
game_grid = None
potato_row = -1
potato_col = -1

def on_publish(client,userdata,result):
	print("LED sequence sent")
	pass

def on_connect(client, userdata, flags, rc):
	print("Connected: result code " + str(rc))
	client.subscribe(listen_path)

def on_message(client, userdata, msg):
    byte_statement = msg.payload
    statement = byte_statement.decode("utf-8")
    print(msg.topic + " " + str(statement))
    if "DIED" in statement:
        dead_client = statement[:-4]
        if dead_client in rec_client_strings:
            del rec_client_strings[dead_client]
    elif "PASS_POTATO" in statement:
        new_row, new_col, valid = parse_pass(statement, game_grid, potato_row, potato_col)
        if valid:
            potato_row = new_row
            potato_col = new_col
            pass_msg = string(game_grid[potato_row][potato_col]) + ";RECEIVE"
            # Send updated potato position to clients
            client.publish(send_path, pass_msg)
    else:
        split_string = statement.split(";")
        # Map statement to client ID. This overwrites any previous statements from same client.
        rec_client_strings[split_string[4]]=statement
        time.sleep(2)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(MQTT_SERVER, 1883, 60)
client.loop_start()
while True:
    time.sleep(2)
    if len(rec_client_strings) >= MIN_CLIENTS:
        client_data = parse_from_strings_hash(rec_client_strings)
        print(client_data)
        game_grid, _ = localize_all(client_data)
