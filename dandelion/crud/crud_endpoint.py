# Copyright 2023 99Cloud, Inc. All Rights Reserved.
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
from dandelion.models import Endpoint
from dandelion.schemas.endpoint import EndpointCreate, EndpointUpdate


class CRUDEndpoint(CRUDBase[Endpoint, EndpointCreate, EndpointUpdate]):
    """"""

    def get_all(self, db: Session, enabled: Optional[bool]) -> List[Endpoint]:
        query_ = db.query(self.model)
        if enabled is not None:
            query_ = query_.filter(self.model.enabled == enabled)
        return query_.all()


endpoint = CRUDEndpoint(Endpoint)
