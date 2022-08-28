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
import redis
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud
from dandelion.db import redis_pool, session
from dandelion.mqtt.service import RouterHandler

LOG: LoggerAdapter = log.getLogger(__name__)


class EdgeDeleteRouterHandler(RouterHandler):
    def handler(self, client: mqtt.MQTT_CLIENT, topic: str, data: Dict[str, Any]) -> None:
        db: Session = session.DB_SESSION_LOCAL()
        redis_conn: redis.Redis = redis_pool.REDIS_CONN
        edge_id: int = data.get("edge_id", 0)
        redis_conn.delete(f"EDGE_ONLINE_{edge_id}")
        try:
            crud.edge_node_rsu.remove_by_node_id(db, edge_node_id=edge_id)
            crud.edge_node.remove(db, id=edge_id)
        except Exception as ex:
            LOG.warn(f"Failed to delete Edge [id: {edge_id}]: {ex}")
        LOG.info(f"{topic} => Edge offline")
