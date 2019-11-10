import paho.mqtt.publish as publish

MQTT_SERVER = "192.168.43.130"
#port = 1883
MQTT_PATH = "topic/serene"
def on_publish(client,userdata,result):
	print("LED sequence sent")
	pass
"""
client1 = paho.Client("control1")
client1.on_publish = on_publish
client1.connect(broker,port)
ret = client1.publish("topic/serene", "sequence 1")
"""
publish.single(MQTT_PATH, "1st sequence", hostname = MQTT_SERVER)
