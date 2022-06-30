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
from typing import List, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import RSU, RSULog
from dandelion.schemas import RSULogCreate, RSULogUpdate


class CRUDRSULog(CRUDBase[RSULog, RSULogCreate, RSULogUpdate]):
    """"""

    def create_rsu_log(self, db: Session, *, obj_in: RSULogCreate, rsus: List[RSU]) -> RSULog:
        rsu_log = RSULog()
        rsu_log.upload_url = obj_in.upload_url
        rsu_log.user_id = obj_in.user_id
        rsu_log.password = obj_in.password
        rsu_log.transprotocal = obj_in.transprotocal

        obj_in_data = jsonable_encoder(rsu_log)
        db_obj = self.model(**obj_in_data)
        db_obj.rsus = rsus
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_rsu_log(
        self, db: Session, *, db_obj: RSULog, obj_in: RSULogUpdate, rsus: List[RSU]
    ) -> RSULog:
        obj_data = jsonable_encoder(db_obj)
        del obj_in.rsus
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.rsus = rsus
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
    ) -> Tuple[int, List[RSULog]]:
        query_ = db.query(self.model)
        total = query_.count()
        data = query_.offset(skip).limit(limit).all()
        return total, data


rsu_log = CRUDRSULog(RSULog)
