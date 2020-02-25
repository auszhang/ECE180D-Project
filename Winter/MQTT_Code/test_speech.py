# *****************************************
# Austin's test script so he doesn't have to start up an instance of a game 
# every time he wants to test multithreaded behavior :)
# *****************************************

import os
import time
from pocketsphinx import LiveSpeech, get_model_path
from threading import Thread


# Variables for speech recognition
last_phrase = "DEFAULT"
model_path = get_model_path()

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

def thread1():
    print("Executing MQTT shit")

def thread2():
    for phrase in speech:
        last_phrase = phrase
        print("PHRASE: ", last_phrase)

speech_thread = Thread(target = thread2)
speech_thread.daemon = True
speech_thread.start()

mqtt_thread = Thread(target = thread1)
mqtt_thread.daemon = True
mqtt_thread.start()




while(True):
    time.sleep(0.5)
    print("In loop")

