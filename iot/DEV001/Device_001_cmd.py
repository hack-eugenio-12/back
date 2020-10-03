import paho.mqtt.client as mqtt
import ssl
import json
import time
import random

ca_cert = 'CAcertificate_001.cert'
device_cert = 'cert.pem'
device_key = 'key.pem'
device_id = 'c7f78c4c-b27b-4164-aefe-b5b9d6486bf5'
username = 'logicalis-eugeniostg-iothub.azure-devices.net/' + device_id + '/api-version=2017-06-30'
password = None

print ("Starting connection")
client = mqtt.Client(device_id, mqtt.MQTTv311)
client.username_pw_set(username, password)
client.tls_set(ca_certs=ca_cert, certfile=device_cert, keyfile=device_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
client.tls_insecure_set(False)

print("Connect to broker")

broker_mqtt_hostname = 'logicalis-eugeniostg-iothub.azure-devices.net'
broker_mqtt_port = 8883

client.connect(broker_mqtt_hostname, broker_mqtt_port)

topic = 'devices/3a5eac80-638d-474f-af48-8edc0ae88c9e/messages/devicebound/'
print ("")

for x in range(1):
    print("Passo " + str(x) + str(": Publishing Data"))

    y = random.randint(25, 30)

    message = {
        "method": "ligar",
        "payload": {
            "status": "ON",
            "nivel": y,
            "comando": "none",
            "deviceid" : "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
        }, 
        "timeout" : 10
    }
    print("Nivel: " + str(y))

    print("Sending Data")
    print("Publishing Data")

    client.connect(broker_mqtt_hostname, broker_mqtt_port)
    client.publish(topic, json.dumps(message))
    
    print("Waiting 10.0 seconds.")
    time.sleep(10.0)
    print("Done after 10.0 seconds.")
    print ("Connection closed")
    print ("")

