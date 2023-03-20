# Copyright 2022 99Cloud, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import json
import os
import uuid
from logging import LoggerAdapter
from typing import Any

import paho.mqtt.client as mqtt
from oslo_config import cfg
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import conf, crud
from dandelion.mqtt.service.cloud.edge_info_ack import EdgeInfoACKRouterHandler
from dandelion.mqtt.topic import v2x_edge

LOG: LoggerAdapter = log.getLogger(__name__)
CONF: cfg = conf.CONF
mode_conf = CONF.mode

MQTT_CLIENT: mqtt.Client = None
EDGE_ID: int = 0
EDGE_NAME: str = ""
AREA_CODE: str = ""


def get_mqtt_client() -> mqtt.Client:
    global MQTT_CLIENT
    if MQTT_CLIENT is None:
        raise SystemError("Cloud MQTT Client is none")
    return MQTT_CLIENT


def set_edge_id(edge_id) -> None:
    global EDGE_ID
    EDGE_ID = edge_id


def get_edge_id() -> int:
    global EDGE_ID
    return EDGE_ID


def _on_connect(client: mqtt.Client, userdata: Any, flags: Any, rc: int) -> None:
    if rc != 0:
        raise SystemError("Cloud MQTT Connection failed")
    LOG.info("Cloud MQTT Connection succeeded")

    global MQTT_CLIENT
    MQTT_CLIENT = client

    key = uuid.uuid4().hex
    subscribe_topic = v2x_edge.v2x_edge_key_info_up_ack(key)
    client.message_callback_add(subscribe_topic, EdgeInfoACKRouterHandler().request)
    client.subscribe(topic=subscribe_topic, qos=0)
    client.publish(
        topic=v2x_edge.V2X_EDGE_INFO_UP,
        payload=json.dumps(
            dict(key=key, name=EDGE_NAME, ip=os.getenv("OPENV2X_EXTERNAL_IP"), area_code=AREA_CODE)
        ),
        qos=0,
    )


def _on_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
    LOG.info(msg.payload.decode("utf-8"))


def _on_disconnect(client: mqtt.Client, userdata: Any, rc: int) -> None:
    LOG.error(f"Cloud MQTT Connection disconnected, rc: {rc}")
    global MQTT_CLIENT
    MQTT_CLIENT = None


def connect() -> None:
    from dandelion.db import session

    db: Session = session.DB_SESSION_LOCAL()
    config = crud.system_config.get(db, 1)
    if config:
        global EDGE_NAME
        EDGE_NAME = config.name
        global AREA_CODE
        AREA_CODE = config.area_code

    if config and config.mqtt_config:
        LOG.info("Starting Cloud MQTT...")
        mqtt_config = config.mqtt_config
        _client = mqtt.Client(client_id=uuid.uuid4().hex)
        _client.username_pw_set(mqtt_config.get("username"), mqtt_config.get("password"))
        _client.on_connect = _on_connect
        _client.on_message = _on_message
        _client.on_disconnect = _on_disconnect
        _client.connect(mqtt_config.get("host"), mqtt_config.get("port"), 60)
        _client.loop_start()
