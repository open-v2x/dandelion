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
from dandelion.api.deps import error_handle

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.RadarCamera,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new RadarCamera.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.RadarCamera, "description": "Created"},
        **deps.RESPONSE_ERROR,
    },
)
def create(
    radar_camera_in: schemas.RadarCameraCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RadarCamera:
    try:
        radar_in_db = crud.radar_camera.create(db, obj_in=radar_camera_in)
    except (sql_exc.IntegrityError, sql_exc.DataError) as ex:
        raise error_handle(ex, "sn or name", f"{radar_camera_in.sn} or {radar_camera_in.name}")
    return radar_in_db.to_all_dict()


@router.delete(
    "/{radar_camera_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a RadarCamera.
""",
    responses=deps.RESPONSE_ERROR,
    response_class=Response,
    response_description="No Content",
)
def delete(
    radar_camera_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    crud.radar_camera.remove(db, id=radar_camera_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{radar_camera_id}",
    response_model=schemas.RadarCamera,
    status_code=status.HTTP_200_OK,
    description="""
Get a RadarCamera.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RadarCamera, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get(
    radar_camera_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RadarCamera:
    radar_in_db = deps.crud_get(
        db=db, obj_id=radar_camera_id, crud_model=crud.radar_camera, detail="RadarCamera"
    )
    return radar_in_db.to_all_dict()


@router.get(
    "",
    response_model=schemas.RadarCameras,
    status_code=status.HTTP_200_OK,
    summary="List RadarCamera",
    description="""
Get all RadarCameras.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RadarCameras, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get_all(
    sn: Optional[str] = Query(
        None, alias="sn", description="Filter by sn. Fuzzy prefix query is supported"
    ),
    name: Optional[str] = Query(
        None, alias="name", description="Filter by name. Fuzzy prefix query is supported"
    ),
    rsu_id: Optional[int] = Query(None, alias="rsuID", description="Filter by rsuID"),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RadarCameras:
    skip = page_size * (page_num - 1)
    total, data = crud.radar_camera.get_multi_with_total(
        db,
        skip=skip,
        limit=page_size,
        sn=sn,
        name=name,
        rsu_id=rsu_id,
    )
    return schemas.RadarCameras(
        total=total, data=[radar_camera.to_all_dict() for radar_camera in data]
    )


@router.patch(
    "/{radar_camera_id}",
    response_model=schemas.RadarCamera,
    status_code=status.HTTP_200_OK,
    description="""
Update a RadarCamera.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RadarCamera, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def update(
    radar_camera_id: int,
    radar_camera_in: schemas.RadarCameraUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RadarCamera:
    radar_camera_in_db = deps.crud_get(
        db=db, obj_id=radar_camera_id, crud_model=crud.radar_camera, detail="RadarCamera"
    )
    try:
        new_radar_camera_in_db = crud.radar_camera.update(
            db, db_obj=radar_camera_in_db, obj_in=radar_camera_in
        )
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        raise error_handle(ex, "sn or name", f"{radar_camera_in.sn} or {radar_camera_in.name}")
    return new_radar_camera_in_db.to_all_dict()
