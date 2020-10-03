#!/usr/bin/env python
# coding: utf-8
"""
####################################################################
## Simple Mqtt Client Code for connecting to Eugenio.io IoT platform
####################################################################
##
##################################################
## Author: Artur Sarlo
## Copyright:
## License:
## Version: 0.0.0
## Maintainer: Artur Sarlo
## Email: artur.sarlo@la.logicalis.com
## Status: demo
##################################################
"""

import logging
import paho.mqtt.client as mqtt
import ssl
from json import loads, dumps
from time import sleep


class MqttController(object):
    """This class wraps a mqtt client and defines how to handle messages received by the mqtt broker"""
    def __init__(self, broker_mqtt_hostname, broker_mqtt_port):
        """Class constructor

        Args:
            broker_mqtt_hostname: Mqtt broker hostname (usually informed at device registration moment)
            broker_mqtt_port: Mqtt broker port (usually informed at device registration moment)

        """
        self.paho_client_mqtt = None
        self.flag_connected = False

        # Logger related
        self.logger_path = "logger.txt"
        logging.basicConfig(filename=self.logger_path, level=logging.DEBUG)

        # Broker related
        self.broker_mqtt_hostname = broker_mqtt_hostname
        self.broker_mqtt_port = broker_mqtt_port
        self.broker_mqtt_protocol = mqtt.MQTTv311

        #########################################################################################
        # CHANGE HERE
        #########################################################################################
        self.broker_mqtt_CACert = "CAcertificate_001.cert"

        # Device related
        self.device_id = "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
        self.client_id = "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
        self.device_cert = "cert.pem"
        self.device_key = "key.pem"

        print ("Passo 1")

        #########################################################################################
        #########################################################################################

        self.username = self.broker_mqtt_hostname + '/' + self.device_id + '/api-version=2019-03-30'

        # Mqtt topics
        self.device_to_cloud_topic = 'devices/' + self.device_id + '/messages/events/'
        self.cloud_to_device_topic = 'devices/' + self.device_id + '/messages/devicebound/'
        self.invoke_base_topic = '$iothub/methods/POST/'
        self.invoke_topic = self.invoke_base_topic + '#'
        self.invoke_reply_topic = '$iothub/methods/res/{status_code}/?$rid={rid}'

        print ("Passo 2")
        self.__init_mqtt()

    def __init_mqtt(self):
        """Responsible for configuring the internal mqtt client"""

        print ("Passo 3")
        def on_connect(client, userdata, flags, rc):
            print ("Passo 4")
            """Callback for when the connection is established with the mqtt broker"""
            try:
                logging.info('MQTT Paho Connected with result code ' + str(rc))
                self.flag_connected = True
                logging.info('Subscribing to invoke topic')
                client.subscribe(self.invoke_topic)

            except Exception as e:
                logging.warning("on_connect with result error %s" % e)

        def on_message(client, userdata, msg):
            print ("Passo 5")
            """Callback for when a message is received by client"""
            logging.info('MQTT message arrived')
            logging.debug('topic %s' % msg.topic)
            logging.debug('payload %s' % msg.payload)
            self.handle_mqtt_messages(msg.topic, msg.payload)

        def on_disconnect(client, userdata, rc):
            print ("Passo 6")
            """Callback for when the connection is lost"""
            self.flag_connected = False
            logging.info('MQTT Disconnected!!')

        print ("Passo 7")
        self.paho_client_mqtt = mqtt.Client(client_id=self.device_id, protocol=self.broker_mqtt_protocol)
        self.paho_client_mqtt.on_connect = on_connect
        self.paho_client_mqtt.on_message = on_message
        self.paho_client_mqtt.on_disconnect = on_disconnect
        self.paho_client_mqtt.username_pw_set(username=self.username)
        self.paho_client_mqtt.tls_set(ca_certs=self.broker_mqtt_CACert,
                                      certfile=self.device_cert,
                                      keyfile=self.device_key,
                                      cert_reqs=ssl.CERT_REQUIRED,
                                      tls_version=ssl.PROTOCOL_TLSv1,
                                      ciphers=None)
        self.paho_client_mqtt.tls_insecure_set(False)

    def __mqtt_connect(self):
        print ("Passo 8")
        """Connects the mqtt client to the mqtt broker"""
        retry = 1
        while True:
            try:
                logging.debug('MQTT Connect... ' + str(retry))
                self.paho_client_mqtt.connect(host=str(self.broker_mqtt_hostname),
                                              port=int(self.broker_mqtt_port))
                break
            except Exception as e:
                logging.error('MQTT Connect error: %s' % e)
                if retry > 3:
                    logging.debug('MQTT Connection FAIL ' + str(retry))
                    break
                retry += 1

    def mqtt_start(self):
        print ("Passo 9")
        """Starts the mqtt connection"""
        if self.flag_connected:
            self.paho_client_mqtt.loop_start()
        else:
            self.__mqtt_connect()
            self.paho_client_mqtt.loop_start()

    def mqtt_stop(self):
        print ("Passo 10")
        """Stops the mqtt connection"""
        try:
            self.paho_client_mqtt.loop_stop()
        except Exception as e:
            logging.error('Failed to stop mqtt: %s' % e)

    def mqtt_publish(self, payload):
        print ("Passo 11")
        """Publishes a mqtt message at the default event topic for this device

        Args:
            payload: Message payload

        Returns:

        """
        if self.flag_connected:
            logging.debug(payload)
            return self.paho_client_mqtt.publish(self.device_to_cloud_topic, payload)
        else:
            logging.info('MQTT Disconnected')
            self.mqtt_start()
            return None

    def mqtt_publish_with_topic(self, topic, payload):
        print ("Passo 12")

        """Publishes a mqtt message at a passed topic

        Args:
            topic: Message topic
            payload: Message Payload

        """
        logging.debug(topic)
        logging.debug(payload)
        self.paho_client_mqtt.publish(topic, payload)

    def mqtt_is_connected(self):
        print ("Passo 13")
        """Returns the connection flag"""
        return self.flag_connected

    def handle_mqtt_messages(self, topic, payload):

        print ("Passo 14")
        """This is where the job is done. This method will parse and execute different commands based on the content of
        the mqtt message.

        Args:
            topic: Message topic
            payload: Message payload

        """
        print (payload)

        logging.debug('handle_mqtt_messages')
        # handle messages from invoke topic
        if topic.startswith(self.invoke_base_topic):
            rid = topic.split('?$rid=')[1]
            method = topic.split('$iothub/methods/POST/')[1].split('/')[0]
            logging.debug('Rid: %s' % rid)
            logging.debug('Method: %s' % method)
            print (method)
            try:
                if method == 'ping':
                    decoded_payload = self.__decode_payload_as_non_compressed_json(payload)
                    logging.info("Received ping: {}".format(decoded_payload))
                    self.invoke_reply(200, rid, dumps({}))
                if method == 'reboot':
                    decoded_payload = self.__decode_payload_as_non_compressed_json(payload)
                    logging.info("Received reboot: {}".format(decoded_payload))
                    self.invoke_reply(200, rid, dumps({}))
                if method == 'get_system_log':
                    decoded_payload = self.__decode_payload_as_non_compressed_json(payload)
                    logging.info("Received system log: {}".format(decoded_payload))
                    self.invoke_reply(200, rid, dumps({}))
                if method == 'get_eugenio_edge_log':
                    decoded_payload = self.__decode_payload_as_non_compressed_json(payload)
                    logging.info("Received eugenio log: {}".format(decoded_payload))
                    self.invoke_reply(200, rid, dumps({}))    
                if method == 'ligar':
                    decoded_payload = self.__decode_payload_as_non_compressed_json(payload)
                    logging.info("Received ligar: {}".format(decoded_payload))
                    self.invoke_reply(200, rid, dumps({"status" : "ligado"}))
                if method == 'testar':
                    decoded_payload = self.__decode_payload_as_non_compressed_json(payload)
                    logging.info("Received testar: {}".format(decoded_payload))
                    self.invoke_reply(200, rid, dumps({"status" : "ok"}))
                if method == 'chamar':
                    decoded_payload = self.__decode_payload_as_non_compressed_json(payload)
                    logging.info("Received chamar: {}".format(decoded_payload))
                    self.invoke_reply(200, rid, dumps({"status" : "chamando"}))
                if method == 'provar':
                    decoded_payload = self.__decode_payload_as_non_compressed_json(payload)
                    logging.info("Received provar: {}".format(decoded_payload))
                    self.invoke_reply(200, rid, dumps({"status" : "provando"}))
                if method == 'localizar':
                    decoded_payload = self.__decode_payload_as_non_compressed_json(payload)
                    logging.info("Received localizar: {}".format(decoded_payload))
                    self.invoke_reply(200, rid, dumps({"status" : "localizando"}))
                if method == 'comprar':
                    decoded_payload = self.__decode_payload_as_non_compressed_json(payload)
                    logging.info("Received comprar: {}".format(decoded_payload))
                    self.invoke_reply(200, rid, dumps({"status" : "comprando"}))

  
            except Exception as e:
                logging.error('Failed to run command: %s' % e)
                resp = {'message': e}
                self.invoke_reply(500, rid, dumps(resp))

    def __decode_payload_as_non_compressed_json(self, payload):
        print ("Passo 15")
        """Transforms the payload (assuming it contains a non compressed json) from bytes object to dict object

        Args:
            payload (bytes): Json payload as bytes object

        Returns:
            dict: Json payload converted to a dict

        """
        payload_as_json_string = payload.decode()
        payload_as_json_dict = loads(payload_as_json_string)
        logging.debug('Payload: %s' % payload_as_json_dict)
        return payload_as_json_dict

    def invoke_reply(self, status_code, rid, payload):
        print ("Passo 16")
        """Method used to publish the result of a previously received command

        Args:
            status_code (int): REST like status code
            rid (): Request Id used to identify witch request this response relates with
            payload (str): Message Payload


        """
        logging.debug('Invoke reply')
        topic = self.invoke_reply_topic
        topic = topic.replace('{status_code}', str(status_code))
        topic = topic.replace('{rid}', str(rid))
        logging.debug('Invoke reply topic: %s' % topic)
        logging.debug('Invoke reply message: %s' % payload)
        self.mqtt_publish_with_topic(topic, payload)


if __name__ == '__main__':
    print ("Passo 0")
    my_mqtt_controller = MqttController("logicalis-eugeniostg-iothub.azure-devices.net", 8883)
    my_mqtt_controller.mqtt_start()
    while True:
        sleep(10)
