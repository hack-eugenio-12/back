import paho.mqtt.client as mqtt
import ssl
import json

# Criar configuracao de acordo com cada Device - 003
ca_cert = 'CAcertificate_001.cert'
device_cert = 'cert.pem'
device_key = 'key.pem'
device_id = 'c7f78c4c-b27b-4164-aefe-b5b9d6486bf5'
username = 'logicalis-eugeniostg-iothub.azure-devices.net/' + device_id + '/api-version=2017-06-30'
password = None

# Criando o client MQTT
print ("Starting connection - Creating Client")
client = mqtt.Client(device_id, mqtt.MQTTv311)
client.username_pw_set(username, password)
client.tls_set(ca_certs=ca_cert, certfile=device_cert, keyfile=device_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
client.tls_insecure_set(False)

# Conectando
print("Connect to broker")
broker_mqtt_hostname = 'logicalis-eugeniostg-iothub.azure-devices.net'
broker_mqtt_port = 8883

# Subscrevendo
print ("Subscribing")
print ("")

cloud_to_device_topic = 'logicalis-eugeniostg-iothub.azure-devices.ne/methods/POST/#'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(cloud_to_device_topic)

def my_command(cmd = None):
    200, "{}"

#def publish(message="{}", status=200, rid=None, publish):
    
#    direct_method_reply_topic = "logicalis-eugeniostg-iothub.azure-devices.ne/methods/res/{status}/?$rid={request id}"
#    topic = direct_method_reply_topic.format(status=status, request_id=rid)
#    print(topic)
#    publish(topic, message)

def on_message(client, userdata, msg):
    print("User: ")
    print(client)
    print(userdata)
    print("Data: ")
    print(msg)
    print(msg.topic)
    print(str(msg.payload))
   
    cmd = msg.topic.split('/')[3]
    rid = msg.topic.split('/')[4].split('=')[1]
    print(cmd)
    print(rid)

    # call any method do process the command
    #status, reply = my_command(cmd)

    #publish(reply, status, rid, client.publish)

client.connect(broker_mqtt_hostname, broker_mqtt_port)

client.subscribe(cloud_to_device_topic)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

