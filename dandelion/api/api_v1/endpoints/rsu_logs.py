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

import time
from logging import LoggerAdapter
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.mqtt.service.log import log_down

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "",
    response_model=schemas.RSULog,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new RSU log.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.RSULog, "description": "Created"},
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
    rsu_log_in: schemas.RSULogCreate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSULog:
    rsus: List[models.RSU] = []
    for rsu_id in rsu_log_in.rsus:
        rus_in_db = crud.rsu.get(db, id=rsu_id)
        if not rus_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": status.HTTP_404_NOT_FOUND, "msg": f"RSU [id: {rsu_id}] not found"},
            )
        rsus.append(rus_in_db)

    log_in_db = crud.rsu_log.create_rsu_log(db, obj_in=rsu_log_in, rsus=rsus)

    timestamp = int(time.time())
    for rsu in rsus:
        data = log_in_db.mqtt_dict()
        data["rsuId"] = rsu.rsu_id
        data["rsuEsn"] = rsu.rsu_esn
        data["protocolVersion"] = rsu.version
        data["timestamp"] = timestamp
        data["ack"] = False
        log_down(data, rsu.rsu_esn)
    return log_in_db.to_all_dict()


@router.delete(
    "/{rsu_log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a RSULog.
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
    rsu_log_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    if not crud.rsu_log.get(db, id=rsu_log_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": status.HTTP_404_NOT_FOUND,
                "msg": f"RSULog [id: {rsu_log_id}] not found",
            },
        )
    crud.rsu_log.remove(db, id=rsu_log_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{rsu_log_id}",
    response_model=schemas.RSULog,
    status_code=status.HTTP_200_OK,
    description="""
Get a RSULog.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSULog, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    rsu_log_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSULog:
    rsu_log_in_db = crud.rsu_log.get(db, id=rsu_log_id)
    if not rsu_log_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": status.HTTP_404_NOT_FOUND,
                "msg": f"RSULog [id: {rsu_log_id}] not found",
            },
        )
    return rsu_log_in_db.to_all_dict()


@router.get(
    "",
    response_model=schemas.RSULogs,
    status_code=status.HTTP_200_OK,
    summary="List RSU Logs",
    description="""
Get all RSULogs.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSULogs, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all(
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSULogs:
    skip = page_size * (page_num - 1)
    total, data = crud.rsu_log.get_multi_with_total(db, skip=skip, limit=page_size)
    return schemas.RSULogs(total=total, data=[rsu_log.to_all_dict() for rsu_log in data])


@router.put(
    "/{rsu_log_id}",
    response_model=schemas.RSULog,
    status_code=status.HTTP_200_OK,
    description="""
Update a RSULog.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSULog, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    rsu_log_id: int,
    rsu_log_in: schemas.RSULogUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSULog:
    rsu_log_in_db = crud.rsu_log.get(db, id=rsu_log_id)
    if not rsu_log_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": status.HTTP_404_NOT_FOUND,
                "msg": f"RSULog [id: {rsu_log_id}] not found",
            },
        )

    rsus: List[models.RSU] = []
    for rsu_id in rsu_log_in.rsus:
        rus_in_db = crud.rsu.get(db, id=rsu_id)
        if not rus_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": status.HTTP_404_NOT_FOUND, "msg": f"RSU [id: {rsu_id}] not found"},
            )
        rsus.append(rus_in_db)

    log_in_db = crud.rsu_log.update_rsu_log(db, db_obj=rsu_log_in_db, obj_in=rsu_log_in, rsus=rsus)

    timestamp = int(time.time())
    for rsu in rsus:
        data = log_in_db.mqtt_dict()
        data["rsuId"] = rsu.rsu_id
        data["rsuEsn"] = rsu.rsu_esn
        data["protocolVersion"] = rsu.version
        data["timestamp"] = timestamp
        data["ack"] = False
        log_down(data, rsu.rsu_esn)
    return log_in_db.to_all_dict()
