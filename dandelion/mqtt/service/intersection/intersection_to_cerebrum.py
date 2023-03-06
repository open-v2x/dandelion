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

from oslo_log import log

from dandelion.mqtt import server as mqtt_server
from dandelion.mqtt.topic import v2x_rsu

LOG: LoggerAdapter = log.getLogger(__name__)


def intersection_publish(payload):
    if mqtt_server.MQTT_CLIENT is not None:
        payload = json.dumps(payload)
        mqtt_server.get_mqtt_client().publish(
            topic=v2x_rsu.V2X_INTERSECTION_CHANGE,
            payload=payload,
            qos=0,
        )
        LOG.info(f"publish to topic: {v2x_rsu.V2X_INTERSECTION_CHANGE},payload:{payload}")
