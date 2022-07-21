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
from dandelion.crud.utils import get_mng_default
from dandelion.models import RSU, RSUTMP
from dandelion.schemas import (
    RSUCreate,
    RSUUpdate,
    RSUUpdateWithBaseInfo,
    RSUUpdateWithStatus,
    RSUUpdateWithVersion,
)


class CRUDRSU(CRUDBase[RSU, RSUCreate, RSUUpdate]):
    """"""

    def update_online_status(
        self, db: Session, *, db_obj: RSU, obj_in: RSUUpdateWithStatus
    ) -> RSU:
        obj_data = jsonable_encoder(db_obj, by_alias=False)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.update_time = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_version(
        self, db: Session, *, db_obj: RSU, obj_in: RSUUpdateWithVersion
    ) -> RSU:
        obj_data = jsonable_encoder(db_obj, by_alias=False)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.update_time = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_base_info(
        self, db: Session, *, db_obj: RSU, obj_in: RSUUpdateWithBaseInfo
    ) -> RSU:
        obj_data = jsonable_encoder(db_obj, by_alias=False)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.update_time = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_rsu(
        self, db: Session, *, obj_in: RSUCreate, rsu_tmp_in_db: Optional[RSUTMP]
    ) -> RSU:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        obj_in_data["version"] = "" if rsu_tmp_in_db is None else rsu_tmp_in_db.version
        obj_in_data["location"] = {} if rsu_tmp_in_db is None else rsu_tmp_in_db.location
        obj_in_data["config"] = {} if rsu_tmp_in_db is None else rsu_tmp_in_db.config
        obj_in_data["rsu_status"] = "" if rsu_tmp_in_db is None else rsu_tmp_in_db.rsu_status
        obj_in_data["online_status"] = False
        obj_in_data["mng"] = get_mng_default()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_first(self, db: Session) -> RSU:
        return db.query(self.model).first()

    def get_by_rsu_esn(self, db: Session, *, rsu_esn: str) -> RSU:
        return db.query(self.model).filter(self.model.rsu_esn == rsu_esn).first()

    def get_multi_with_total(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        rsu_name: Optional[str] = None,
        rsu_esn: Optional[str] = None,
        area_code: Optional[str] = None,
        online_status: Optional[bool] = None,
        rsu_status: Optional[str] = None,
    ) -> Tuple[int, List[RSU]]:
        query_ = db.query(self.model)
        if rsu_name is not None:
            query_ = query_.filter(self.model.rsu_name.like(f"{rsu_name}%"))
        if rsu_esn is not None:
            query_ = query_.filter(self.model.rsu_esn.like(f"{rsu_esn}%"))
        if area_code is not None:
            query_ = query_.filter(self.model.area_code == area_code)
        if online_status is not None:
            query_ = query_.filter(self.model.online_status == online_status)
        if rsu_status is not None:
            query_ = query_.filter(self.model.rsu_status == rsu_status)
        total = query_.count()
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data


rsu = CRUDRSU(RSU)
