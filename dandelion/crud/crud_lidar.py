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

from typing import List, Optional, Tuple, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import RSU, Lidar
from dandelion.schemas import LidarCreate, LidarEnabledUpdate, LidarUpdate


class CRUDLidar(CRUDBase[Lidar, LidarCreate, Union[LidarUpdate, LidarEnabledUpdate]]):
    """"""

    def create(self, db: Session, *, obj_in: LidarCreate) -> Lidar:
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
        sn: Optional[str] = None,
        name: Optional[str] = None,
        rsu_id: Optional[int] = None,
        area_code: Optional[str] = None,
        rsu_esn: Optional[str] = None,
    ) -> Tuple[int, List[Lidar]]:
        query_ = db.query(self.model).join(RSU, self.model.rsu_id == RSU.id)
        if sn is not None:
            query_ = query_.filter(self.model.sn.like(f"%{sn}%"))
        if name is not None:
            query_ = query_.filter(self.model.name.like(f"%{name}%"))
        if rsu_id is not None:
            query_ = query_.filter(self.model.rsu_id == rsu_id)
        if area_code is not None:
            query_ = query_.filter(RSU.area_code == area_code)
        if rsu_esn is not None:
            query_ = query_.filter(RSU.rsu_esn.like(f"%{rsu_esn}%"))
        total = query_.count()
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data


lidar = CRUDLidar(Lidar)
