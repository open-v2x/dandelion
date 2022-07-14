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

import redis
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, schemas
from dandelion.db import redis_pool, session
from dandelion.mqtt import cloud_server as mqtt_cloud_server

LOG: LoggerAdapter = log.getLogger(__name__)


def update_rsu_online_status() -> None:
    LOG.info("Updating RSU online status...")
    db: Session = session.DB_SESSION_LOCAL()
    redis_conn: redis.Redis = redis_pool.REDIS_CONN

    _, online_rsus = crud.rsu.get_multi_with_total(db, online_status=True)
    LOG.debug(f"Found {len(online_rsus)} online RSUs")
    for rsu in online_rsus:
        if redis_conn.get(f"RSU_ONLINE_{rsu.rsu_esn}"):
            continue
        try:
            crud.rsu.update_online_status(
                db, db_obj=rsu, obj_in=schemas.RSUUpdateWithStatus(onlineStatus=False)
            )
        except Exception as ex:
            LOG.warn(f"Failed to update RSU [rsu_esn: {rsu.rsu_esn}] online status: {ex}")


def delete_offline_edge() -> None:
    LOG.info("Deleting offline Edge...")
    db: Session = session.DB_SESSION_LOCAL()
    redis_conn: redis.Redis = redis_pool.REDIS_CONN

    _, edges = crud.edge_node.get_multi_with_total(db)
    LOG.debug(f"Found {len(edges)} online Edges")
    for edge in edges:
        if redis_conn.get(f"EDGE_ONLINE_{edge.id}"):
            continue
        try:
            crud.edge_node_rsu.remove_by_node_id(db, edge_node_id=edge.id)
            crud.edge_node.remove(db, id=edge.id)
        except Exception as ex:
            LOG.warn(f"Failed to delete Edge [id: {edge.id}]: {ex}")


def edge_heartbeat() -> None:
    LOG.info("Edge Heartbeat...")

    client = mqtt_cloud_server.GET_MQTT_CLIENT()
    edge_id = mqtt_cloud_server.GET_EDGE_ID()
    if client and edge_id > 0:
        client.publish(topic="V2X/EDGE/HB/UP", payload=json.dumps(dict(id=edge_id)), qos=0)
