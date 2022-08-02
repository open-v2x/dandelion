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
from dandelion.models import RSICWM
from dandelion.schemas import RSICWMCreate
from dandelion.schemas.utils import Sort


class CRUDRSICWM(CRUDBase[RSICWM, RSICWMCreate, RSICWMCreate]):
    def create(self, db: Session, *, obj_in: RSICWMCreate) -> RSICWM:
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
        sort: Sort = Sort.desc,
        event_type: Optional[int] = 0,
        collision_type: Optional[int],
    ) -> Tuple[int, List[RSICWM]]:
        query_ = db.query(self.model)
        if event_type is not None:
            query_ = query_.filter(self.model.event_type == event_type)
        if collision_type is not None:
            query_ = query_.filter(self.model.collision_type == collision_type)
        total = query_.count()
        if sort == Sort.asc:
            query_ = query_.order_by(self.model.id)
        else:
            query_ = query_.order_by(desc(self.model.id))
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data


rsi_cwm = CRUDRSICWM(RSICWM)
