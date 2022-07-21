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


class RSUBaseINFORouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        esn = data.get("rsuEsn")
        if not esn:
            return
        base_info = schemas.RSUUpdateWithBaseInfo()
        base_info.rsu_id = data.get("rsuId")
        base_info.version = data.get("protocolVersion")
        base_info.rsu_status = data.get("rsuStatus")
        base_info.location = data.get("location")
        base_info.area_code = data.get("regionId")
        base_info.imei = data.get("imei")
        base_info.icc_id = data.get("iccid")
        base_info.communication_type = data.get("communicationType")
        base_info.running_communication_type = data.get("RunningCommunicationType")
        base_info.transprotocal = data.get("transprotocal")
        base_info.software_version = data.get("SoftwareVersion")
        base_info.hardware_version = data.get("hardwareVersion")
        base_info.depart = data.get("depart")
        db: Session = session.DB_SESSION_LOCAL()
        rsu = crud.rsu.get_by_rsu_esn(db, rsu_esn=esn)
        if rsu:
            crud.rsu.update_with_base_info(db, db_obj=rsu, obj_in=base_info)
        LOG.info(f"{topic} => Processed RSU Base Info successfully")
