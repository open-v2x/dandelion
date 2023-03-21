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

from typing import List

from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import City
from dandelion.schemas import CityCreate, CityUpdate


class CRUDCity(CRUDBase[City, CityCreate, CityUpdate]):
    """"""

    def get_multi_by_province_code(
        self, db: Session, province_code: str, *, skip: int = 0, limit: int = 100
    ) -> List[City]:
        return (
            db.query(self.model)
            .filter(City.province_code == province_code)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_with_total(
        self,
        db: Session,
    ) -> List[City]:
        return db.query(self.model).all()


city = CRUDCity(City)
