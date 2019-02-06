#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import paho.mqtt.client as paho
import time
import alsaaudio
import json

siteId = "pi3sat1"
MQTT_IP_ADDR = "192.168.9.170"
MQTT_PORT = 1883

def on_sat_volume(volume):
    print("volume " + str(volume))
    if volume < 0:
        volume = 0

    if volume > 10:
        volume = 10

    mixer = alsaaudio.Mixer("PCM")
    mixer.setvolume(10*volume)

def on_message(client, userdata, message):
    topic = message.topic
    msg=str(message.payload.decode("utf-8","ignore"))
    msgJson=json.loads(msg)

    if "siteId" in msgJson:
        if msgJson["siteId"] != siteId:
            return

    print "[Topic]: " + str(topic)
    print "[Payload]: " + msg

    if topic == "sat/volume":
        on_sat_volume(volume=msgJson["volume"])

#def on_connect(a,b,c,f):
#    print("connected")

#def on_log(client, userdata, level, buf):
#    print("log: ",buf)


tmpClient = paho.Client("tmp_"+siteId)
tmpClient.on_message=on_message
#tmpClient.on_connect=on_connect
#tmpClient.on_log=on_log
tmpClient.connect(MQTT_IP_ADDR, MQTT_PORT)
tmpClient.subscribe("sat/volume")
tmpClient.loop_forever()
