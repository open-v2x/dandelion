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

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.RSUModel,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new RSU Model.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.RSUModel, "description": "Created"},
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
    rsu_model_in: schemas.RSUModelCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUModel:
    rsu_model_in_db = crud.rsu_model.create(db, obj_in=rsu_model_in)
    return rsu_model_in_db.to_dict()


@router.delete(
    "/{rsu_model_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a RSU Model.
""",
    responses={
        status.HTTP_204_NO_CONTENT: {"class": JSONResponse, "description": "No Content"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
    response_class=JSONResponse,
)
def delete(
    rsu_model_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> JSONResponse:
    if not crud.rsu_model.get(db, id=rsu_model_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RSU Model [id: {rsu_model_id}] not found",
        )
    crud.rsu_model.remove(db, id=rsu_model_id)
    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{rsu_model_id}",
    response_model=schemas.RSUModel,
    status_code=status.HTTP_200_OK,
    description="""
Get a RSU Model.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUModel, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    rsu_model_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUModel:
    rsu_model_in_db = crud.rsu_model.get(db, id=rsu_model_id)
    if not rsu_model_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RSU Model [id: {rsu_model_id}] not found",
        )
    return rsu_model_in_db.to_dict()


@router.get(
    "",
    response_model=schemas.RSUModels,
    status_code=status.HTTP_200_OK,
    description="""
Get all RSU Models.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUModels, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def list(
    name: Optional[str] = Query(
        None, alias="name", description="Filter by name. Fuzzy prefix query is supported"
    ),
    manufacturer: Optional[str] = Query(
        None,
        alias="manufacturer",
        description="Filter by manufacturer. Fuzzy prefix query is supported",
    ),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=0, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUModels:
    skip = page_size * (page_num - 1)
    total, data = crud.rsu_model.get_multi_with_total(
        db, skip=skip, limit=page_size, name=name, manufacturer=manufacturer
    )
    return schemas.RSUModels(total=total, data=[rsu_model.to_dict() for rsu_model in data])


@router.put(
    "/{rsu_model_id}",
    response_model=schemas.RSUModel,
    status_code=status.HTTP_200_OK,
    description="""
Update a RSU Model.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUModel, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    rsu_model_id: int,
    rsu_model_in: schemas.RSUModelUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUModel:
    rsu_model_in_db = crud.rsu_model.get(db, id=rsu_model_id)
    if not rsu_model_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RSU Model [id: {rsu_model_id}] not found",
        )
    new_rsu_model_in_db = crud.rsu_model.update(db, db_obj=rsu_model_in_db, obj_in=rsu_model_in)
    return new_rsu_model_in_db.to_dict()
