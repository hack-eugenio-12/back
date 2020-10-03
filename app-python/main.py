from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from datetime import date
from datetime import datetime
import socket
import os

from flask import request

import paho.mqtt.client as mqtt
import ssl
import json
import time
import random

import requests

ca_cert = 'CAcertificate_001.cert'
device_cert = 'cert_001.pem'
device_key = 'key_001.pem'
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

topic = 'devices/c7f78c4c-b27b-4164-aefe-b5b9d6486bf5/messages/events/'
print ("")

global compras
compras = 0

@app.route('/')
def hello():
    return "Hello DevSecOps!"

@app.route('/data')
def data():
    today = date.today()
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return "{ data : " + date_time + "}"

@app.route('/server')
def server():
    return socket.gethostname()

@app.route('/status')
def status():
    return "{ status : up }"

@app.route('/version')
def version():
    return "Version 3.0"

@app.route('/eugenio')
def eugenio():
    return "Version 3.0"

@app.route('/eugenio/version')
def eugenio_version():
    return "Version 3.0"

@app.route('/eugenio/send')
def eugenio_send():

    y = random.randint(25, 30)
    message = {
        "schema": "dados",
        "payload": {
            "status": "ON",
            "nivel": y,
            "comando": "none",
            "deviceid" : "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
        }
    }
    print("Nivel: " + str(y))

    print("Sending Data")
    print("Publishing Data")

    client.connect(broker_mqtt_hostname, broker_mqtt_port)
    client.publish(topic, json.dumps(message))

    print ("Connection closed")
    print ("")

    print ("Publishing Data")
    return "Data sent"

@app.route('/eugenio/testar')
def eugenio_testar():

    payload = "{ \"method\": \"testar\",  \"payload\": \"ON\",  \"timeout\": 10 }";
    deviceId = "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
    headers = {
        'apikey': "Rv5BrH5A929jIGH5hX4HQoRDUM1CGugr",
        'content-type': "application/json"
    }
    response = requests.request("POST", 'https://portal.stg.eugenio.io/api/v1/things/'+deviceId+'/invoke', data=payload, headers=headers)

    print(response.text)
    print ("Publishing Data")
    return "Teste done"

@app.route('/eugenio/ligar')
def eugenio_ligar():

    payload = "{ \"method\": \"ligar\",  \"payload\": \"ON\",  \"timeout\": 10 }";
    deviceId = "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
    headers = {
        'apikey': "Rv5BrH5A929jIGH5hX4HQoRDUM1CGugr",
        'content-type': "application/json"
    }
    response = requests.request("POST", 'https://portal.stg.eugenio.io/api/v1/things/'+deviceId+'/invoke', data=payload, headers=headers)

    print(response.text)
    print ("Publishing Data")
    return "Ligar done"

@app.route('/eugenio/chamar')
def eugenio_chamar():

    payload = "{ \"method\": \"chamar\",  \"payload\": \"Vou chamar a consultora\",  \"timeout\": 10 }";
    deviceId = "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
    headers = {
        'apikey': "Rv5BrH5A929jIGH5hX4HQoRDUM1CGugr",
        'content-type': "application/json"
    }
    response = requests.request("POST", 'https://portal.stg.eugenio.io/api/v1/things/'+deviceId+'/invoke', data=payload, headers=headers)

    print(response.text)
    print ("Publishing Data")
    return "Chamando"


@app.route('/eugenio/provar')
def eugenio_provar():

    payload = "{ \"method\": \"provar\",  \"payload\": \"Vou mostrar nossos produtos\",  \"timeout\": 10 }";
    deviceId = "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
    headers = {
        'apikey': "Rv5BrH5A929jIGH5hX4HQoRDUM1CGugr",
        'content-type': "application/json"
    }
    response = requests.request("POST", 'https://portal.stg.eugenio.io/api/v1/things/'+deviceId+'/invoke', data=payload, headers=headers)

    print(response.text)
    print ("Publishing Data")
    return "Provando"


@app.route('/eugenio/localizar')
def eugenio_localizar():

    payload = "{ \"method\": \"localizar\",  \"payload\": \"Encontrando seu produto preferido\",  \"timeout\": 10 }";
    deviceId = "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
    headers = {
        'apikey': "Rv5BrH5A929jIGH5hX4HQoRDUM1CGugr",
        'content-type': "application/json"
    }
    response = requests.request("POST", 'https://portal.stg.eugenio.io/api/v1/things/'+deviceId+'/invoke', data=payload, headers=headers)

    print(response.text)
    print ("Publishing Data")
    return "Encontrando"

@app.route('/eugenio/comprar')
def eugenio_comprar():

    payload = "{ \"method\": \"comprar\",  \"payload\": \"Vamos fechar seu pedido\",  \"timeout\": 10 }";
    deviceId = "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
    headers = {
        'apikey': "Rv5BrH5A929jIGH5hX4HQoRDUM1CGugr",
        'content-type': "application/json"
    }
    response = requests.request("POST", 'https://portal.stg.eugenio.io/api/v1/things/'+deviceId+'/invoke', data=payload, headers=headers)
    global compras
    compras = compras + 1 
    print(response.text)
    print ("Publishing Data")
    return "Comprando " + str(compras)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    compras = 0
    app.run(host='0.0.0.0', port=port)
