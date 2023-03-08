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

from typing import List, Optional

from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import Area
from dandelion.schemas import AreaCreate, AreaUpdate


class CRUDArea(CRUDBase[Area, AreaCreate, AreaUpdate]):
    """"""

    def get_multi_by_city_code(
        self, db: Session, city_code: Optional[str] = None, *, skip: int = 0, limit: int = 100
    ) -> List[Area]:
        query_ = db.query(self.model)
        if city_code:
            query_ = query_.filter(Area.city_code == city_code)
        return query_.offset(skip).limit(limit).all()


area = CRUDArea(Area)
