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


class SystemConfig(Base, DandelionBase):
    __tablename__ = "system_config"

    name = Column(String(length=255), nullable=True, default="")
    node_id = Column(Integer, nullable=True, default=0)
    mqtt_config = Column(JSON, nullable=True)
    area_code = Column(String(64), ForeignKey("area.code", name="edge_fk_area"))
    local_ip = Column(String(64), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<SystemConfig(name='{self.name}', "
            f"node_id='{self.node_id}', "
            f"mqtt_config='{self.mqtt_config}'>"
        )
