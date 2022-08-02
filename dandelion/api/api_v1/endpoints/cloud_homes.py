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

from fastapi import APIRouter, Body, Depends, Query, status
from oslo_log import log
from redis import Redis
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.util import Optional as Optional_util

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.get(
    "/online_rate",
    response_model=schemas.OnlineRate,
    status_code=status.HTTP_200_OK,
    description="""
Get online rate of all devices.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.OnlineRate, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def online_rate(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.OnlineRate:
    rsu_online_rate = {
        "online": crud.rsu.get_multi_with_total(db, online_status=True)[0],
        "offline": crud.rsu.get_multi_with_total(db, online_status=False)[0],
        "notRegister": crud.rsu_tmp.get_multi_with_total(db)[0],
    }
    # temporarily unavailable data
    camera_online_rate = {
        "online": 0,
        "offline": 0,
        "notRegister": crud.camera.get_multi_with_total(db)[0],
    }
    # temporarily unavailable data
    radar_online_rate = {
        "online": 0,
        "offline": 0,
        "notRegister": crud.radar.get_multi_with_total(db)[0],
    }
    return schemas.OnlineRate(
        **{
            "data": {
                "rsu": rsu_online_rate,
                "camera": camera_online_rate,
                "radar": radar_online_rate,
            }
        }
    )


@router.get(
    "/route_info",
    response_model=schemas.RouteInfo,
    status_code=status.HTTP_200_OK,
    description="""
Get traffic situation.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RouteInfo, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def route_info(
    rsu_esn: str = Query(..., alias="rsuEsn", description="RSU ESN"),
    *,
    redis_conn: Redis = Depends(deps.get_redis_conn),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RouteInfo:
    key = f"ROUTE_INFO_{rsu_esn}"
    return schemas.RouteInfo(
        vehicleTotal=Optional_util.none(redis_conn.hget(key, "vehicleTotal"))
        .map(lambda v: int(v))
        .orElse(0),
        averageSpeed=Optional_util.none(redis_conn.hget(key, "averageSpeed"))
        .map(lambda v: float(v))
        .map(lambda v: round(v, 1))
        .orElse(0),
        pedestrianTotal=Optional_util.none(redis_conn.hget(key, "pedestrianTotal"))
        .map(lambda v: int(v))
        .orElse(0),
        congestion=Optional_util.none(redis_conn.hget(key, "congestion"))
        .map(lambda v: str(v, encoding="utf-8"))
        .orElse("Unknown"),
    )


@router.post(
    "/route_info_push",
    response_model=schemas.RouteInfo,
    status_code=status.HTTP_201_CREATED,
    description="""
Push traffic situation.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.RouteInfo, "description": "OK"},
    },
)
def route_info_push(
    route_info_in: schemas.RouteInfoCreate = Body(..., description="Route Info"),
    *,
    redis_conn: Redis = Depends(deps.get_redis_conn),
) -> schemas.RouteInfo:
    rsu_esn = route_info_in.rsu_esn
    key = f"ROUTE_INFO_{rsu_esn}"
    if route_info_in.vehicle_total:
        redis_conn.hset(key, "vehicleTotal", route_info_in.vehicle_total)
    if route_info_in.average_speed:
        redis_conn.hset(key, "averageSpeed", route_info_in.average_speed)
    if route_info_in.pedestrian_total:
        redis_conn.hset(key, "pedestrianTotal", route_info_in.pedestrian_total)
    if route_info_in.congestion:
        redis_conn.hset(key, "congestion", route_info_in.congestion)
    redis_conn.expire(name=key, time=60)
    return schemas.RouteInfo(
        vehicleTotal=route_info_in.vehicle_total,
        averageSpeed=route_info_in.average_speed,
        pedestrianTotal=route_info_in.pedestrian_total,
        congestion=route_info_in.congestion,
    )
