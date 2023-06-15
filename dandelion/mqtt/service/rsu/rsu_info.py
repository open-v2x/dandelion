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
from dandelion.mqtt import server, topic
from dandelion.mqtt.service import RouterHandler

LOG: LoggerAdapter = log.getLogger(__name__)


def rsu_info_publish():
    server.get_mqtt_client().publish(
        topic=topic.V2X_RSU_REG_TICE,
        payload=None,
        qos=0,
    )
    LOG.info(f"publish to topic: {topic.V2X_RSU_PIP_CFG}")


class RSUInfoRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()

        rsu_esn = data.get("rsuEsn")
        if not rsu_esn:
            LOG.warn(f"{topic} => rsu_esn is None")
            return None

        rsu = crud.rsu.get_by_rsu_esn(db, rsu_esn=rsu_esn)
        if not rsu:
            LOG.info(f"{topic} => RSU not found: {rsu_esn}")
            total, _ = crud.rsu_tmp.get_multi_with_total(db, rsu_esn=rsu_esn)
            if total > 0:
                LOG.info(
                    f"{topic} => RSU Tmp [rsu_esn: {rsu_esn}] total: {total}, "
                    "ignore to create RSU Tmp"
                )
                return None
            rsu_tmp = schemas.RSUTMPCreate(**data)
            crud.rsu_tmp.create(db, obj_in=rsu_tmp)
            LOG.info(f"{topic} => RSU Tmp [rsu_esn: {rsu_esn}] created")
        else:
            rsu_in = schemas.RSUUpdateWithVersion(
                rsuId=data.get("rsuId"),
                rsuName=data.get("rsuName"),
                version=data.get("version"),
                location=data.get("location"),
                config=data.get("config"),
            )
            crud.rsu.update_with_version(db, db_obj=rsu, obj_in=rsu_in)
            LOG.info(f"{topic} => RSU [rsu_esn: {rsu_esn}] updated")
