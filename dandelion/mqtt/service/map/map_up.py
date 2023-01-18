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

import re
from logging import LoggerAdapter
from typing import Any, Dict

import paho.mqtt.client as mqtt
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, models
from dandelion.db import session
from dandelion.mqtt.service import RouterHandler

LOG: LoggerAdapter = log.getLogger(__name__)


class MapRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()
        rsu_esn = re.findall("V2X/RSU/(.*)/MAP/UP", topic)[0]
        rsu = crud.rsu.get_by_rsu_esn(db, rsu_esn=rsu_esn)
        map_ = models.Map(
            name=rsu_esn,
            intersection_code=rsu.intersection_code,
            data=data,
            lng=rsu.location.get("lon"),
            lat=rsu.location.get("lat"),
        )
        crud.map.create(db, obj_in=map_)
        LOG.info(f"{topic} => Map [name: {map_.name}] created")
