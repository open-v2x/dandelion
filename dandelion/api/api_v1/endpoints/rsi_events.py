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

from fastapi import APIRouter, Depends, HTTPException, Query, status
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.get(
    "/{event_id}",
    response_model=schemas.RSIEvent,
    status_code=status.HTTP_200_OK,
    description="""
Get a RSIEvent.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSIEvent, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get(
    event_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSIEvent:
    rsi_event_in_db = crud.rsi_event.get(db, id=event_id)
    if not rsi_event_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"RSIEvent [id: {event_id}] not found"
        )
    return rsi_event_in_db.to_all_dict()


@router.get(
    "",
    response_model=schemas.RSIEvents,
    status_code=status.HTTP_200_OK,
    summary="List RSI Events",
    description="""
Get all RSI Events.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSIEvents, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all(
    event_type: Optional[int] = Query(None, alias="eventType", description="Filter by eventType"),
    area_code: Optional[str] = Query(None, alias="areaCode", description="Filter by areaCode"),
    address: Optional[str] = Query(
        None, alias="address", description="Filter by address. Fuzzy prefix query is supported"
    ),
    page_num: int = Query(1, alias="pageNum", ge=1, description="Page number"),
    page_size: int = Query(10, alias="pageSize", ge=-1, description="Page size"),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.RSIEvents:
    skip = page_size * (page_num - 1)
    total, data = crud.rsi_event.get_multi_with_total(
        db, skip=skip, limit=page_size, event_type=event_type, area_code=area_code, address=address
    )
    return schemas.RSIEvents(total=total, data=[rsi_event.to_all_dict() for rsi_event in data])
