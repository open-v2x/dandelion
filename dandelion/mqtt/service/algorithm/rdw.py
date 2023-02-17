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

from logging import LoggerAdapter
from typing import Any, Dict

import paho.mqtt.client as mqtt
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, schemas
from dandelion.db import session
from dandelion.mqtt.service import RouterHandler

LOG: LoggerAdapter = log.getLogger(__name__)


class RDWRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()

        sensor_pos = data.get("sensorPos", {})
        contents = data.get("content", [])
        for content in contents:
            rdw = schemas.OSWCreate()
            sec_mark = content.get("secMark")
            rdw.sensor_pos = sensor_pos
            ego_info = content.get("egoInfo")
            rdw.ego_id = ego_info.get("egoId")
            rdw.ego_pos = ego_info.get("egoPos")
            rdw.speed = ego_info.get("speed")
            rdw.heading = ego_info.get("heading")
            rdw.width = ego_info.get("width")
            rdw.length = ego_info.get("length")
            rdw.height = ego_info.get("height")
            rdw.sec_mark = sec_mark

            crud.osw.create(db=db, obj_in=rdw)
        LOG.info(f"{topic} => RDW created")
