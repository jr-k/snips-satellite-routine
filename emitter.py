#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt #import the client1
import time
import json

############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################
broker_address="192.168.9.170"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
print("Publishing message to topic","sat/volume")

payload = {
    "volume": 3,
    "siteId": "pi3sat1"
}

din=json.dumps(payload)
print din
print payload
client.publish("sat/volume",din)
client.loop_stop()
