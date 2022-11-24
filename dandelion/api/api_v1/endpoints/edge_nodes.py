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

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import exc as sql_exc
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.api.deps import OpenV2XHTTPException as HTTPException

router = APIRouter()


@router.get(
    "",
    response_model=schemas.EdgeNodes,
    status_code=status.HTTP_200_OK,
    summary="List Edge Nodes",
    description="""
Get all Edge Nodes.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.EdgeNodes, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all(
    name: str = Query(None, alias="name", description=""),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EdgeNodes:
    skip = page_size * (page_num - 1)
    total, data = crud.edge_node.get_multi_with_total(
        db,
        skip=skip,
        limit=page_size,
        name=name,
    )
    return schemas.EdgeNodes(total=total, data=[node.to_all_dict() for node in data])


@router.post(
    "",
    response_model=schemas.EdgeNode,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new edge node.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.EdgeNode, "description": "Created"},
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
    edge_node_in: schemas.EdgeNodeCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EdgeNode:
    try:
        edge_node_in_db = crud.edge_node.create(db, obj_in=edge_node_in)
    except sql_exc.DataError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    return edge_node_in_db.to_all_dict()
