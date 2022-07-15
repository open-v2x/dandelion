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

from typing import Any

from sqlalchemy.orm import Session

from dandelion.crud.base import CRUDBase
from dandelion.models import SystemConfig
from dandelion.schemas import SystemConfigCreate


class CRUDSystemConfig(CRUDBase[SystemConfig, SystemConfigCreate, SystemConfigCreate]):
    def update_node_id(self, db: Session, *, _id: int, node_id: int) -> Any:
        _system_config: SystemConfig = db.query(self.model).filter(self.model.id == _id).first()
        if _system_config:
            _system_config.node_id = node_id
            db.add(_system_config)
            db.commit()
            db.refresh(_system_config)
        return _system_config


system_config = CRUDSystemConfig(SystemConfig)
