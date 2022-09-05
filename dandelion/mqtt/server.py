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

import uuid
from logging import LoggerAdapter
from typing import Any, Callable, Dict

import paho.mqtt.client as mqtt
from oslo_config import cfg
from oslo_log import log

from dandelion import conf
from dandelion.mqtt.service import RouterHandler
from dandelion.mqtt.service.algorithm.rsi import RSIRouterHandler
from dandelion.mqtt.service.algorithm.rsi_dnp import RSIDNPRouterHandler
from dandelion.mqtt.service.algorithm.rsm import RSMRouterHandler
from dandelion.mqtt.service.map.map_down import MapDownACKRouterHandler
from dandelion.mqtt.service.map.map_up import MapRouterHandler
from dandelion.mqtt.service.query.rsu_query_up import RSUQueryUPRouterHandler
from dandelion.mqtt.service.rsu.rsu_base_info import RSUBaseINFORouterHandler
from dandelion.mqtt.service.rsu.rsu_config import RSUConfigDownACKRouterHandler
from dandelion.mqtt.service.rsu.rsu_heartbeat import RSUHeartbeatRouterHandler
from dandelion.mqtt.service.rsu.rsu_info import RSUInfoRouterHandler
from dandelion.mqtt.service.rsu.rsu_running_info import RSURunningInfoRouterHandler
from dandelion.mqtt.topic import v2x_rsu

LOG: LoggerAdapter = log.getLogger(__name__)
CONF: cfg = conf.CONF

topic_router: Dict[str, RouterHandler] = {
    v2x_rsu.V2X_RSU_INFO_UP: RSUInfoRouterHandler(),
    v2x_rsu.V2X_RSU_HB_UP: RSUHeartbeatRouterHandler(),
    v2x_rsu.V2X_RSU_BaseINFO_UP: RSUBaseINFORouterHandler(),
    v2x_rsu.V2X_RSU_RunningInfo_UP: RSURunningInfoRouterHandler(),
    v2x_rsu.V2X_RSU_INFOQuery_Response: RSUQueryUPRouterHandler(),
    v2x_rsu.V2X_RSU_PLUS_MAP_DOWN_ACK: MapDownACKRouterHandler(),
    v2x_rsu.V2X_RSU_PLUS_CONFIG_DOWN_ACK: RSUConfigDownACKRouterHandler(),
    v2x_rsu.V2X_RSU_PLUS_MAP_UP: MapRouterHandler(),
    v2x_rsu.V2X_RSU_PLUS_RSM_DOWN: RSMRouterHandler(),
    v2x_rsu.V2X_RSU_PLUS_RSI_DOWN: RSIRouterHandler(),
    v2x_rsu.V2X_RSU_PLUS_DNP_DOWN: RSIDNPRouterHandler(),
}
MQTT_CLIENT: mqtt.Client = None
GET_MQTT_CLIENT: Callable[[], mqtt.Client]


def _get_mqtt() -> mqtt.Client:
    global MQTT_CLIENT
    if MQTT_CLIENT is None:
        raise SystemError("MQTT Client is none")
    return MQTT_CLIENT


def _on_connect(client: mqtt.Client, userdata: Any, flags: Any, rc: int) -> None:
    if rc != 0:
        raise SystemError("MQTT Connection failed")
    LOG.info("MQTT Connection succeeded")

    global MQTT_CLIENT
    MQTT_CLIENT = client

    global GET_MQTT_CLIENT
    GET_MQTT_CLIENT = _get_mqtt

    for route in topic_router:
        client.message_callback_add(route, topic_router[route].request)
        client.subscribe(topic=route, qos=0)


def _on_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
    LOG.info(msg.payload.decode("utf-8"))


def _on_disconnect(client: mqtt.Client, userdata: Any, rc: int) -> None:
    LOG.error(f"MQTT Connection disconnected, rc: {rc}")


def connect() -> None:
    mqtt_conf = CONF.mqtt

    _client = mqtt.Client(client_id=uuid.uuid4().hex)
    _client.username_pw_set(mqtt_conf.username, mqtt_conf.password)
    _client.on_connect = _on_connect
    _client.on_message = _on_message
    _client.on_disconnect = _on_disconnect
    _client.connect(mqtt_conf.host, mqtt_conf.port, 60)
    _client.loop_start()
