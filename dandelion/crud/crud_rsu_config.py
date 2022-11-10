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
from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import RSU, RSUConfig, RSUConfigRSU
from dandelion.schemas import RSUConfigCreate, RSUConfigUpdate


class CRUDRSUConfig(CRUDBase[RSUConfig, RSUConfigCreate, RSUConfigUpdate]):
    """"""

    def create_rsu_config(
        self, db: Session, *, obj_in: RSUConfigCreate, rsus: List[RSU]
    ) -> RSUConfig:
        del obj_in.rsus
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db_obj.rsus = [RSUConfigRSU.create(rsu_, db_obj) for rsu_ in rsus]
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_rsu_config(
        self, db: Session, *, db_obj: RSUConfig, obj_in: RSUConfigUpdate, rsus: List[RSU]
    ) -> RSUConfig:
        obj_data = jsonable_encoder(db_obj)
        del obj_in.rsus
        update_data = jsonable_encoder(obj_in, by_alias=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.rsus = [RSUConfigRSU.create(rsu_, db_obj) for rsu_ in rsus]
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
    ) -> Tuple[int, List[RSUConfig]]:
        query_ = db.query(self.model)
        if name is not None:
            query_ = self.fuzz_filter(query_, self.model.name, name)
        total = query_.count()
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data


rsu_config = CRUDRSUConfig(RSUConfig)
