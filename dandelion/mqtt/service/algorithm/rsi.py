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


class RSIRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()

        rsis = data.get("rsiDatas")
        if not rsis:
            LOG.warn(f"{topic} => RSIs is None")
            return None
        rsu = crud.rsu.get_first(db)
        for rsi in rsis:
            rsi_event_in = schemas.RSIEventCreate(
                alertID=rsi.get("alertID"),
                duration=rsi.get("duration"),
                eventStatus=rsi.get("eventStatus"),
                timeStamp=rsi.get("timeStamp"),
                eventClass=rsi.get("eventClass"),
                eventType=rsi.get("eventType"),
                eventSource=rsi.get("eventSource"),
                eventConfidence=rsi.get("eventConfidence"),
                eventPosition=rsi.get("eventPosition"),
                eventRadius=rsi.get("eventRadius"),
                eventDescription=rsi.get("eventDescription"),
                eventPriority=rsi.get("eventPriority"),
                referencePaths=rsi.get("referencePaths"),
                intersectionCode=rsu.intersection_code,
            )
            crud.rsi_event.create_rsi_event(db, obj_in=rsi_event_in, rsu=rsu)
            LOG.info(f"{topic} => RSIEvent [alert_id: {rsi_event_in.alert_id}] created")
