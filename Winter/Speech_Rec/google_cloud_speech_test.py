import speech_recognition as sr

def callback(recognizer, audio):
    try:
        print(recognizer.recognize_google(audio))
    except sr.RequestError:
        print("There was an issue in handling the request")
    except sr.UnknownValueError:
        print("Unable to recognize speech")

r = sr.Recognizer()
r.pause_threshold = 0.1

try: 
    mic = sr.Microphone()
except(IOError):
    print("ERROR: No default microphone")

with mic as source:
    r.adjust_for_ambient_noise(source)

stop_listening = r.listen_in_background(mic, callback)