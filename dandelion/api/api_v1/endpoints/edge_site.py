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

import os

import requests
from fastapi import APIRouter, Depends, Query, Response, status
from oslo_config import cfg
from sqlalchemy import exc as sql_exc
from sqlalchemy.orm import Session

from dandelion import constants, crud, models, schemas
from dandelion.api import deps
from dandelion.api.deps import OpenV2XHTTPException as HTTPException, error_handle

router = APIRouter()
CONF: cfg = cfg.CONF


@router.get(
    "",
    response_model=schemas.EdgeSites,
    status_code=status.HTTP_200_OK,
    summary="List Edge Sites",
    description="""
Get all Edge Sites.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.EdgeSites, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def get_all(
    name: str = Query(None, alias="name", description=""),
    area_code: str = Query(None, alias="areaCode", description=""),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EdgeSites:
    skip = page_size * (page_num - 1)
    total, data = crud.edge_site.get_multi_with_total(
        db, skip=skip, limit=page_size, name=name, area_code=area_code
    )
    return schemas.EdgeSites(total=total, data=[node.to_all_dict() for node in data])


@router.post(
    "",
    response_model=schemas.EdgeSite,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new edge site.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.EdgeSite, "description": "Created"},
        **deps.RESPONSE_ERROR,
    },
)
def create(
    edge_node_in: schemas.EdgeSiteCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    token: str = Depends(deps.reusable_oauth2),
) -> schemas.EdgeSite:
    try:
        edge_node_in_db = crud.edge_site.create(db, obj_in=edge_node_in)
    except sql_exc.DataError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    body_data = {
        "edgeSiteID": edge_node_in_db.id,
        "mqttConfig": {
            "host": CONF.mqtt.host,
            "port": CONF.mqtt.port,
            "username": CONF.mqtt.username,
            "password": CONF.mqtt.password,
        },
        "centerDandelionEndpoint": edge_node_in.center_dandelion_endpoint,
    }
    url = os.path.join(
        edge_node_in_db.edge_site_dandelion_endpoint,
        constants.API_V1_STR.strip("/"),
        "system_configs",
    )
    edge_create_res = requests.post(
        url=url, json=body_data, headers={"Authorization": f"bearer {token}"}
    )
    if edge_create_res.status_code != status.HTTP_200_OK:
        crud.edge_site.remove(db=db, id=edge_node_in_db.id)
        raise HTTPException(status_code=edge_create_res.status_code, detail=edge_create_res.json())
    return edge_node_in_db.to_all_dict()


@router.patch(
    "/{edge_site_id}",
    response_model=schemas.EdgeSite,
    status_code=status.HTTP_200_OK,
    description="""
Update a edge site.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.EdgeSite, "description": "OK"},
        **deps.RESPONSE_ERROR,
    },
)
def update(
    edge_site_id: int,
    edge_site_in: schemas.EdgeSiteUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.EdgeSite:
    edge_site_in_db = deps.crud_get(
        db=db, obj_id=edge_site_id, crud_model=crud.edge_site, detail="Edge Site"
    )
    try:
        new_edge_site_in_db = crud.edge_site.update(
            db, db_obj=edge_site_in_db, obj_in=edge_site_in
        )
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        raise error_handle(ex, "name", edge_site_in.name)
    return new_edge_site_in_db.to_all_dict()


@router.delete(
    "/{edge_site_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a Edge Site.
""",
    responses=deps.RESPONSE_ERROR,
    response_class=Response,
    response_description="No Content",
)
def delete(
    edge_site_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    deps.crud_get(db=db, obj_id=edge_site_id, crud_model=crud.edge_site, detail="Edge Site")
    crud.edge_site.remove(db, id=edge_site_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
