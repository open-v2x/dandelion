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

from sqlalchemy import JSON, Column, ForeignKey, Integer, String

from dandelion.db.base_class import Base, DandelionBase


class EdgeNodeRSU(Base, DandelionBase):
    __tablename__ = "edge_node_rsu"

    edge_node_id = Column(Integer, ForeignKey("edge_node.id"))
    area_code = Column(String(64), ForeignKey("area.code"))
    name = Column(String(64), nullable=False, index=True)
    esn = Column(String(64), nullable=False, index=True)
    location = Column(JSON, nullable=False)
    edge_rsu_id = Column(Integer, nullable=False)

    def to_all_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            esn=self.esn,
            location=self.location,
            createTime=self.create_time,
        )

    def __repr__(self) -> str:
        return f"<EdgeNodeRSU(name='{self.name}', esn='{self.esn}')>"
