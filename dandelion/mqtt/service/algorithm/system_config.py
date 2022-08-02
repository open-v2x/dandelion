import json

from dandelion.mqtt import server


def notice():
    topic = "V2X/CONFIG/UPDATE/NOTICE"
    client = server.GET_MQTT_CLIENT()
    client.publish(topic=topic, payload=json.dumps({}), qos=0)
