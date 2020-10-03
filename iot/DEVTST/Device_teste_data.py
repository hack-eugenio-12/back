import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect("mqtt.eclipse.org", 1883, 60)

topic = 'LYMTEC'

message = {
    "schema": "dados",
    "payload": {
        "status": "ON",
        "nivel": 50,
        "comando": "none",
        "deviceid": "3b774926-fe13-4710-ab40-37df41f2e90e"
    }
}

print ("Publishing Data")

client.publish(topic, json.dumps(message))
