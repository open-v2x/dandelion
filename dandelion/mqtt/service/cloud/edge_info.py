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
from typing import Any, Dict

import paho.mqtt.client as mqtt
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, schemas
from dandelion.db import session
from dandelion.mqtt.service import RouterHandler

LOG: LoggerAdapter = log.getLogger(__name__)


class EdgeInfoRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()
        name = data.get("name")
        if name:
            edge_node = crud.edge_node.get_by_name(db, name)
            if not edge_node:
                edge_node_in = schemas.EdgeNodeCreate()
                edge_node_in.name = name
                edge_node = crud.edge_node.create(db, obj_in=edge_node_in)
            client.publish(
                topic=f'V2X/EDGE/{data.get("key")}/INFO/UP/ACK',
                payload=json.dumps(dict(id=edge_node.id)),
                qos=0,
            )
        LOG.info(f"{topic} => Edge registered")
