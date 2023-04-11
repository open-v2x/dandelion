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
import re
from datetime import datetime
from logging import LoggerAdapter
from typing import Any, Dict

import paho.mqtt.client as mqtt
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud
from dandelion.db import session
from dandelion.mqtt import server as mqtt_server, topic
from dandelion.mqtt.service import RouterHandler

LOG: LoggerAdapter = log.getLogger(__name__)


def spat_publish(spat_in_db):
    if mqtt_server.MQTT_CLIENT is not None:
        payload = json.dumps(
            dict(
                name=spat_in_db.name,
                intersections=[
                    dict(
                        intersectionId=spat_in_db.intersection_id,
                        status=spat_in_db.online_status,
                        phases=[
                            dict(
                                phaseId=spat_in_db.phase_id,
                                phaseStates=dict(
                                    light=spat_in_db.light,
                                    timing=spat_in_db.timing.strftime("%Y-%m-%d %H:%M:%S"),
                                ),
                            )
                        ],
                    )
                ],
            )
        )
        mqtt_server.get_mqtt_client().publish(
            topic=topic.RSU_SPAT_DOWN,
            payload=payload,
            qos=0,
        )
        LOG.info(f"publish to topic: {topic.RSU_SPAT_DOWN},payload:{payload}")


class RSUSpatHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()
        intersections_list: list = data["intersections"]
        for intersections in intersections_list:
            intersection_id = intersections.get("intersectionId")
            online_status = intersections.get("status")
            for phases in intersections.get("phases"):
                phase_id = phases.get("phaseId")
                spat_in_db = crud.spat.filter(db, intersection_id, phase_id)
                rsu_id = int(re.findall("V2X/RSU/(\\d+)/SPAT/UP", "V2X/RSU/1/SPAT/UP")[0])
                spat_in = {
                    "intersection_id": intersection_id,
                    "online_status": online_status,
                    "phase_id": phase_id,
                    "light": phases.get("phaseStates").get("light"),
                    "timing": datetime.strptime(
                        phases.get("phaseStates").get("timing"), "%Y-%m-%d %H:%M:%S"
                    ),
                    "rsu_id": rsu_id,
                }
                if spat_in_db:
                    crud.spat.update(db, db_obj=spat_in_db, obj_in=spat_in)
                    LOG.info(f"{topic} => update spat successfully")
                else:
                    crud.spat.create(db, obj_in=spat_in)
                    LOG.info(f"{topic} => create spat successfully")
