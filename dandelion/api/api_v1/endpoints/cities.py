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
from typing import List

from fastapi import APIRouter, Depends, Query, status
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.get(
    "",
    response_model=List[schemas.City],
    status_code=status.HTTP_200_OK,
    description="""
Search city by province.
""",
    responses={
        status.HTTP_200_OK: {"model": List[schemas.City], "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def list(
    province_code: str = Query(..., description="Filter by provinceCode", alias="provinceCode"),
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> List[schemas.City]:
    cities = crud.city.get_multi_by_province_code(db, province_code)
    return [city for city in cities]
