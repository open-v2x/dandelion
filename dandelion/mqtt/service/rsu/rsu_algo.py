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
from typing import Dict

from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud
from dandelion.mqtt import cloud_server as mqtt_cloud_server, topic
from dandelion.util import get_all_algo_config

LOG: LoggerAdapter = log.getLogger(__name__)


def algo_publish(db: Session):
    if mqtt_cloud_server.MQTT_CLIENT is not None:
        redis_info: Dict = {}
        algo_in_db = crud.algo_name.get_multi_all(db=db)
        response_data = get_all_algo_config(data=algo_in_db)
        for algo in response_data.values():
            algo_name = algo.get("algo")
            redis_info[algo_name] = algo.get("inUse") if algo.get("enable") else "disable"
        payload = json.dumps({"redis_info": redis_info})
        mqtt_cloud_server.get_mqtt_client().publish(
            topic=topic.V2X_RSU_PIP_CFG,
            payload=payload,
            qos=0,
        )
        LOG.info(f"publish to topic: {topic.V2X_RSU_PIP_CFG},payload:{payload}")
