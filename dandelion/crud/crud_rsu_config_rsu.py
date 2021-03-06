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

from typing import Optional

from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import RSUConfigRSU
from dandelion.schemas import RSUConfigRSUCreate, RSUConfigRSUUpdate


class CRUDRSUConfigRSU(CRUDBase[RSUConfigRSU, RSUConfigRSUCreate, RSUConfigRSUUpdate]):
    """"""

    def remove_by_rsu_config_id(self, db: Session, *, rsu_config_id: int) -> None:
        db.query(self.model).filter(self.model.rsu_config_id == rsu_config_id).delete()
        db.commit()

    def remove_by_rsu_id(self, db: Session, *, rsu_id: int) -> None:
        db.query(self.model).filter(self.model.rsu_id == rsu_id).delete()
        db.commit()

    def update_status_by_id(
        self,
        db: Session,
        *,
        id: int,
        status: int,
    ) -> Optional[RSUConfigRSU]:
        config_rsu = self.get(db, id)
        if config_rsu:
            config_rsu.status = status
            db.add(config_rsu)
            db.commit()
            db.refresh(config_rsu)
        return config_rsu


rsu_config_rsu = CRUDRSUConfigRSU(RSUConfigRSU)
