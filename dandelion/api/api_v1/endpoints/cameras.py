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
    response_model=schemas.Camera,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new Camera.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.Camera, "description": "Created"},
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
    camera_in: schemas.CameraCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Camera:
    try:
        camera_in_db = crud.camera.create(db, obj_in=camera_in)
    except (sql_exc.IntegrityError, sql_exc.DataError) as ex:
        LOG.error(ex.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    return camera_in_db.to_dict()


@router.delete(
    "/{camera_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a Camera.
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
    camera_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    if not crud.camera.get(db, id=camera_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Camera [id: {camera_id}] not found"
        )
    crud.camera.remove(db, id=camera_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{camera_id}",
    response_model=schemas.Camera,
    status_code=status.HTTP_200_OK,
    description="""
Get a Camera.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Camera, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    camera_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Camera:
    camera_in_db = crud.camera.get(db, id=camera_id)
    if not camera_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Camera [id: {camera_id}] not found"
        )
    return camera_in_db.to_dict()


@router.get(
    "",
    response_model=schemas.Cameras,
    status_code=status.HTTP_200_OK,
    summary="List Cameras",
    description="""
Get all Cameras.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Cameras, "description": "OK"},
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
        None, alias="sn", description="Filter by camera sn. Fuzzy prefix query is supported"
    ),
    name: Optional[str] = Query(
        None, alias="name", description="Filter by camera name. Fuzzy prefix query is supported"
    ),
    rsu_id: Optional[int] = Query(None, alias="rsuId", description="Filter by RSU ID"),
    rsu_esn: Optional[str] = Query(None, alias="rsuEsn", description="Filter by rsuEsn"),
    area_code: Optional[str] = Query(
        None, alias="areaCode", description="Filter by camera area code"
    ),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Cameras:
    skip = page_size * (page_num - 1)
    total, data = crud.camera.get_multi_with_total(
        db,
        skip=skip,
        limit=page_size,
        sn=sn,
        name=name,
        rsu_id=rsu_id,
        area_code=area_code,
        rsu_esn=rsu_esn,
    )
    return schemas.Cameras(total=total, data=[camera.to_dict() for camera in data])


@router.put(
    "/{camera_id}",
    response_model=schemas.Camera,
    status_code=status.HTTP_200_OK,
    description="""
Update a Camera.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Camera, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    camera_id: int,
    camera_in: schemas.CameraUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUModel:
    camera_in_db = crud.camera.get(db, id=camera_id)
    if not camera_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Camera [id: {camera_id}] not found"
        )
    try:
        new_camera_in_db = crud.camera.update(db, db_obj=camera_in_db, obj_in=camera_in)
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        LOG.error(ex.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    return new_camera_in_db.to_dict()
