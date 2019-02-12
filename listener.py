#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import paho.mqtt.client as paho
import time
import alsaaudio
import json
import pytoml
import os
import vlc

#time.sleep(1)

SNIPS_CONFIG_PATH = '/etc/snips.toml'
siteId = 'default'
mqttServer = '127.0.0.1'
mqttPort = 1883


def loadConfigs():
	global mqttServer, mqttPort, siteId, hotwordId

	if os.path.isfile(SNIPS_CONFIG_PATH):
		with open(SNIPS_CONFIG_PATH) as confFile:
			configs = pytoml.load(confFile)
			if 'mqtt' in configs['snips-common']:
				if ':' in configs['snips-common']['mqtt']:
					mqttServer = configs['snips-common']['mqtt'].split(':')[0]
					mqttPort = int(configs['snips-common']['mqtt'].split(':')[1])
				elif '@' in configs['snips-common']['mqtt']:
					mqttServer = configs['snips-common']['mqtt'].split('@')[0]
					mqttPort = int(configs['snips-common']['mqtt'].split('@')[1])
			if 'bind' in configs['snips-audio-server']:
				if ':' in configs['snips-audio-server']['bind']:
					siteId = configs['snips-audio-server']['bind'].split(':')[0]
				elif '@' in configs['snips-audio-server']['bind']:
					siteId = configs['snips-audio-server']['bind'].split('@')[0]
			if 'hotword_id' in configs['snips-hotword']:
				hotwordId = configs['snips-hotword']['hotword_id']
	else:
		print('Snips configs not found')

def on_sat_volume(volume):
    print("volume " + str(volume))

    if volume == 0:
        volume = 0
    elif volume == 1:
        volume = 44
    elif volume == 2:
        volume = 60
    elif volume == 3:
        volume = 71
    elif volume == 4:
        volume = 78
    elif volume == 5:
        volume = 85
    elif volume == 6:
        volume = 88
    elif volume == 7:
        volume = 91
    elif volume == 8:
        volume = 95
    elif volume == 9:
        volume = 98
    elif volume == 10:
        volume = 100

    mixer = alsaaudio.Mixer("PCM")
    mixer.setvolume(volume)


instance = None
player = None

def on_hotword():
    if player != None:
        vol = player.audio_get_volume()
        player.audio_set_volume(30)
        time.sleep(4)
        player.audio_set_volume(vol)

def on_media_play(media, port):
    global instance, player
    instance = vlc.Instance('--no-video', '-A alsa,none-alsa-audio-device default')
    player = instance.media_player_new()
    resource = 'http://'+mqttServer+':'+str(port)+'/'+media
    print "Trying to play resource : " + resource
    media = instance.media_new(resource)
    player.set_media(media)
    player.play()
    player.audio_set_volume(100)

def on_stop():
    global player

    if player != None:
        player.stop()

def on_message(client, userdata, message):
    topic = message.topic
    msg=str(message.payload.decode("utf-8","ignore"))
    msgJson=json.loads(msg)

    if "siteId" in msgJson:
        if msgJson["siteId"] != siteId:
            return

    print "[Topic]: " + str(topic)
    print "[Payload]: " + msg

    if topic == "hermes/artifice/volume/set":
        on_sat_volume(volume=msgJson["volume"])
    elif topic == "hermes/artifice/media/audio/play":
        on_media_play(media=msgJson["media"], port=msgJson["port"])
    elif topic == "hermes/artifice/stop":
        on_stop()
    elif topic == "hermes/hotword/default/detected":
        on_hotword()

def on_connect(client, userdata, flag, rc):
    print("connected")
    print(rc)

def on_disconnected(client, userdata, rc):
    print("disconnected")

def on_log(client, userdata, level, buf):
    print("log: ",buf)

loadConfigs()
tmpClient = paho.Client("tmp_"+siteId)
tmpClient.on_message=on_message
# tmpClient.on_connect=on_connect
# tmpClient.on_log=on_log
tmpClient.connect(mqttServer, mqttPort)
tmpClient.subscribe("hermes/hotword/default/detected")
tmpClient.subscribe("hermes/artifice/volume/set")
tmpClient.subscribe("hermes/artifice/media/audio/play")
tmpClient.subscribe("hermes/artifice/stop")
tmpClient.loop_forever()
