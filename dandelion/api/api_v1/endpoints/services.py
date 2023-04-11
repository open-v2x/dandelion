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

from fastapi import APIRouter, Depends, Response, status
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
    response_model=schemas.ServiceTypeCreateAll,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new service type.

A service type defines service protocol & interface description.
A group of services belong to (share) a pre-defined service type.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.ServiceTypeCreateAll, "description": "Created"},
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
    service_type_in: schemas.ServiceTypeCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.ServiceTypeCreateAll:
    try:
        new_service_type_in_db = crud.service_type.create(
            db,
            obj_in=schemas.ServiceTypeCreate(
                name=service_type_in.name, description=service_type_in.description
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
    return new_service_type_in_db.to_dict()


@router.delete(
    "/{service_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a service type.
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
    service_type_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    crud.service_type.remove(db, id=service_type_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{service_type_id}",
    status_code=status.HTTP_200_OK,
    description="""
get a service type by ID.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
    response_model=schemas.ServiceTypeGET,
    response_description="OK",
)
def get(
    service_type_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.ServiceTypeGET:
    service_type = crud.service_type.get(db, id=service_type_id)
    if not service_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return service_type.to_dict()


@router.put(
    "/{service_type_id}",
    response_model=schemas.ServiceTypeGET,
    status_code=status.HTTP_200_OK,
    description="""
Update a service type.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.ServiceTypeGET, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    service_type_id: int,
    service_type_in: schemas.ServiceTypeUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.ServiceTypeGET:
    service_type_in_db = deps.crud_get(
        db=db, obj_id=service_type_id, crud_model=crud.service_type, detail="Service type"
    )
    try:
        new_service_type_in_db = crud.service_type.update(
            db, db_obj=service_type_in_db, obj_in=service_type_in
        )
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        raise error_handle(ex, "name", service_type_in.name)
    return new_service_type_in_db.to_dict()


@router.get(
    "",
    response_model=schemas.ServiceTypes,
    status_code=status.HTTP_200_OK,
    summary="List service types",
    description="""
List service types.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.ServiceTypes, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.ServiceTypes:
    service_types = crud.service_type.get_all(db)
    return schemas.ServiceTypes(total=len(service_types), data=service_types)
