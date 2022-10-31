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
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Query, status
from oslo_log import log
from sqlalchemy import exc as sql_exc
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.api.deps import OpenV2XHTTPException as HTTPException
from dandelion.mqtt.service.mng import mng_down

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.get(
    "",
    response_model=schemas.MNGs,
    status_code=status.HTTP_200_OK,
    summary="List MNGs",
    description="""
Get all MNGs.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.MNGs, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all(
    rsu_name: Optional[str] = Query(
        None, alias="rsuName", description="Filter by rsuName. Fuzzy prefix query is supported"
    ),
    rsu_esn: Optional[str] = Query(None, alias="rsuEsn", description="Filter by rsuEsn"),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.MNGs:
    skip = page_size * (page_num - 1)
    total, data = crud.rsu.get_multi_with_total(
        db, skip=skip, limit=page_size, rsu_name=rsu_name, rsu_esn=rsu_esn
    )
    return schemas.MNGs(total=total, data=[rsu.mng.all_dict() for rsu in data])


@router.put(
    "/{mng_id}",
    response_model=schemas.MNG,
    status_code=status.HTTP_200_OK,
    description="""
Update a MNG.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.MNG, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    mng_id: int,
    mng_in: schemas.MNGUpdate,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.MNG:
    mng_in_db = crud.mng.get(db, id=mng_id)
    if not mng_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"MNG [id: {mng_id}] not found"
        )
    try:
        new_mng_in_db = crud.mng.update_mng(db, db_obj=mng_in_db, obj_in=mng_in)
    except (sql_exc.DataError, sql_exc.IntegrityError) as ex:
        LOG.error(ex.args[0])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.args[0])
    return new_mng_in_db.all_dict()


@router.post(
    "/{mng_id}/down",
    response_model=schemas.Message,
    status_code=status.HTTP_200_OK,
    description="""
Down a MNG.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Message, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def down(
    mng_id: int = Query(..., alias="mng_id", gt=0, description="MNG id"),
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Message:
    mng_in_db = crud.mng.get(db, id=mng_id)
    if not mng_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"MNG [id: {mng_id}] not found"
        )

    data = mng_in_db.mqtt_dict()
    data["timestamp"] = int(time.time())
    data["ack"] = False
    mng_down(mng_in_db.rsu.rsu_esn, data)
    return schemas.Message(detail={"code": status.HTTP_200_OK, "msg": "Send down for mng."})


@router.post(
    "/{mng_id}/copy",
    response_model=schemas.Message,
    status_code=status.HTTP_200_OK,
    description="""
Copy a MNG.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.Message, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def copy(
    mng_id: int = Query(..., alias="mng_id", gt=0, description="MNG id"),
    mng_copy_in: schemas.MNGCopy = Body(..., alias="mng_copy_in", description="MNG copy"),
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.Message:
    mng_in_db = crud.mng.get(db, id=mng_id)
    if not mng_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"MNG [id: {mng_id}] not found"
        )

    new_mngs: List[models.MNG] = []
    for rsu_id in mng_copy_in.rsus:
        new_mng_in_db = crud.mng.get_by_rsu_id(db, rsu_id=rsu_id)
        if not new_mng_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"MNG [by rsu id: {rsu_id}] not found",
            )
        new_mngs.append(new_mng_in_db)

    timestamp = int(time.time())
    for new_mng in new_mngs:
        new_mng = crud.mng.update(
            db,
            db_obj=new_mng,
            obj_in={
                "heartbeat_rate": mng_in_db.heartbeat_rate,
                "running_info_rate": mng_in_db.running_info_rate,
                "log_level": mng_in_db.log_level,
                "reboot": mng_in_db.reboot,
                "address_change": mng_in_db.address_change,
                "extend_config": mng_in_db.extend_config,
            },
        )
        data = new_mng.mqtt_dict()
        data["timestamp"] = timestamp
        data["ack"] = False
        mng_down(new_mng.rsu.rsu_esn, data)

    return schemas.Message(detail={"code": status.HTTP_200_OK, "msg": "Copy mng."})
