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

from sqlalchemy import JSON, Column, Integer, String

from dandelion.db.base_class import Base, DandelionBase


class SystemConfig(Base, DandelionBase):
    __tablename__ = "system_config"

    edge_site_id = Column(Integer, nullable=True, default=0)
    mqtt_config = Column(JSON, nullable=True)
    edge_site_external_ip = Column(String(64), nullable=True)
    center_dandelion_endpoint = Column(String(255), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<SystemConfig edge_site_id'{self.edge_site_id}', mqtt_config='{self.mqtt_config}'>"
        )

    def to_dict(self):
        return dict(
            id=self.id,
            edgeSiteID=self.edge_site_id,
            mqttConfig=self.mqtt_config,
            edgeSiteExternalIP=self.edge_site_external_ip,
            centerDandelionEedpoint=self.center_dandelion_endpoint,
        )
