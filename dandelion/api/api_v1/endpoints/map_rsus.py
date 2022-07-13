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

from datetime import datetime
from logging import LoggerAdapter
from typing import Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.mqtt.service.map.map_down import map_down

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "/{map_id}/rsus",
    response_model=schemas.MapRSU,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new Radar.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.MapRSU, "description": "Created"},
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
    map_id: int,
    map_rsu_in: schemas.MapRSUCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.MapRSU:
    map_in_db = crud.map.get(db, id=map_id)
    if not map_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Map [id: {map_id}] not found"
        )

    rsus: List[models.RSU] = []
    for rsu_id in map_rsu_in.rsus:
        rsu_in_db = crud.rsu.get(db, id=rsu_id)
        if not rsu_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"RSU [id: {rsu_id}] not found"
            )
        rsus.append(rsu_in_db)

    map_rsus: List[Dict[str, Union[int, str, datetime, bool]]] = []
    for rsu in rsus:
        _map_rsu = models.MapRSU(map_id=map_id, rsu_id=rsu.id)
        map_rsu = crud.map_rsu.create(db, obj_in=_map_rsu)
        map_rsus.append(
            {
                "id": map_rsu.id,
                "rsuId": map_rsu.rsu_id,
                "status": map_rsu.status,
                "createTime": map_rsu.create_time,
            }
        )
        map_down(map_in_db.name, map_in_db.data, "v1", rsu.rsu_esn)

    return schemas.MapRSU(**{"data": {"mapId": map_id, "rsus": map_rsus}})


@router.delete(
    "/{map_id}/rsus/{map_rsu_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a Map RSU.
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
    map_rsu_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    if not crud.map.get(db, id=map_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Map [id: {map_id}] not found"
        )
    if not crud.map_rsu.get(db, id=map_rsu_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"MapRSU [id: {map_rsu_id}] not found"
        )
    crud.map_rsu.remove(db, id=map_rsu_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{map_id}/rsus",
    response_model=schemas.MapRSUs,
    status_code=status.HTTP_200_OK,
    description="""
Get all Map RSUs.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.MapRSUs, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def list(
    map_id: Optional[int] = Query(None, alias="mapId", description="Filter by mapId"),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.MapRSUs:
    skip = page_size * (page_num - 1)
    total, data = crud.map_rsu.get_multi_with_total(db, skip=skip, limit=page_size, map_id=map_id)
    return schemas.MapRSUs(total=total, data=[map_rsu.to_dict() for map_rsu in data])
