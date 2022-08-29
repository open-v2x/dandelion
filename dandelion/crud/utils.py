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
from typing import List

from sqlalchemy.orm import Session

from dandelion import crud
from dandelion.models import MNG
from dandelion.models.mng import Reboot
from dandelion.mqtt import cloud_server as mqtt_cloud_server
from dandelion.mqtt.topic import v2x_edge


def get_mng_default() -> MNG:
    mng = MNG()
    mng.heartbeat_rate = 0
    mng.running_info_rate = 0
    mng.log_level = "NOLog"
    mng.reboot = Reboot.not_reboot
    mng.address_change = {"cssUrl": "", "time": 0}
    mng.extend_config = ""
    return mng


def refresh_cloud_rsu(db: Session):
    if mqtt_cloud_server.MQTT_CLIENT:
        _, rsus = crud.rsu.get_multi_with_total(db)
        node_rsus: List[dict] = []
        for rsu in rsus:
            node_rsu = dict(
                name=rsu.rsu_name,
                esn=rsu.rsu_esn,
                areaCode=rsu.area_code,
                location=rsu.location,
            )
            node_rsus.append(node_rsu)
        mqtt_cloud_server.MQTT_CLIENT.publish(
            topic=v2x_edge.V2X_EDGE_RSU_UP,
            payload=json.dumps(dict(id=mqtt_cloud_server.EDGE_ID, rsus=node_rsus)),
            qos=0,
        )
