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
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import MNG
from dandelion.schemas import MNGCreate, MNGUpdate


class CRUDMNG(CRUDBase[MNG, MNGCreate, MNGUpdate]):
    """"""

    def update_mng(self, db: Session, *, db_obj: MNG, obj_in: MNGUpdate) -> MNG:
        obj_data = jsonable_encoder(db_obj)
        update_data = jsonable_encoder(obj_in, by_alias=False)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.update_time = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_rsu_id(self, db: Session, *, rsu_id: int) -> Optional[MNG]:
        return db.query(MNG).filter(MNG.rsu_id == rsu_id).first()


mng = CRUDMNG(MNG)
