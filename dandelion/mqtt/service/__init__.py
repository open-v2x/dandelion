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

LOG: LoggerAdapter = log.getLogger(__name__)


class RouterHandler(object):
    def request(
        self, _client: mqtt.MQTT_CLIENT, _user_data: Dict[str, Any], _msg: mqtt.MQTTMessage
    ) -> None:
        try:
            topic_ = _msg.topic
            msg_ = _msg.payload.decode("utf-8")
            LOG.info(f"{topic_} => {msg_}")
            data_ = json.loads(msg_)
            self.handler(_client, topic_, data_)
        except Exception as ex:
            LOG.error(ex)

    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        """"""
