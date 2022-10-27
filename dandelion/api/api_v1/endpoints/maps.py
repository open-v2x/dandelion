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
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from oslo_log import log
from sqlalchemy import exc as sql_exc
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.util import Optional as Optional_util

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.Map,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new Map.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.Map, "description": "Created"},
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
    map_in: schemas.MapCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Map:
    new_map_in = models.Map(
        name=map_in.name,
        area_code=map_in.area_code,
        address=map_in.address,
        desc=map_in.desc,
        data=map_in.data,
        lng=Optional_util.none(map_in.data.get("refPos")).map(lambda v: v.get("lon")).orElse(0),
        lat=Optional_util.none(map_in.data.get("refPos")).map(lambda v: v.get("lat")).orElse(0),
    )
    try:
        map_in_db = crud.map.create(db, obj_in=new_map_in)
    except sql_exc.IntegrityError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=deps.error_msg_handle(ex.args[0])
        )
    return map_in_db.to_dict()


@router.delete(
    "/{map_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a Map.
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
    map_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    if not crud.map.get(db, id=map_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": status.HTTP_404_NOT_FOUND, "msg": f"Map [id: {map_id}] not found"},
        )
    crud.map.remove(db, id=map_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{map_id}",
    response_model=schemas.Map,
    status_code=status.HTTP_200_OK,
    description="""
Get a Radar.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Map, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    map_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Map:
    map_in_db = crud.map.get(db, id=map_id)
    if not map_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": status.HTTP_404_NOT_FOUND, "msg": f"Map [id: {map_id}] not found"},
        )
    return map_in_db.to_dict()


@router.get(
    "",
    response_model=schemas.Maps,
    status_code=status.HTTP_200_OK,
    summary="List Maps",
    description="""
Get all Maps.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Maps, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all(
    name: Optional[str] = Query(
        None, alias="name", description="Filter by map name. Fuzzy prefix query is supported"
    ),
    area_code: Optional[str] = Query(None, alias="areaCode", description="Filter by map areaCode"),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Maps:
    skip = page_size * (page_num - 1)
    total, data = crud.map.get_multi_with_total(
        db, skip=skip, limit=page_size, name=name, area_code=area_code
    )
    return schemas.Maps(total=total, data=[map.to_dict() for map in data])


@router.put(
    "/{map_id}",
    response_model=schemas.Map,
    status_code=status.HTTP_200_OK,
    description="""
Update a Map.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Map, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    map_id: int,
    map_in: schemas.MapUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Map:
    map_in_db = crud.map.get(db, id=map_id)
    if not map_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": status.HTTP_404_NOT_FOUND, "msg": f"Map [id: {map_id}] not found"},
        )

    new_map_in = models.Map()
    new_map_in.name = map_in.name
    new_map_in.area_code = map_in.area_code
    new_map_in.address = map_in.address
    new_map_in.desc = map_in.desc
    if map_in.data:
        new_map_in.lng = map_in.data.get("refPos", {}).get("lon", 0.0)
        new_map_in.lat = map_in.data.get("refPos", {}).get("lat", 0.0)

    try:
        new_map_in_db = crud.map.update(db, db_obj=map_in_db, obj_in=new_map_in.__dict__)
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        LOG.error(ex.args[0])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=deps.error_msg_handle(ex.args[0])
        )
    return new_map_in_db.to_dict()


@router.get(
    "/{map_id}/data",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    description="""
Get a Map data.
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
def data(
    map_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Dict[str, Any]:
    map_in_db = crud.map.get(db, id=map_id)
    if not map_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": status.HTTP_404_NOT_FOUND, "msg": f"Map [id: {map_id}] not found"},
        )
    return map_in_db.data
