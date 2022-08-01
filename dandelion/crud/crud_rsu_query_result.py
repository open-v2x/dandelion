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

from typing import List

from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import RSUQueryResult
from dandelion.schemas import RSUQueryResultCreate, RSUQueryResultUpdate


class CRUDRSUQueryResult(CRUDBase[RSUQueryResult, RSUQueryResultCreate, RSUQueryResultUpdate]):
    """"""

    def get_multi_by_rsu_id(self, db: Session, *, rsu_id: int) -> List[RSUQueryResult]:
        return db.query(RSUQueryResult).filter(RSUQueryResult.rsu_id == rsu_id).all()

    def get_multi_by_query_id(self, db: Session, *, query_id: int) -> List[RSUQueryResult]:
        return db.query(RSUQueryResult).filter(RSUQueryResult.query_id == query_id).all()


rsu_query_result = CRUDRSUQueryResult(RSUQueryResult)
