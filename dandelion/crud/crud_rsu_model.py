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
from dandelion.models import RSUModel
from dandelion.schemas import RSUModelCreate, RSUModelUpdate


class CRUDRSUModel(CRUDBase[RSUModel, RSUModelCreate, RSUModelUpdate]):
    """"""

    def get_multi_with_total(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        name: Optional[str] = None,
        manufacturer: Optional[str] = None,
    ) -> Tuple[int, List[RSUModel]]:
        query_ = db.query(self.model)
        if name is not None:
            query_ = self.fuzz_filter(query_, self.model.name, name)
        if manufacturer is not None:
            query_ = self.fuzz_filter(query_, self.model.manufacturer, manufacturer)
        total = query_.count()
        if limit != -1:
            query_ = query_.offset(skip).limit(limit)
        data = query_.all()
        return total, data


rsu_model = CRUDRSUModel(RSUModel)
