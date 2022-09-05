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
from dandelion.mqtt.topic.v2x_rsu import V2X_RSU_MAP_DOWN, v2x_rsu_map_down

LOG: LoggerAdapter = log.getLogger(__name__)


def map_down(
    id: str, map_slice: str, map_: Dict[str, Any], e_tag: str, rsu_esn: Optional[str] = None
) -> None:
    data = dict(mapSlice=map_slice, map=map_, eTag=e_tag, ack=False, seqNum=f"{id}")
    topic = V2X_RSU_MAP_DOWN
    if rsu_esn is not None:
        topic = v2x_rsu_map_down(rsu_esn)
    client = server.GET_MQTT_CLIENT()
    client.publish(topic=topic, payload=json.dumps(data), qos=0)


class MapDownACKRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()

        _id = int(data.get("seqNum", 0))
        if _id > 0:
            map_rsu = crud.map_rsu.get(db, id=_id)
            if map_rsu:
                status = 1
                if int(data.get("errorCode", -1)) != 0:
                    status = 2
                crud.map_rsu.update_status_by_id(db, id=_id, status=status)
        LOG.info(f"{topic} => Map DOWN ACK [id: {_id}] created")
