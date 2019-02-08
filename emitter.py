#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import json

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client = mqtt.Client("sk1")
client.on_message=on_message

client.connect("192.168.9.170", "1883")
client.loop_start()

payload = {"volume": 3, "siteId": "pi3sat1"}
jsonPayload = json.dumps(payload)
client.publish("sat/volume", jsonpayload)
client.loop_stop()
