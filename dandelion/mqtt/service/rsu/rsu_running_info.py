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

from dandelion.api.deps import get_redis_conn
from dandelion.mqtt.service import RouterHandler

LOG: LoggerAdapter = log.getLogger(__name__)


class RSURunningInfoRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        LOG.info(f"{topic} => Not implemented yet")
        redis_conn = get_redis_conn()
        rsu_esn = data.get("rsuEsn")
        info = data.get("runningInfo")
        if rsu_esn and info:
            key = f"RSU_RUNNING_INFO_{rsu_esn}"
            redis_conn.hset(key, "cpu", json.dumps(info.get("cpu", {})))
            redis_conn.hset(key, "mem", json.dumps(info.get("mem", {})))
            redis_conn.hset(key, "disk", json.dumps(info.get("disk", {})))
            redis_conn.hset(key, "net", json.dumps(info.get("net", {})))
            redis_conn.expire(name=key, time=60 * 60 * 24)
