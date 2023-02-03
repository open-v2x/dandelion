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

from datetime import datetime
from typing import List, Optional, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import Map
from dandelion.schemas import MapCreate, MapUpdate


class CRUDMap(CRUDBase[Map, MapCreate, MapUpdate]):
    """"""

    def update_map(self, db: Session, *, db_obj: Map, obj_in: MapUpdate) -> Map:
        obj_data = jsonable_encoder(db_obj, by_alias=False)
        update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("data"):
            update_data["lng"] = update_data.get("data", {}).get("refPos", {}).get("lon", 0.0)
            update_data["lat"] = update_data.get("data", {}).get("refPos", {}).get("lat", 0.0)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.update_time = datetime.utcnow()
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
        intersection_code: Optional[str] = None,
    ) -> Tuple[int, List[Map]]:
        query_ = db.query(self.model)
        if name is not None:
            query_ = self.fuzz_filter(query_, self.model.name, name)
        if intersection_code is not None:
            query_ = query_.filter(self.model.intersection_code == intersection_code)
        total = query_.count()
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data

    def get_with_bitmap(
        self,
        db: Session,
        *,
        bitmap_filename: str,
    ) -> Optional[Map]:
        return db.query(self.model).filter(self.model.bitmap_filename == bitmap_filename).first()

    def get_list_bitmap(self, db: Session):
        return db.execute(
            select(self.model.bitmap_filename).where(self.model.bitmap_filename.isnot(None))
        ).all()

    def get_with_intersection_code(
        self,
        db: Session,
        *,
        intersection_code: str,
    ) -> Optional[Map]:
        return (
            db.query(self.model).filter(self.model.intersection_code == intersection_code).first()
        )


map = CRUDMap(Map)
