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

import datetime
import os
from logging import LoggerAdapter
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Query, UploadFile, status
from fastapi.responses import FileResponse
from oslo_log import log
from sqlalchemy import exc as sql_exc
from sqlalchemy.orm import Session

from dandelion import constants, crud, models, schemas
from dandelion.api import deps
from dandelion.api.deps import OpenV2XHTTPException as HTTPException, error_handle

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.get(
    "/{map_id}",
    response_model=schemas.Map,
    status_code=status.HTTP_200_OK,
    description="""
Get a Map.
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
    map_in_db = deps.crud_get(db=db, obj_id=map_id, crud_model=crud.map, detail="Map")
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
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Maps:
    skip = page_size * (page_num - 1)
    total, data = crud.map.get_multi_with_total(db, skip=skip, limit=page_size, name=name)
    return schemas.Maps(total=total, data=[map.to_dict() for map in data])


@router.patch(
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
    map_in_db = deps.crud_get(db=db, obj_id=map_id, crud_model=crud.map, detail="Map")
    if map_in.bitmap_filename and not os.path.exists(
        f"{constants.BITMAP_FILE_PATH}/{map_in.bitmap_filename}"
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"bitmap [filename: {map_in.bitmap_filename}] not found",
        )
    try:
        new_map_in_db = crud.map.update(db, db_obj=map_in_db, obj_in=map_in)
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        raise error_handle(ex, "name", map_in.name)
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
    map_in_db = deps.crud_get(db=db, obj_id=map_id, crud_model=crud.map, detail="Map")
    return map_in_db.data


@router.post(
    "/bitmap",
    status_code=status.HTTP_200_OK,
    description="""
add map bitmap.
""",
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def add_bitmap(
    bitmap: UploadFile,
    *,
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.jpg"
    if os.path.exists(f"{constants.BITMAP_FILE_PATH}/{filename}"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"bitmap filename:{filename} already exist",
        )
    with open(f"{constants.BITMAP_FILE_PATH}/{filename}", "wb") as f:
        f.write(bitmap.file.read())

    return {"bitmapFilename": filename}


@router.get(
    "/{map_id}/bitmap",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    description="""
Get a bitmap data.
""",
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_bitmap(
    map_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> FileResponse:
    map_in_db = deps.crud_get(db=db, obj_id=map_id, crud_model=crud.map, detail="Map")
    if not map_in_db.bitmap_filename:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bitmap not found")
    return FileResponse(f"{constants.BITMAP_FILE_PATH}/{map_in_db.bitmap_filename}")
