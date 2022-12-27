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

from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import AlgoVersion
from dandelion.schemas.algo_version import AlgoVersionCreate, AlgoVersionUpdate


class CRUDAlgo(CRUDBase[AlgoVersion, AlgoVersionCreate, AlgoVersionUpdate]):
    """"""

    def get_by_version(self, db: Session, version: str) -> AlgoVersion:
        return db.query(self.model).filter(self.model.version == version).first()

    def get_by_algo(self, db: Session, algo: str) -> AlgoVersion:
        return db.query(self.model).filter(self.model.algo == algo).all()


algo_version = CRUDAlgo(AlgoVersion)
