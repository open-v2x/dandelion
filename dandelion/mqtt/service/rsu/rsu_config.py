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
from typing import Any, Dict, Optional

import paho.mqtt.client as mqtt
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud
from dandelion.db import session
from dandelion.mqtt import server
from dandelion.mqtt.service import RouterHandler
from dandelion.mqtt.topic.rsu_config import v2x_rsu_config_down, v2x_rsu_config_down_all

LOG: LoggerAdapter = log.getLogger(__name__)


def config_down(data: Dict[str, Any], rsu_esn: Optional[str] = None) -> None:
    LOG.info(f"config_down: rsu_esn={rsu_esn}, data={data}")
    topic = v2x_rsu_config_down_all()
    if rsu_esn is not None:
        topic = v2x_rsu_config_down(rsu_esn)
    client = server.GET_MQTT_CLIENT()
    client.publish(topic=topic, payload=json.dumps(data), qos=0)


class RSUConfigDownACKRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()

        _id = int(data.get("seqNum", 0))
        if _id > 0:
            config_rsu = crud.rsu_config_rsu.get(db, id=_id)
            if config_rsu:
                status = 1
                if int(data.get("errorCode", -1)) != 0:
                    status = 2
                crud.rsu_config_rsu.update_status_by_id(db, id=_id, status=status)
        LOG.info(f"{topic} => RSUConfig DOWN ACK [id: {_id}] created")
