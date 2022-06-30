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
from typing import Any, Dict, List

import paho.mqtt.client as mqtt
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.db import session
from dandelion.mqtt.service import RouterHandler
from dandelion.util import Optional as Optional_util

LOG: LoggerAdapter = log.getLogger(__name__)


class RSMRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()

        rsms = Optional_util.none(data.get("content")).map(lambda v: v.get("rsms")).get()
        for rsm_ in rsms:
            rsm = schemas.RSMCreate(refPos=rsm_.get("refPos"))

            ps = rsm_.get("participants")
            if not ps:
                LOG.info(f"{topic} => RSM has no participants")
                return None
            participants: List[models.Participants] = []
            for p_ in ps:
                p = models.Participants()
                p.ptc_id = p_.get("ptcId")
                p.ptc_type = p_.get("ptcType")
                p.source = p_.get("source")
                p.sec_mark = p_.get("secMark")
                p.pos = p_.get("pos")
                p.accuracy = p_.get("accuracy")
                p.speed = p_.get("speed")
                p.heading = p_.get("heading")
                p.size = p_.get("size", {})
                participants.append(p)
            crud.rsm.create_rsm(db, obj_in=rsm, participants=participants)
            LOG.info(f"{topic} => RSM created")
