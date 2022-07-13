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

from typing import List, Tuple

from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import RSUQuery
from dandelion.schemas import RSUQueryCreate, RSUQueryUpdate


class CRUDRSUQuery(CRUDBase[RSUQuery, RSUQueryCreate, RSUQueryUpdate]):
    """"""

    def get_multi_with_total(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
    ) -> Tuple[int, List[RSUQuery]]:
        query_ = db.query(self.model)
        total = query_.count()
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data

    def create(self, db: Session, *, obj_in: RSUQueryCreate) -> RSUQuery:
        db_obj = RSUQuery()
        db_obj.query_type = obj_in.query_type
        db_obj.time_type = obj_in.time_type
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


rsu_query = CRUDRSUQuery(RSUQuery)
