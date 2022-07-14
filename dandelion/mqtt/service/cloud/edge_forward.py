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
from logging import LoggerAdapter
from typing import Any, Dict

import paho.mqtt.client as mqtt
from oslo_log import log

from dandelion.mqtt.service import RouterHandler

LOG: LoggerAdapter = log.getLogger(__name__)


class EdgeForwardRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        from dandelion.mqtt.cloud_server import GET_EDGE_ID

        edge_id = GET_EDGE_ID()
        LOG.info(f"{topic}")
        if edge_id > 0:
            client.publish(topic=f"{topic}/NODE{edge_id}", payload=json.dumps(data), qos=0)
            LOG.info(f"{topic}/NODE{edge_id} => forward succeeded")
