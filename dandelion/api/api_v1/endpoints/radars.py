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
from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status
from oslo_log import log
from sqlalchemy import exc as sql_exc
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.api.deps import OpenV2XHTTPException as HTTPException

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.Radar,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new Radar.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.Radar, "description": "Created"},
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
    radar_in: schemas.RadarCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Radar:
    try:
        radar_in_db = crud.radar.create(db, obj_in=radar_in)
    except (sql_exc.IntegrityError, sql_exc.DataError) as ex:
        LOG.error(ex.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    return radar_in_db.to_dict()


@router.delete(
    "/{radar_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a Radar.
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
    radar_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    if not crud.radar.get(db, id=radar_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Radar [id: {radar_id}] not found"
        )
    crud.radar.remove(db, id=radar_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{radar_id}",
    response_model=schemas.Radar,
    status_code=status.HTTP_200_OK,
    description="""
Get a Radar.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Radar, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    radar_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Radar:
    radar_in_db = crud.radar.get(db, id=radar_id)
    if not radar_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Radar [id: {radar_id}] not found"
        )
    return radar_in_db.to_dict()


@router.get(
    "",
    response_model=schemas.Radars,
    status_code=status.HTTP_200_OK,
    summary="List Radars",
    description="""
Get all Radars.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Radars, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all(
    sn: Optional[str] = Query(
        None, alias="sn", description="Filter by radar sn. Fuzzy prefix query is supported"
    ),
    name: Optional[str] = Query(
        None, alias="name", description="Filter by radar name. Fuzzy prefix query is supported"
    ),
    rsu_id: Optional[int] = Query(None, alias="rsuId", description="Filter by rsuId"),
    area_code: Optional[str] = Query(
        None, alias="areaCode", description="Filter by camera area code"
    ),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Radars:
    skip = page_size * (page_num - 1)
    total, data = crud.radar.get_multi_with_total(
        db, skip=skip, limit=page_size, sn=sn, name=name, rsu_id=rsu_id, area_code=area_code
    )
    return schemas.Radars(total=total, data=[radar.to_dict() for radar in data])


@router.put(
    "/{radar_id}",
    response_model=schemas.Radar,
    status_code=status.HTTP_200_OK,
    description="""
Update a Radar.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Radar, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    radar_id: int,
    radar_in: schemas.RadarUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Radar:
    radar_in_db = crud.radar.get(db, id=radar_id)
    if not radar_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Radar [id: {radar_id}] not found"
        )
    try:
        new_radar_in_db = crud.radar.update(db, db_obj=radar_in_db, obj_in=radar_in)
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        LOG.error(ex.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    return new_radar_in_db.to_dict()
