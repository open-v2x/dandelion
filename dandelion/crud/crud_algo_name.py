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
from dandelion.models import AlgoName
from dandelion.schemas.algo_name import AlgoNameCreate, AlgoNameUpdate


class CRUDAlgo(CRUDBase[AlgoName, AlgoNameCreate, AlgoNameUpdate]):
    """"""

    def get_by_name_and_module(self, db: Session, algo: str, module_id: int) -> AlgoName:
        return (
            db.query(self.model)
            .filter(self.model.name == algo, self.model.module_id == module_id)
            .first()
        )

    def get_multi_by_algo_name(
        self,
        db: Session,
        *,
        algo: Optional[str] = None,
    ) -> Tuple[int, List[AlgoName]]:
        query_ = db.query(self.model)
        if algo is not None:
            query_ = self.fuzz_filter(query_, self.model.name, algo)
        total = query_.count()
        data = query_.all()
        return total, data

    def get_multi_all(
        self,
        db: Session,
    ) -> List[AlgoName]:
        return db.query(self.model).all()


algo_name = CRUDAlgo(AlgoName)
