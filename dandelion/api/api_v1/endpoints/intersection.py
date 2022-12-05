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
from dandelion.api.deps import OpenV2XHTTPException as HTTPException, error_handle

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.Intersection,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new intersection.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.Intersection, "description": "Created"},
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
    intersection_in: schemas.IntersectionCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Intersection:
    try:
        intersection_in_db = crud.intersection.create(db, obj_in=intersection_in)
    except (sql_exc.IntegrityError, sql_exc.DataError) as ex:
        raise error_handle(ex, "code", intersection_in.code)
    return intersection_in_db.to_dict()


@router.delete(
    "/{intersection_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a intersection.
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
    intersection_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    if not crud.intersection.get(db, id=intersection_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intersection [id: {intersection_id}] not found",
        )
    crud.intersection.remove(db, id=intersection_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{intersection_id}",
    response_model=schemas.Intersection,
    status_code=status.HTTP_200_OK,
    description="""
Get a Intersection.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Intersection, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    intersection_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Intersection:
    intersection_in_db = crud.intersection.get(db, id=intersection_id)
    if not intersection_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intersection [id: {intersection_id}] not found",
        )
    return intersection_in_db.to_dict()


@router.get(
    "",
    response_model=schemas.Intersections,
    status_code=status.HTTP_200_OK,
    summary="List Cameras",
    description="""
Get all Intersection.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Intersections, "description": "OK"},
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
        None,
        alias="name",
        description="Filter by intersection name. Fuzzy prefix query is supported",
    ),
    area_code: Optional[str] = Query(
        None, alias="areaCode", description="Filter by intersection area code"
    ),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Intersections:
    skip = page_size * (page_num - 1)
    total, data = crud.intersection.get_multi_with_total(
        db,
        skip=skip,
        limit=page_size,
        name=name,
        area_code=area_code,
    )
    return schemas.Intersections(
        total=total, data=[intersection.to_dict() for intersection in data]
    )


@router.put(
    "/{intersection_id}",
    response_model=schemas.Intersection,
    status_code=status.HTTP_200_OK,
    description="""
Update a Intersection.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Intersection, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    intersection_id: int,
    intersection_in: schemas.IntersectionUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUModel:
    intersection_in_db = crud.intersection.get(db, id=intersection_id)
    if not intersection_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intersection [id: {intersection_in_db}] not found",
        )
    try:
        new_intersection_in_db = crud.intersection.update(
            db, db_obj=intersection_in_db, obj_in=intersection_in
        )
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        raise error_handle(ex, "code", intersection_in.code)
    return new_intersection_in_db.to_dict()
