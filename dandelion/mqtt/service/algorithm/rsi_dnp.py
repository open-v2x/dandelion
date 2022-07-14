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


class RSIDNPRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()

        dnp = schemas.RSIDNPCreate()

        dnp.msg_id = data.get("id")
        if not dnp.msg_id:
            LOG.info(f"{topic} => RSI DNP has no id")
            return None
        dnp.sec_mark = data.get("secMark", 0)
        dnp.ref_pos = data.get("refPos", {})
        coordinates = data.get("coordinates")
        if coordinates:
            dnp.veh_id = coordinates.get("vehId", "0")
            dnp.drive_suggestion = coordinates.get("driveSuggestion", {})
            dnp.path_guidance = coordinates.get("pathGuidance", [])
            dnp.info = coordinates.get("info", 0)

        crud.rsi_dnp.create(db, obj_in=dnp)
        LOG.info(f"{topic} => RSI DNP created")
