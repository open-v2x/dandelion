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

import redis
from fastapi import APIRouter, Depends, status
from oslo_config import cfg
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.mqtt import cloud_server as mqtt_cloud_server
from dandelion.mqtt.topic import v2x_edge

router = APIRouter()
CONF: cfg = cfg.CONF
mode_conf = CONF.mode
mqtt_conf = CONF.mqtt


@router.post(
    "",
    response_model=schemas.SystemConfig,
    status_code=status.HTTP_200_OK,
    description="""
Get detailed info of System Config.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.SystemConfig, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def create(
    user_in: schemas.SystemConfigCreate,
    *,
    db: Session = Depends(deps.get_db),
    redis_conn: redis.Redis = Depends(deps.get_redis_conn),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.SystemConfig:
    """
    Set system configuration.
    """
    # mq_host = (
    #     Optional.none(user_in).map(lambda c: c.mqtt_config).map(lambda c: c.host).orElse(None)
    # )
    # mq_port = (
    #     Optional.none(user_in).map(lambda c: c.mqtt_config).map(lambda c: c.port).orElse(None)
    # )
    # if "edge" == mode_conf.mode:
    #     if (
    #         mq_host is not None
    #         and mqtt_conf.host == mq_host
    #         and mq_port is not None
    #         and mqtt_conf.port == mq_port
    #     ):
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Coexist node configuration is the different as the node.",
    #         )

    # if "center" == mode_conf.mode:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="The current node does not support configuration.",
    #     )
    # if "coexist" == mode_conf.mode:
    #     if (mq_host is not None and mqtt_conf.host != mq_host) or (
    #         mq_port is not None and mqtt_conf.port != mq_port
    #     ):
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Coexist node configuration is the same as the node.",
    #         )
    # System configuration is global, So use ID=1.
    system_config = crud.system_config.get(db, id=1)
    if system_config:
        system_config = crud.system_config.update(db, db_obj=system_config, obj_in=user_in)
        if mqtt_cloud_server.MQTT_CLIENT:
            # disconnect
            if system_config.node_id is not None and system_config.node_id > 0:
                mqtt_cloud_server.MQTT_CLIENT.publish(
                    topic=v2x_edge.V2X_EDGE_DELETE_UP,
                    payload=json.dumps(dict(edge_id=system_config.node_id)),
                    qos=0,
                )
            mqtt_cloud_server.MQTT_CLIENT.disconnect()
        mqtt_cloud_server.connect()
    else:
        system_config = crud.system_config.create(db, obj_in=user_in)
        mqtt_cloud_server.connect()

    return system_config


@router.get(
    "/{system_config_id}",
    response_model=schemas.SystemConfig,
    status_code=status.HTTP_200_OK,
    description="""
Get detailed info of System Config.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.SystemConfig, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    system_config_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.SystemConfig:
    system_config = deps.crud_get(
        db=db,
        obj_id=system_config_id,
        crud_model=crud.system_config,
        detail="System config",
    )
    system_config.mode = mode_conf.mode
    return system_config
