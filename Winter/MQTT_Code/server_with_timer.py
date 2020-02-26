import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import os
from pocketsphinx import LiveSpeech, get_model_path
from server_helpers import *
from lighting_helpers import *
from threading import Thread
MQTT_SERVER = "192.168.43.130"
#port = 1883
send_path = "topic/serene"
listen_path = "topic/init_loc"
rec_client_strings = {}
MIN_CLIENTS = 2 #Change to 4

# Variables for tracking game state
game_grid = None
name_grid = None
potato_row = -1
potato_col = -1
prev_row = -1
prev_col = -1
failed_pass = False
fail_msg = ""
game_start = False
client_to_notify = ""
MAX_TIME = 8 # Max timer duration
MIN_TIME = 2 # Min timer duration
curr_time = MAX_TIME # Current timer duration

# Variables for speech recognition
model_path = get_model_path()
last_phrase = "x"

# LiveSpeech parameters
speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=1024,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'en-us'),
    lm=os.path.join(model_path, 'en-us.lm.bin'),
    #dic=os.path.join(model_path, 'cmudict-en-us.dict')
    dic='words.dic'
)

def on_publish(client,userdata,result):
	#print("published")
	pass

def on_connect(client, userdata, flags, rc):
	print("Connected: result code " + str(rc))
	client.subscribe(listen_path)

def on_message(client, userdata, msg):
    byte_statement = msg.payload
    statement = byte_statement.decode("utf-8")
    print(msg.topic + " " + str(statement))
    global potato_row
    global potato_col
    global failed_pass
    global fail_msg
    global game_grid
    global prev_row
    global prev_col
    global curr_intervals
    if "DIED" in statement:
        dead_client = statement[:-4]
        if dead_client in rec_client_strings:
            del rec_client_strings[dead_client]
            game_grid, potato_lost = remove_player(dead_client,game_grid, potato_row, potato_col)
            if potato_lost:
                failed_pass = False
                potato_row, potato_col = get_random_pos(game_grid)
                prev_row = -1
                prev_col = -1
                curr_intervals = MAX_TIME
    elif "PASS_POTATO" in statement:
        new_row, new_col, valid = parse_pass(statement, game_grid, potato_row, potato_col)
        data = parse_from_string(statement)
        direction = data[2]
        if direction != last_phrase.upper():
            valid = False
        if valid:
            print("valid")
            failed_pass = False
            potato_row = new_row
            potato_col = new_col
        else:
            print("not valid")
            failed_pass = True
            # Set failure message
            client_id = data[0]
            fail_msg = client_id+";FAILED_TO_PASS"
    else:
        split_string = statement.split(";")
        # Map statement to client ID. This overwrites any previous statements from same client.
        rec_client_strings[split_string[2]]=statement
        time.sleep(0.5)

def listen_speech():
    for phrase in speech:
        last_phrase = phrase
        print("PHRASE: ", last_phrase)

# Initialize speech recognition in separate thread
speech_thread = Thread(target = listen_speech)
speech_thread.daemon = True
speech_thread.start()

client = mqtt.Client() 
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect(MQTT_SERVER, 1883, 60)
client.loop_start()

while True:
    time.sleep(0.5)
    #print(rec_client_strings)
    #print(game_grid)
    if len(rec_client_strings) >= MIN_CLIENTS:
        client_data = parse_from_strings_hash(rec_client_strings)
        game_grid, name_grid = localize_all(client_data)
        if not game_start:
            # Initialize the game
            game_start = True
            potato_row = 0
            potato_col = 0
    if failed_pass:
        pass_msg = fail_msg
    elif potato_row != prev_row or potato_col != prev_col:
        pass_msg = str(game_grid[potato_row][potato_col]) + ";RECEIVE;" + str(curr_time)
        if curr_time > MIN_TIME:
            curr_time -= 1
        prev_row = potato_row
        prev_col = potato_col
    else:
        pass_msg = ""
    print(pass_msg)
    client.publish(send_path,pass_msg)
            
        
