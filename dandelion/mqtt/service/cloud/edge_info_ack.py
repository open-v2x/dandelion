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
from logging import LoggerAdapter
from typing import Any, Dict, List

import paho.mqtt.client as mqtt
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud
from dandelion.db import session
from dandelion.mqtt.service import RouterHandler

LOG: LoggerAdapter = log.getLogger(__name__)


class EdgeInfoACKRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        from dandelion.mqtt.cloud_server import SET_EDGE_ID

        node_id = int(data.get("id", 0))
        SET_EDGE_ID(node_id)
        db: Session = session.DB_SESSION_LOCAL()
        crud.system_config.update_node_id(db, _id=1, node_id=node_id)

        # Notification cerebrum
        client.publish(topic="V2X/CONFIG/UPDATE/NOTICE", payload=json.dumps({}), qos=0)

        _, rsus = crud.rsu.get_multi_with_total(db)
        node_rsus: List[dict] = []
        for rsu in rsus:
            node_rsu = dict(
                name=rsu.rsu_name, esn=rsu.rsu_esn, areaCode=rsu.area_code, location=rsu.location
            )
            node_rsus.append(node_rsu)

        client.publish(
            topic="V2X/EDGE/RSU/UP",
            payload=json.dumps(dict(id=node_id, rsus=node_rsus)),
            qos=0,
        )
