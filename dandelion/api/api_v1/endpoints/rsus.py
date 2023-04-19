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
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Response, status
from oslo_log import log
from redis import Redis
from sqlalchemy import exc as sql_exc
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.api.deps import OpenV2XHTTPException as HTTPException, error_handle
from dandelion.util import Optional as Optional_util

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.RSU,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new RSU.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.RSU, "description": "Created"},
        **deps.RESPONSE_ERROR,
    },
)
def create(
    rsu_in: schemas.RSUCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSU:
    rsu_tmp: Optional[models.RSUTMP] = None
    if rsu_in.tmp_id:
        deps.crud_get(
            db=db,
            obj_id=rsu_in.tmp_id,
            crud_model=crud.rsu_tmp,
            detail="TMP RSU",
        )
        crud.rsu_tmp.remove(db, id=rsu_in.tmp_id)

    del rsu_in.tmp_id
    try:
        rsu_in_db = crud.rsu.create_rsu(db, obj_in=rsu_in, rsu_tmp_in_db=rsu_tmp)
    except (sql_exc.IntegrityError, sql_exc.DataError) as ex:
        raise error_handle(ex, "rsu_esn", rsu_in.rsu_esn)
    return rsu_in_db.to_all_dict()


@router.get(
    "",
    response_model=schemas.RSUs,
    status_code=status.HTTP_200_OK,
    summary="List RSUs",
    description="""
Get all RSUs.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUs, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get_all(
    rsu_name: Optional[str] = Query(
        None, alias="rsuName", description="Filter by rsuName. Fuzzy prefix query is supported"
    ),
    rsu_esn: Optional[str] = Query(
        None, alias="rsuEsn", description="Filter by rsuEsn. Fuzzy prefix query is supported"
    ),
    online_status: Optional[bool] = Query(
        None, alias="onlineStatus", description="Filter by onlineStatus"
    ),
    enabled: Optional[bool] = Query(None, alias="enabled", description="Filter by enabled"),
    rsu_status: Optional[str] = Query(None, alias="rsuStatus", description="Filter by rsuStatus"),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUs:
    skip = page_size * (page_num - 1)
    total, data = crud.rsu.get_multi_with_total(
        db,
        skip=skip,
        limit=page_size,
        rsu_name=rsu_name,
        rsu_esn=rsu_esn,
        online_status=online_status,
        rsu_status=rsu_status,
        enabled=enabled,
    )
    return schemas.RSUs(total=total, data=[rsu.to_all_dict() for rsu in data])


@router.get(
    "/{rsu_id}",
    response_model=schemas.RSUDetail,
    status_code=status.HTTP_200_OK,
    description="""
Get a RSU.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUDetail, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get(
    rsu_id: int,
    *,
    db: Session = Depends(deps.get_db),
    redis_conn: Redis = Depends(deps.get_redis_conn),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUDetail:
    rsu_in_db = deps.crud_get(db=db, obj_id=rsu_id, crud_model=crud.rsu, detail="RSU")
    result = rsu_in_db.to_info_dict()
    rsu_config_rsus: List[models.RSUConfigRSU] = result["config"]
    result["config"] = [rsu_config_rsu.to_config_dict() for rsu_config_rsu in rsu_config_rsus]
    key = f"RSU_RUNNING_INFO_{rsu_in_db.rsu_esn}"
    result["runningInfo"] = dict(
        cpu=Optional_util.none(redis_conn.hget(key, "cpu"))
        .map(lambda v: json.loads(v))
        .orElse({}),
        mem=Optional_util.none(redis_conn.hget(key, "mem"))
        .map(lambda v: json.loads(v))
        .orElse({}),
        disk=Optional_util.none(redis_conn.hget(key, "disk"))
        .map(lambda v: json.loads(v))
        .orElse({}),
        net=Optional_util.none(redis_conn.hget(key, "net"))
        .map(lambda v: json.loads(v))
        .orElse({}),
    )
    return result


@router.patch(
    "/{rsu_id}",
    response_model=schemas.RSU,
    status_code=status.HTTP_200_OK,
    description="""
Update a RSU.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSU, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def update(
    rsu_id: int,
    rsu_in: schemas.RSUUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSU:
    rsu_in_db = deps.crud_get(db=db, obj_id=rsu_id, crud_model=crud.rsu, detail="RSU")
    try:
        new_rsu_in_db = crud.rsu.update_with_location(db, db_obj=rsu_in_db, obj_in=rsu_in)
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        raise error_handle(ex, "rsu_esn", rsu_in.rsu_esn)
    return new_rsu_in_db.to_all_dict()


@router.delete(
    "/{rsu_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a RSU.
""",
    responses=deps.RESPONSE_ERROR,
    response_class=Response,
    response_description="No Content",
)
def delete(
    rsu_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    deps.crud_get(db=db, obj_id=rsu_id, crud_model=crud.rsu, detail="RSU")
    results = crud.rsu_query_result.get_multi_by_rsu_id(db, rsu_id=rsu_id)
    for result in results:
        crud.rsu_query_result_data.remove_by_result_id(db, result_id=result.id)
        crud.rsu_query_result.remove(db, id=result.id)
    crud.mng.remove_by_rsu_id(db, rsu_id=rsu_id)
    crud.rsu.remove(db, id=rsu_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{rsu_esn}/location",
    response_model=schemas.RSULocation,
    status_code=status.HTTP_200_OK,
    description="""
Get a RSU Location.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSULocation, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get_location(
    rsu_esn: str,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSULocation:
    rsu_in_db = crud.rsu.get_by_rsu_esn(db, rsu_esn=rsu_esn)
    if not rsu_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RSU [rsu_esn: {rsu_esn}] not found",
        )
    return Optional_util.none(rsu_in_db).map(lambda v: v.location).get()


@router.get(
    "/{rsu_id}/running",
    response_model=schemas.RSURunning,
    status_code=status.HTTP_200_OK,
    description="""
Get a RSU Running Info.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSURunning, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get_running(
    rsu_id: int,
    *,
    db: Session = Depends(deps.get_db),
    redis_conn: Redis = Depends(deps.get_redis_conn),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSURunning:
    rsu_in_db = deps.crud_get(db=db, obj_id=rsu_id, crud_model=crud.rsu, detail="RSU")
    rsu_running = schemas.RSURunning()
    rsu_running.cpu = []
    for cpu in redis_conn.zrevrange(f"RSU_RUNNING_CPU_{rsu_in_db.rsu_esn}", start=0, end=6):
        data = json.loads(cpu)
        cpu_ = schemas.RunningCPU()
        cpu_.time = data.get("time")
        cpu_.uti = data.get("uti", 0)
        cpu_.load = data.get("load", 0)
        rsu_running.cpu.append(cpu_)

    rsu_running.mem = []
    for mem in redis_conn.zrevrange(f"RSU_RUNNING_MEM_{rsu_in_db.rsu_esn}", start=0, end=6):
        data = json.loads(mem)
        mem_ = schemas.RunningMEM()
        mem_.time = data.get("time")
        mem_.total = data.get("total", 0)
        mem_.used = data.get("used", 0)
        rsu_running.mem.append(mem_)

    rsu_running.disk = []
    for disk in redis_conn.zrevrange(f"RSU_RUNNING_DISK_{rsu_in_db.rsu_esn}", start=0, end=6):
        data = json.loads(disk)
        disk_ = schemas.RunningDisk()
        disk_.time = data.get("time")
        disk_.rx_byte = data.get("rxByte", 0)
        disk_.wx_byte = data.get("wxByte", 0)
        rsu_running.disk.append(disk_)

    rsu_running.net = []
    for net in redis_conn.zrevrange(f"RSU_RUNNING_NET_{rsu_in_db.rsu_esn}", start=0, end=6):
        data = json.loads(net)
        net_ = schemas.RunningNet()
        net_.time = data.get("time")
        net_.read = data.get("read", 0)
        net_.write = data.get("write", 0)
        rsu_running.net.append(net_)

    return rsu_running
