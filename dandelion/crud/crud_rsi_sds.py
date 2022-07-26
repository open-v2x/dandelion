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

from typing import List, Optional, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc
from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import RSISDS
from dandelion.schemas import RSISDSCreate


class CRUDRSISDS(CRUDBase[RSISDS, RSISDSCreate, RSISDSCreate]):
    def create(self, db: Session, *, obj_in: RSISDSCreate) -> RSISDS:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_with_total(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        equipment_type: Optional[int] = None,
    ) -> Tuple[int, List[RSISDS]]:
        query_ = db.query(self.model)
        if equipment_type is not None:
            query_ = query_.filter(self.model.equipment_type == equipment_type)
        total = query_.count()
        query_ = query_.order_by(desc(self.model.id))
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data


rsi_sds = CRUDRSISDS(RSISDS)
