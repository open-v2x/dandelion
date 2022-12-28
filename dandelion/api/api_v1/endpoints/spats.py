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
from dandelion.mqtt.service.rsu.rsu_spat import spat_publish

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.Spat,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new Spat.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.Spat, "description": "Created"},
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
    spat_in: schemas.SpatCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Spat:
    try:
        spat_in_db = crud.spat.create(db, obj_in=spat_in)
    except sql_exc.IntegrityError as ex:
        LOG.error(ex.args[0])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": 1116,
                "msg": ex.args[0],
                "detail": {
                    "intersection_id": spat_in.intersection_id,
                    "phase_id": spat_in.phase_id,
                },
            },
        )
    except sql_exc.DataError as ex:
        LOG.error(ex.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    spat_publish(spat_in_db)
    return spat_in_db.to_dict()


@router.delete(
    "/{spat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a Spat.
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
    spat_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    if not crud.spat.get(db, id=spat_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Spat [id: {spat_id}] not found"
        )
    crud.spat.remove(db, id=spat_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{spat_id}",
    response_model=schemas.Spat,
    status_code=status.HTTP_200_OK,
    description="""
Get a Spat.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Spat, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    spat_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Spat:
    spat_in_db = crud.spat.get(db, id=spat_id)
    if not spat_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Spat [id: {spat_id}] not found"
        )
    return spat_in_db.to_dict()


@router.get(
    "",
    response_model=schemas.Spats,
    status_code=status.HTTP_200_OK,
    summary="List Spats",
    description="""
Get all Spats.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Spats, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all(
    intersection_id: Optional[str] = Query(
        None,
        alias="intersectionId",
        description="Filter by spat intersectionId. Fuzzy prefix query is supported",
    ),
    name: Optional[str] = Query(
        None, alias="name", description="Filter by spat name. Fuzzy prefix query is supported"
    ),
    rsu_id: Optional[int] = Query(None, alias="rsuId", description="Filter by rsuId"),
    intersection_code: Optional[str] = Query(
        None, alias="areaCode", description="Filter by spat intersection code"
    ),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Spats:
    skip = page_size * (page_num - 1)
    total, data = crud.spat.get_multi_with_total(
        db,
        skip=skip,
        limit=page_size,
        intersection_id=intersection_id,
        name=name,
        rsu_id=rsu_id,
        intersection_code=intersection_code,
    )
    return schemas.Spats(total=total, data=[spat.to_dict() for spat in data])


@router.patch(
    "/{spat_id}",
    response_model=schemas.Spat,
    status_code=status.HTTP_200_OK,
    description="""
Update a Spat.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Spat, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    spat_id: int,
    spat_in: schemas.SpatUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Spat:
    spat_in_db = crud.spat.get(db, id=spat_id)
    if not spat_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Spat [id: {spat_id}] not found"
        )
    try:
        new_spat_in_db = crud.spat.update(db, db_obj=spat_in_db, obj_in=spat_in)
    except sql_exc.IntegrityError as ex:
        LOG.error(ex.args[0])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": 1116,
                "msg": "error",
                "detail": {
                    "intersection_id": spat_in.intersection_id,
                    "phase_id": spat_in.phase_id,
                },
            },
        )
    except sql_exc.DataError as ex:
        LOG.error(ex.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    spat_publish(spat_in_db)

    return new_spat_in_db.to_dict()
