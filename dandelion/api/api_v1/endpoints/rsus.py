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
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from oslo_log import log
from redis import Redis
from sqlalchemy import exc as sql_exc
from sqlalchemy.orm import Session, exc as orm_exc

from dandelion import crud, models, schemas
from dandelion.api import deps
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
        status.HTTP_400_BAD_REQUEST: {"model": schemas.ErrorMessage, "description": "Bad Request"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
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
        try:
            rsu_tmp = crud.rsu_tmp.get(db, rsu_in.tmp_id)
            crud.rsu_tmp.remove(db, id=rsu_in.tmp_id)
        except orm_exc.UnmappedInstanceError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"RSU Temp [id: {rsu_in.tmp_id}] not found",
            )
    del rsu_in.tmp_id
    try:
        rsu_in_db = crud.rsu.create_rsu(db, obj_in=rsu_in, rsu_tmp_in_db=rsu_tmp)
    except sql_exc.IntegrityError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    return rsu_in_db.to_all_dict()


@router.get(
    "",
    response_model=schemas.RSUs,
    status_code=status.HTTP_200_OK,
    description="""
Get all RSUs.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUs, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def list(
    rsu_name: Optional[str] = Query(
        None, alias="rsuName", description="Filter by rsuName. Fuzzy prefix query is supported"
    ),
    rsu_esn: Optional[str] = Query(
        None, alias="rsuEsn", description="Filter by rsuEsn. Fuzzy prefix query is supported"
    ),
    area_code: Optional[str] = Query(None, alias="areaCode", description="Filter by areaCode"),
    online_status: Optional[bool] = Query(
        None, alias="onlineStatus", description="Filter by onlineStatus"
    ),
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
        area_code=area_code,
        online_status=online_status,
        rsu_status=rsu_status,
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
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    rsu_id: int,
    *,
    db: Session = Depends(deps.get_db),
    redis_conn: Redis = Depends(deps.get_redis_conn),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUDetail:
    rsu_in_db = crud.rsu.get(db, id=rsu_id)
    if not rsu_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RSU [id: {rsu_in_db}] not found",
        )
    result = rsu_in_db.to_info_dict()
    rsu_config_rsus: List[models.RSUConfigRSU] = result["config"]
    result["config"] = [rsu_config_rsu.to_dict() for rsu_config_rsu in rsu_config_rsus]
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
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    rsu_id: int,
    rsu_in: schemas.RSUUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSU:
    rsu_in_db = crud.rsu.get(db, id=rsu_id)
    if not rsu_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"RSU [id: {rsu_id}] not found"
        )
    try:
        new_rsu_in_db = crud.rsu.update(db, db_obj=rsu_in_db, obj_in=rsu_in)
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        LOG.error(ex.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    return new_rsu_in_db.to_all_dict()


@router.delete(
    "/{rsu_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a RSU.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
    response_class=Response,
    response_description="No Content",
)
def delete(
    rsu_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    if not crud.rsu.get(db, id=rsu_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"RSU [id: {rsu_id}] not found"
        )
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
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
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
    "/{rsu_id}/map",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    description="""
Get a RSU Map.
""",
    responses={
        status.HTTP_200_OK: {"model": Dict[str, Any], "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_map(
    rsu_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Dict[str, Any]:
    map_rsu_in_db = crud.map_rsu.get_by_rsu_id(db, rsu_id=rsu_id)
    if not map_rsu_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Map RSU [rsu_id: {rsu_id}] not found",
        )
    return Optional_util.none(map_rsu_in_db).map(lambda v: v.map).map(lambda v: v.data).get()
