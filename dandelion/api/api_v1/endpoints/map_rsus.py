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
from typing import Dict, List, Union

from fastapi import APIRouter, Depends, Path, Query, Response, status
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
Create a new rsu map.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.MapRSU, "description": "Created"},
        **deps.RESPONSE_ERROR,
    },
)
def create(
    map_rsu_in: schemas.MapRSUCreate,
    *,
    map_id: int = Path(),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.MapRSU:
    map_in_db = deps.crud_get(db=db, obj_id=map_id, crud_model=crud.map, detail="Map")
    rsus: List[models.RSU] = []
    for rsu_id in map_rsu_in.rsus:
        rsu_in_db = deps.crud_get(db=db, obj_id=rsu_id, crud_model=crud.rsu, detail="RSU")
        rsus.append(rsu_in_db)

    map_rsus: List[Dict[str, Union[int, str, datetime, bool]]] = []
    for rsu in rsus:
        _map_rsu = models.MapRSU()
        _map_rsu.map_id = map_id
        _map_rsu.rsu_id = rsu.id
        map_rsu = crud.map_rsu.create(db, obj_in=_map_rsu)
        map_rsus.append(
            {
                "id": map_rsu.id,
                "rsuId": map_rsu.rsu_id,
                "status": map_rsu.status,
                "createTime": map_rsu.create_time,
            }
        )
        map_down(map_rsu.id, map_in_db.name, map_in_db.data, "v1", rsu.rsu_esn)

    return schemas.MapRSU(**{"data": {"mapId": map_id, "rsus": map_rsus}})


@router.delete(
    "/{map_id}/rsus/{map_rsu_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a Map RSU.
""",
    responses=deps.RESPONSE_ERROR,
    response_class=Response,
    response_description="No Content",
)
def delete(
    *,
    map_id: int = Path(),
    map_rsu_id: int = Path(),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    deps.crud_get(db=db, obj_id=map_id, crud_model=crud.map, detail="Map")
    deps.crud_get(db=db, obj_id=map_rsu_id, crud_model=crud.map_rsu, detail="MapRSU")

    crud.map_rsu.remove(db, id=map_rsu_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{map_id}/rsus",
    response_model=schemas.MapRSUs,
    status_code=status.HTTP_200_OK,
    summary="List Map RSUs",
    description="""
Get all Map RSUs.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.MapRSUs, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get_all(
    map_id: int = Path(),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.MapRSUs:
    skip = page_size * (page_num - 1)
    total, data = crud.map_rsu.get_multi_with_total(db, skip=skip, limit=page_size, map_id=map_id)
    return schemas.MapRSUs(total=total, data=[map_rsu.to_dict() for map_rsu in data])
