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


class CGWRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()

        sensor_pos = data.get("sensorPos", {})
        contents = data.get("content", [])
        for content in contents:
            cgw = schemas.CGWCreate()
            cgw.sensor_pos = sensor_pos
            sec_mark = content.get("secMark")
            lane_info = content.get("congestionLanesInfo")
            cgw.cgw_level = lane_info.get("level")
            cgw.lane_id = lane_info.get("laneId")
            cgw.average_speed = lane_info.get("avgSpeed")
            cgw.start_point = lane_info.get("startPoint")
            cgw.end_point = lane_info.get("endPoint")
            cgw.sec_mark = sec_mark

            crud.cgw.create(db=db, obj_in=cgw)
        LOG.info(f"{topic} => CGW created")
