# Copyright 2023 99Cloud, Inc. All Rights Reserved.
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
    response_model=schemas.ServiceCreateAll,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new service.

A service defines service name & description.
A group of endpoints (deferent versions or metadatas) belong to a service.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.ServiceCreateAll, "description": "Created"},
        **deps.RESPONSE_ERROR,
    },
)
def create(
    service_in: schemas.ServiceCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.ServiceCreateAll:
    try:
        new_service_in_db = crud.service.create(
            db,
            obj_in=schemas.ServiceCreate(
                name=service_in.name,
                type_id=service_in.type_id,
                vendor=service_in.vendor,
                description=service_in.description,
            ),
        )
    except sql_exc.IntegrityError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 1062, "msg": ex.args[0]},
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"msg": ex.args[0]},
        )
    return new_service_in_db.to_dict()


@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a service.
""",
    responses=deps.RESPONSE_ERROR,
    response_class=Response,
    response_description="No Content",
)
def delete(
    service_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    crud.service.remove(db, id=service_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{service_id}",
    status_code=status.HTTP_200_OK,
    description="""
get a service by ID.
""",
    responses=deps.RESPONSE_ERROR,
    response_model=schemas.ServiceGET,
    response_description="OK",
)
def get(
    service_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.ServiceGET:
    service = crud.service.get(db, id=service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return service.to_dict()


@router.put(
    "/{service_id}",
    response_model=schemas.ServiceGET,
    status_code=status.HTTP_200_OK,
    description="""
Update a service.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.ServiceGET, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def update(
    service_id: int,
    service_in: schemas.ServiceUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.ServiceGET:
    service_in_db = deps.crud_get(
        db=db, obj_id=service_id, crud_model=crud.service, detail="Service"
    )
    try:
        new_service_in_db = crud.service.update(db, db_obj=service_in_db, obj_in=service_in)
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        raise error_handle(ex, "name", service_in.name)
    return new_service_in_db.to_dict()


@router.get(
    "",
    response_model=schemas.Services,
    status_code=status.HTTP_200_OK,
    summary="List services",
    description="""
List services.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Services, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get_all(
    name: Optional[str] = Query(
        None, alias="name", description="Filter by name. Fuzzy prefix query is supported"
    ),
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Services:
    services = crud.service.get_all(db, name)
    return schemas.Services(total=len(services), data=services)
