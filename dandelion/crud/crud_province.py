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
from dandelion.models import Province
from dandelion.schemas import ProvinceCreate, ProvinceUpdate


class CRUDProvince(CRUDBase[Province, ProvinceCreate, ProvinceUpdate]):
    """"""

    def get_multi_by_country_code(
        self, db: Session, country_code: str, *, skip: int = 0, limit: int = 100
    ) -> List[Province]:
        return (
            db.query(self.model)
            .filter(Province.country_code == country_code)
            .offset(skip)
            .limit(limit)
            .all()
        )


province = CRUDProvince(Province)
