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
import uuid
from logging import LoggerAdapter
from typing import Any, Callable, Dict

import paho.mqtt.client as mqtt
from oslo_config import cfg
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import conf, crud
from dandelion.mqtt.service import RouterHandler

# from dandelion.mqtt.service.cloud.edge_forward import EdgeForwardRouterHandler
from dandelion.mqtt.service.cloud.edge_hb import EdgeHBRouterHandler
from dandelion.mqtt.service.cloud.edge_info import EdgeInfoRouterHandler
from dandelion.mqtt.service.cloud.edge_info_ack import EdgeInfoACKRouterHandler
from dandelion.mqtt.service.cloud.edge_rsu import EdgeRSURouterHandler

LOG: LoggerAdapter = log.getLogger(__name__)
CONF: cfg = conf.CONF

topic_router: Dict[str, RouterHandler] = {
    "V2X/EDGE/INFO/UP": EdgeInfoRouterHandler(),
    "V2X/EDGE/HB/UP": EdgeHBRouterHandler(),
    "V2X/EDGE/RSU/UP": EdgeRSURouterHandler(),
    # "V2X/DEVICE/+/PARTICIPANT": EdgeForwardRouterHandler(),
    # "V2X/DEVICE/+/APPLICATION/CW": EdgeForwardRouterHandler(),
    # "V2X/DEVICE/+/APPLICATION/CLC": EdgeForwardRouterHandler(),
    # "V2X/DEVICE/+/APPLICATION/DNP": EdgeForwardRouterHandler(),
    # "V2X/DEVICE/+/APPLICATION/SDS": EdgeForwardRouterHandler(),
}
MQTT_CLIENT: mqtt.Client = None
GET_MQTT_CLIENT: Callable[[], mqtt.Client]
EDGE_ID: int = 0
SET_EDGE_ID: Callable[[int], None]
GET_EDGE_ID: Callable[[], int]
EDGE_NAME: str = ""


def _get_mqtt() -> mqtt.Client:
    global MQTT_CLIENT
    if MQTT_CLIENT is None:
        raise SystemError("Cloud MQTT Client is none")
    return MQTT_CLIENT


def _set_edge_id(edge_id) -> None:
    global EDGE_ID
    EDGE_ID = edge_id


def _get_edge_id() -> int:
    global EDGE_ID
    return EDGE_ID


def _on_connect(client: mqtt.Client, userdata: Any, flags: Any, rc: int) -> None:
    if rc != 0:
        raise SystemError("Cloud MQTT Connection failed")
    LOG.info("Cloud MQTT Connection succeeded")

    global MQTT_CLIENT
    MQTT_CLIENT = client

    global GET_MQTT_CLIENT
    GET_MQTT_CLIENT = _get_mqtt

    global SET_EDGE_ID
    SET_EDGE_ID = _set_edge_id

    global GET_EDGE_ID
    GET_EDGE_ID = _get_edge_id

    for route in topic_router:
        client.message_callback_add(route, topic_router[route].request)
        client.subscribe(topic=route, qos=0)

    key = uuid.uuid4().hex

    client.message_callback_add(f"V2X/EDGE/{key}/INFO/UP/ACK", EdgeInfoACKRouterHandler().request)
    client.subscribe(topic=f"V2X/EDGE/{key}/INFO/UP/ACK", qos=0)
    client.publish(
        topic="V2X/EDGE/INFO/UP", payload=json.dumps(dict(key=key, name=EDGE_NAME)), qos=0
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
