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


class EdgeRSULocationRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        LOG.info(f"{topic} => Edge RSU sync {data}")
        db: Session = session.DB_SESSION_LOCAL()
        id_ = data.get("id")
        esn = data.get("esn")
        location = data.get("location")

        if id_ is not None and esn is not None and location is not None:
            node_rsu = crud.edge_node_rsu.get_by_node_id_esn(db, edge_node_id=id_, rsu_esn=esn)
            if node_rsu is not None:
                update_in = schemas.EdgeNodeRSUUpdate()
                update_in.location = location
                crud.edge_node_rsu.update(db, db_obj=node_rsu, obj_in=update_in)

        LOG.info(f"{topic} => Edge RSU updated")
