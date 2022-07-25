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
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from oslo_log import log
from sqlalchemy import exc as sql_exc
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.mqtt.service.rsu.rsu_config import config_down

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.RSUConfig,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new RSU Config.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.RSUConfig, "description": "Created"},
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
    rsu_config_in: schemas.RSUConfigCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUConfig:
    rsus: List[models.RSU] = []
    rsu_dict: Dict[int, str] = dict()
    if rsu_config_in.rsus:
        for rsu_id in rsu_config_in.rsus:
            rsu_in_db = crud.rsu.get(db, id=rsu_id)
            if not rsu_in_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"RSU [id: {rsu_id}] not found",
                )
            crud.rsu_config_rsu.remove_by_rsu_id(db, rsu_id=rsu_id)
            rsu_dict[rsu_in_db.id] = rsu_in_db.rsu_esn
            rsus.append(rsu_in_db)

    try:
        rsu_config_in_db = crud.rsu_config.create_rsu_config(db, obj_in=rsu_config_in, rsus=rsus)
    except sql_exc.IntegrityError as ex:
        LOG.error(ex.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])

    # config down
    data = rsu_config_in_db.mqtt_dict()
    data["ack"] = True
    for rsu in rsu_config_in_db.rsus:
        data["seqNum"] = f"{rsu.id}"
        config_down(data, rsu_dict.get(rsu.rsu_id))

    return rsu_config_in_db.to_dict()


@router.delete(
    "/{rsu_config_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a RSUConfig.
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
    rsu_config_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    if not crud.rsu_config.get(db, id=rsu_config_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RSUConfig [id: {rsu_config_id}] not found",
        )
    crud.rsu_config.remove(db, id=rsu_config_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{rsu_config_id}",
    response_model=schemas.RSUConfigWithRSUs,
    status_code=status.HTTP_200_OK,
    description="""
Get a RSUConfig.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUConfigWithRSUs, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    rsu_config_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUConfigWithRSUs:
    rsu_config_in_db = crud.rsu_config.get(db, id=rsu_config_id)
    if not rsu_config_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RSUConfig [id: {rsu_config_id}] not found",
        )
    return rsu_config_in_db.to_all_dict()


@router.get(
    "",
    response_model=schemas.RSUConfigs,
    status_code=status.HTTP_200_OK,
    description="""
Get all RSUConfigs.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUConfigs, "description": "OK"},
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
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUConfigs:
    skip = page_size * (page_num - 1)
    total, data = crud.rsu_config.get_multi_with_total(db, skip=skip, limit=page_size, name=name)
    return schemas.RSUConfigs(total=total, data=[rsu_config.to_dict() for rsu_config in data])


@router.put(
    "/{rsu_config_id}",
    response_model=schemas.RSUConfig,
    status_code=status.HTTP_200_OK,
    description="""
Update a Radar.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUConfig, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    rsu_config_id: int,
    rsu_config_in: schemas.RSUConfigUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSUConfig:
    rsu_config_in_db = crud.rsu_config.get(db, id=rsu_config_id)
    if not rsu_config_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"RSUConfig [id: {rsu_config_id}] not found",
        )

    rsus: List[models.RSU] = []
    if rsu_config_in.rsus:
        for rsu_id in rsu_config_in.rsus:
            rus_in_db = crud.rsu.get(db, id=rsu_id)
            if not rus_in_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"RSU [id: {rsu_id}] not found",
                )
            rsus.append(rus_in_db)

    try:
        crud.rsu_config_rsu.remove_by_rsu_config_id(db, rsu_config_id=rsu_config_id)
        LOG.debug(f"Old RSU Config in db: {rsu_config_in_db.to_dict()}")
        new_rsu_config_in_db = crud.rsu_config.update_rsu_config(
            db, db_obj=rsu_config_in_db, obj_in=rsu_config_in, rsus=rsus
        )
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        LOG.error(ex.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])

    # config down
    data = new_rsu_config_in_db.mqtt_dict()
    data["ack"] = False
    for rsu in rsus:
        data["seqNum"] = f"{rsu.id}"
        config_down(data, rsu.rsu_esn)

    return new_rsu_config_in_db.to_dict()
