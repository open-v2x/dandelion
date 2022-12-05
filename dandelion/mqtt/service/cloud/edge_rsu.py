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


class EdgeRSURouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        LOG.info(f"{topic} => Edge RSU sync {data}")
        db: Session = session.DB_SESSION_LOCAL()
        id = data.get("id")
        if id:
            crud.edge_node_rsu.remove_by_node_id(db, edge_node_id=id)
            node_rsus = data.get("rsus")
            if node_rsus:
                for node_rsu in node_rsus:
                    edge_node_rsu = schemas.EdgeNodeRSUCreate()
                    edge_node_rsu.edge_node_id = id
                    edge_node_rsu.name = node_rsu.get("name", "")
                    edge_node_rsu.esn = node_rsu.get("esn", "")
                    edge_node_rsu.intersection_code = node_rsu.get("intersectionCode", "")
                    edge_node_rsu.edge_rsu_id = node_rsu.get("edge_rsu_id")
                    location = node_rsu.get("location", {})
                    if location:
                        edge_node_rsu.location = schemas.Location()
                        edge_node_rsu.location.lon = location.get("lon", 116.40)
                        edge_node_rsu.location.lat = location.get("lat", 39.91)
                    _ = crud.edge_node_rsu.create(db, obj_in=edge_node_rsu)

        LOG.info(f"{topic} => Edge RSU synced")
