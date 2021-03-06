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

from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import MapRSU
from dandelion.schemas import MapRSUCreate, MapRSUUpdate


class CRUDMapRSU(CRUDBase[MapRSU, MapRSUCreate, MapRSUUpdate]):
    """"""

    def get_by_rsu_id(self, db: Session, *, rsu_id: int) -> MapRSU:
        return db.query(self.model).filter(self.model.rsu_id == rsu_id).first()

    def get_multi_with_total(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        map_id: Optional[int] = None,
    ) -> Tuple[int, List[MapRSU]]:
        query_ = db.query(self.model)
        if map_id is not None:
            query_ = query_.filter(self.model.map_id == map_id)
        total = query_.count()
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data

    def update_status_by_id(
        self,
        db: Session,
        *,
        id: int,
        status: int,
    ) -> Optional[MapRSU]:
        map_rsu = self.get(db, id)
        if map_rsu:
            map_rsu.status = status
            db.add(map_rsu)
            db.commit()
            db.refresh(map_rsu)
        return map_rsu


map_rsu = CRUDMapRSU(MapRSU)
