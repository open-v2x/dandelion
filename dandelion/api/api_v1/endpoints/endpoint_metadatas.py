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
    response_model=schemas.EndpointMetadataCreateAll,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new endpoint_metadata.

A endpoint_metadata defines endpoint key-value pairs.
A group of endpoint metadatas key-value pairs belong to a endpoint.
""",
    responses={
        status.HTTP_201_CREATED: {
            "model": schemas.EndpointMetadataCreateAll,
            "description": "Created",
        },
        **deps.RESPONSE_ERROR,
    },
)
def create(
    endpoint_metadata_in: schemas.EndpointMetadataCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EndpointMetadataCreateAll:
    try:
        new_endpoint_metadata_in_db = crud.endpoint_metadata.create(
            db,
            obj_in=schemas.EndpointMetadataCreate(
                endpoint_id=endpoint_metadata_in.endpoint_id,
                key=endpoint_metadata_in.key,
                value=endpoint_metadata_in.value,
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
    return new_endpoint_metadata_in_db.to_dict()


@router.delete(
    "/{endpoint_metadata_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a endpoint_metadata.
""",
    responses=deps.RESPONSE_ERROR,
    response_class=Response,
    response_description="No Content",
)
def delete(
    endpoint_metadata_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    crud.endpoint_metadata.remove(db, id=endpoint_metadata_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{endpoint_metadata_id}",
    status_code=status.HTTP_200_OK,
    description="""
get a endpoint_metadata by ID.
""",
    responses=deps.RESPONSE_ERROR,
    response_model=schemas.EndpointMetadataGET,
    response_description="OK",
)
def get(
    endpoint_metadata_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EndpointMetadataGET:
    endpoint_metadata = crud.endpoint_metadata.get(db, id=endpoint_metadata_id)
    if not endpoint_metadata:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return endpoint_metadata.to_dict()


@router.put(
    "/{endpoint_metadata_id}",
    response_model=schemas.EndpointMetadataGET,
    status_code=status.HTTP_200_OK,
    description="""
Update a endpoint_metadata.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.EndpointMetadataGET, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def update(
    endpoint_metadata_id: int,
    endpoint_metadata_in: schemas.EndpointMetadataUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EndpointMetadataGET:
    endpoint_metadata_in_db = deps.crud_get(
        db=db,
        obj_id=endpoint_metadata_id,
        crud_model=crud.endpoint_metadata,
        detail="EndpointMetadata",
    )
    try:
        new_endpoint_metadata_in_db = crud.endpoint_metadata.update(
            db, db_obj=endpoint_metadata_in_db, obj_in=endpoint_metadata_in
        )
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        raise error_handle(ex, "key", endpoint_metadata_in.key)
    return new_endpoint_metadata_in_db.to_dict()


@router.get(
    "",
    response_model=schemas.EndpointMetadatas,
    status_code=status.HTTP_200_OK,
    summary="List endpoint metadatas",
    description="""
List endpoint_metadatas.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.EndpointMetadatas, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get_all(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EndpointMetadatas:
    endpoint_metadatas = crud.endpoint_metadata.get_all(db)
    return schemas.EndpointMetadatas(total=len(endpoint_metadatas), data=endpoint_metadatas)
