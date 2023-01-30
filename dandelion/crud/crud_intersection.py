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
from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import Intersection
from dandelion.schemas import IntersectionCreate, IntersectionUpdate


class CRUDIntersection(CRUDBase[Intersection, IntersectionCreate, IntersectionUpdate]):
    """"""

    def create(self, db: Session, *, obj_in: IntersectionCreate) -> Intersection:
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
        name: Optional[str] = None,
        area_code: Optional[str] = None,
    ) -> Tuple[int, List[Intersection]]:
        query_ = db.query(self.model).filter()
        if name is not None:
            query_ = self.fuzz_filter(query_, self.model.name, name)
        if area_code is not None:
            query_ = query_.filter(self.model.area_code == area_code)
        total = query_.count()
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data

    def get_by_code(self, db: Session, code: str) -> Optional[Intersection]:
        return db.query(self.model).filter(self.model.code == code).first()

    def get_by_name_and_area(
        self,
        db: Session,
        name: str,
        area_code: str,
    ) -> Optional[Intersection]:
        return (
            db.query(self.model)
            .filter(self.model.name == name, self.model.area_code == area_code)
            .first()
        )

    def get_by_code_and_id(
        self,
        db: Session,
        code: str,
        intersection_id: int,
    ) -> Optional[Intersection]:
        return (
            db.query(self.model)
            .filter(self.model.code == code, self.model.id != intersection_id)
            .first()
        )


intersection = CRUDIntersection(Intersection)
