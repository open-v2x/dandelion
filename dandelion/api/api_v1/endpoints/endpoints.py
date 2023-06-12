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
    response_model=schemas.EndpointCreateAll,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new endpoint.

A endpoint defines endpoint url.
A group of endpoints (deferent url & metadatas) belong to a service.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.EndpointCreateAll, "description": "Created"},
        **deps.RESPONSE_ERROR,
    },
)
def create(
    endpoint_in: schemas.EndpointCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EndpointCreateAll:
    try:
        new_endpoint_in_db = crud.endpoint.create(
            db,
            obj_in=schemas.EndpointCreate(
                service_id=endpoint_in.service_id,
                enabled=endpoint_in.enabled,
                url=endpoint_in.url,
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
    return new_endpoint_in_db.to_dict()


@router.delete(
    "/{endpoint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a endpoint.
""",
    responses=deps.RESPONSE_ERROR,
    response_class=Response,
    response_description="No Content",
)
def delete(
    endpoint_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    crud.endpoint.remove(db, id=endpoint_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{endpoint_id}",
    status_code=status.HTTP_200_OK,
    description="""
get a endpoint by ID.
""",
    responses=deps.RESPONSE_ERROR,
    response_model=schemas.EndpointGET,
    response_description="OK",
)
def get(
    endpoint_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EndpointGET:
    endpoint = crud.endpoint.get(db, id=endpoint_id)
    if not endpoint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return endpoint.to_dict()


@router.put(
    "/{endpoint_id}",
    response_model=schemas.EndpointGET,
    status_code=status.HTTP_200_OK,
    description="""
Update a endpoint.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.EndpointGET, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def update(
    endpoint_id: int,
    endpoint_in: schemas.EndpointUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EndpointGET:
    endpoint_in_db = deps.crud_get(
        db=db, obj_id=endpoint_id, crud_model=crud.endpoint, detail="Endpoint"
    )
    try:
        new_endpoint_in_db = crud.endpoint.update(db, db_obj=endpoint_in_db, obj_in=endpoint_in)
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        raise error_handle(ex, "url", endpoint_in.url)
    return new_endpoint_in_db.to_dict()


@router.get(
    "",
    response_model=schemas.Endpoints,
    status_code=status.HTTP_200_OK,
    summary="List endpoints",
    description="""
List endpoints.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Endpoints, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get_all(
    enabled: Optional[bool] = Query(None, alias="enabled", description="enabled"),
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Endpoints:
    endpoints = crud.endpoint.get_all(db, enabled)
    return schemas.Endpoints(total=len(endpoints), data=endpoints)
