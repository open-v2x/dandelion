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
import os
import time
from logging import LoggerAdapter

import redis
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import constants, crud, schemas
from dandelion.db import redis_pool, session
from dandelion.mqtt import cloud_server as mqtt_cloud_server
from dandelion.mqtt.topic import v2x_edge
from dandelion.util import Optional

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

    client = mqtt_cloud_server.get_mqtt_client()
    edge_id = mqtt_cloud_server.get_edge_id()
    if client and edge_id > 0:
        client.publish(topic="V2X/EDGE/HB/UP", payload=json.dumps(dict(id=edge_id)), qos=0)


def edge_delete() -> None:
    LOG.info("Edge Delete...")
    db: Session = session.DB_SESSION_LOCAL()
    system_config = crud.system_config.get(db, id=1)
    if system_config:
        if system_config.node_id is not None and system_config.node_id > 0:
            mqtt_cloud_server.MQTT_CLIENT.publish(
                topic=v2x_edge.V2X_EDGE_DELETE_UP,
                payload=json.dumps(dict(edge_id=system_config.node_id)),
                qos=0,
            )


def rsu_info():
    LOG.info("RSU Running Info...")
    db: Session = session.DB_SESSION_LOCAL()
    redis_conn: redis.Redis = redis_pool.REDIS_CONN
    _, rsus = crud.rsu.get_multi_with_total(db, limit=-1)
    for rsu in rsus:
        get_key = f"RSU_RUNNING_INFO_{rsu.rsu_esn}"
        c_time = int(time.time())
        cpu_data = json.loads(Optional.none(redis_conn.hget(get_key, "cpu")).orElse("{}"))
        cpu = dict(
            time=c_time,
            uti=Optional.none(cpu_data.get("uti")).map(lambda s: len(s.split(","))).orElse(0),
            load=cpu_data.get("load", 0),
        )
        mem_data = json.loads(Optional.none(redis_conn.hget(get_key, "mem")).orElse("{}"))
        mem = dict(time=c_time, total=mem_data.get("total", 0), used=mem_data.get("used", 0))
        net_data = json.loads(Optional.none(redis_conn.hget(get_key, "net")).orElse("{}"))
        net = dict(time=c_time, rxByte=net_data.get("rxByte", 0), wxByte=net_data.get("wxByte", 0))
        disk_data = json.loads(Optional.none(redis_conn.hget(get_key, "disk")).orElse("{}"))
        disk = dict(time=c_time, read=disk_data.get("read", 0), write=disk_data.get("write", 0))

        cpu_key = f"RSU_RUNNING_CPU_{rsu.rsu_esn}"
        redis_conn.zadd(cpu_key, {json.dumps(cpu): c_time})
        mem_key = f"RSU_RUNNING_MEM_{rsu.rsu_esn}"
        redis_conn.zadd(mem_key, {json.dumps(mem): c_time})
        disk_key = f"RSU_RUNNING_DISK_{rsu.rsu_esn}"
        redis_conn.zadd(disk_key, {json.dumps(disk): c_time})
        net_key = f"RSU_RUNNING_NET_{rsu.rsu_esn}"
        redis_conn.zadd(net_key, {json.dumps(net): c_time})

        if redis_conn.zcard(cpu_key) > 1000:
            redis_conn.zremrangebyrank(cpu_key, min=1, max=1)
        if redis_conn.zcard(mem_key) > 1000:
            redis_conn.zremrangebyrank(mem_key, min=1, max=1)
        if redis_conn.zcard(disk_key) > 1000:
            redis_conn.zremrangebyrank(disk_key, min=1, max=1)
        if redis_conn.zcard(net_key) > 1000:
            redis_conn.zremrangebyrank(net_key, min=1, max=1)


def delete_unused_bitmap() -> None:
    LOG.info("Bitmap delete...")
    db: Session = session.DB_SESSION_LOCAL()
    bitmaps = crud.intersection.get_list_bitmap(db)
    bitmaps_set = {bitmap.bitmap_filename for bitmap in bitmaps}
    for filename in os.listdir(constants.BITMAP_FILE_PATH):
        if filename != "map_bg.jpg" and filename not in bitmaps_set:
            os.remove(f"{constants.BITMAP_FILE_PATH}/{filename}")
            LOG.info(f"removed bitmap file {filename}")
