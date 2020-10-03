from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from datetime import date
from datetime import datetime
import socket
import os

import paho.mqtt.client as mqtt
import json
from flask import request

client = mqtt.Client()

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
    status = "NA"
    status = request.args.get('status')

    client.connect("mqtt.eclipse.org", 1883, 60)

    topic = 'LYMTEC'

    message = {
    "schema": "dados",
    "payload": {
        "status": status,
        "nivel": 60,
        "comando": "none",
        "deviceid": "3b774926-fe13-4710-ab40-37df41f2e90e"
        }
    }

    print ("Publishing Data")
    client.publish(topic, json.dumps(message))
    return "Data sent"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
