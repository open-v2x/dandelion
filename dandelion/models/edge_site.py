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

from sqlalchemy import Column, ForeignKey, String

from dandelion.db.base_class import Base, DandelionBase


class EdgeSite(Base, DandelionBase):
    __tablename__ = "edge_site"

    name = Column(String(64), nullable=False, unique=True)
    edge_site_dandelion_endpoint = Column(String(64), nullable=False, unique=True)
    area_code = Column(String(64), ForeignKey("area.code", name="edgesite_fk_area"))
    desc = Column(String(255), nullable=True)

    def to_all_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            createTime=self.create_time,
            edgeSiteDandelionEndpoint=self.edge_site_dandelion_endpoint,
            areaCode=self.area_code,
            areaName=self.area.name if self.area else None,
            desc=self.desc,
            cityCode=self.area.city.code if self.area else None,
            cityName=self.area.city.name if self.area else None,
            provinceCode=self.area.city.province.code if self.area else None,
            provinceName=self.area.city.province.name if self.area else None,
            countryCode=self.area.city.province.country.code if self.area else None,
            countryName=self.area.city.province.country.name if self.area else None,
        )

    def __repr__(self) -> str:
        return f"<EdgeSite(name='{self.name}')>"
