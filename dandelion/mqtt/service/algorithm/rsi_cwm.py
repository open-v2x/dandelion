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


class RSICWMRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()

        for content in data.get("content", []):
            cwm = schemas.RSICWMCreate()
            cwm.sensor_pos = data.get("sensorPos", {})
            cwm.event_type = content.get("eventType", 0)
            cwm.collision_type = content.get("collisionType", 0)
            cwm.sec_mark = content.get("secMark", 0)
            ego = content.get("egoInfo", {})
            other = content.get("otherInfo", {})

            cwm.ego_id = ego.get("egoId", 0)
            cwm.ego_pos = ego.get("egoPos", {})
            cwm.ego_heading = ego.get("heading", 0)
            cwm.ego_kinematics_info = ego.get("kinematicsInfo", {})
            cwm.ego_radius = ego.get("size", {}).get("radius", 0.0)
            cwm.ego_length = ego.get("size", {}).get("length", 0.0)
            cwm.ego_width = ego.get("size", {}).get("width", 0.0)

            cwm.other_id = other.get("otherId", 0)
            cwm.other_pos = other.get("otherPos", {})
            cwm.other_heading = other.get("heading", 0)
            cwm.other_radius = other.get("size", {}).get("radius", 0.0)
            cwm.other_length = other.get("size", {}).get("length", 0.0)
            cwm.other_width = other.get("size", {}).get("width", 0.0)
            cwm.other_kinematics_info = other.get("kinematicsInfo", {})

            crud.rsi_cwm.create(db, obj_in=cwm)

        LOG.info(f"{topic} => RSI CWM created")
