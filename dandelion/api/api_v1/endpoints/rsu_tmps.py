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

from fastapi import APIRouter, Depends, Query, Response, status
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.get(
    "",
    response_model=schemas.RSUTMPs,
    status_code=status.HTTP_200_OK,
    summary="List TMP RSUs",
    description="""
Get all TMP RSUs.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.RSUTMPs, "description": "OK"},
        **deps.RESPONSE_ERROR,
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
) -> schemas.RSUTMPs:
    skip = page_size * (page_num - 1)
    total, data = crud.rsu_tmp.get_multi_with_total(
        db, skip=skip, limit=page_size, rsu_name=rsu_name, rsu_esn=rsu_esn
    )
    return schemas.RSUTMPs(total=total, data=[rsu_tmp.to_dict() for rsu_tmp in data])


@router.delete(
    "/{rsu_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a TMP RSU.
""",
    responses=deps.RESPONSE_ERROR,
    response_class=Response,
    response_description="No Content",
)
def delete(
    rsu_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    deps.crud_get(db=db, obj_id=rsu_id, crud_model=crud.rsu_tmp, detail="TMP RSU")
    crud.rsu_tmp.remove(db, id=rsu_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)
