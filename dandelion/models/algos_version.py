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

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from dandelion.db.base_class import Base, DandelionBase


class AlgoVersion(Base, DandelionBase):
    __tablename__ = "algo_version"

    algo_id = Column(Integer, ForeignKey("algo_name.id"))
    version = Column(String(64), nullable=False)
    endpoint_id = Column(Integer, ForeignKey("endpoint.id"))

    __table_args__ = (UniqueConstraint("algo_id", "version"),)

    def __repr__(self) -> str:
        return f"<algo_version(version='{self.version}')>"

    def to_dict(self):
        return dict(id=self.id, version=self.version, endpoint_id=self.endpoint_id)

    def to_all_dict(self):
        return dict(
            id=self.id,
            version=self.version,
            algo=self.algo_name.name,
            module=self.algo_name.algo_module.module,
            endpoint_id=self.endpoint_id,
            endpoint_url=self.endpoint.url,
        )
