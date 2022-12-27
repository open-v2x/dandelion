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

from sqlalchemy import Boolean, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from dandelion.db.base_class import Base, DandelionBase
from dandelion.models.algos_version import AlgoVersion


class AlgoName(Base, DandelionBase):
    __tablename__ = "algo_name"

    module = Column(String(64), ForeignKey("algo_module.module"))
    name = Column(String(64), nullable=False, index=True)
    enable = Column(Boolean, nullable=False, default=False)
    module_path = Column(String(64), nullable=False)
    in_use = Column(String(64), nullable=True)
    algo_versions: List[AlgoVersion] = relationship("AlgoVersion", backref="algo_name")

    __table_args__ = (UniqueConstraint("name", "module"),)

    def __repr__(self) -> str:
        return f"<algo_name(algo_name='{self.name}')>"

    def to_dict(self):
        version = {version.version: version.version_path for version in self.algo_versions}
        return {
            **dict(
                id=self.id,
                module=self.module,
                algo=self.name,
                enable=self.enable,
                modulePath=version.get(self.in_use)
                if self.in_use in version.keys()
                else self.module_path,
                inUse=self.in_use,
                version=[v.to_dict() for v in self.algo_versions],
                updateTime=self.update_time,
            ),
        }
