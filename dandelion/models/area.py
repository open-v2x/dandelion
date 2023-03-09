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

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from dandelion.db.base_class import Base, DandelionBase
from dandelion.models.intersection import Intersection
from dandelion.util import Optional as Optional_util


class Area(Base, DandelionBase):
    __tablename__ = "area"

    city_code = Column(String(64), ForeignKey("city.code"))
    code = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(64), nullable=False)

    intersections: List[Intersection] = relationship("Intersection", backref="area")

    def __repr__(self) -> str:
        return f"<Area(code='{self.code}', name='{self.name}')>"

    def to_dict(self):
        return dict(code=self.code, name=self.name)

    def to_all(self):
        return dict(
            countryCode=Optional_util.none(self.city)
            .map(lambda v: v.province)
            .map(lambda v: v.country)
            .map(lambda v: v.code)
            .get(),
            countryName=Optional_util.none(self.city)
            .map(lambda v: v.province)
            .map(lambda v: v.country)
            .map(lambda v: v.name)
            .get(),
            provinceCode=Optional_util.none(self.city)
            .map(lambda v: v.province)
            .map(lambda v: v.code)
            .get(),
            provinceName=Optional_util.none(self.city)
            .map(lambda v: v.province)
            .map(lambda v: v.name)
            .get(),
            cityCode=Optional_util.none(self.city).map(lambda v: v.code).get(),
            cityName=Optional_util.none(self.city).map(lambda v: v.name).get(),
            areaCode=self.code,
            areaName=self.name,
        )

    def to_all_dict(self, need_intersection):
        return (
            {**self.to_dict()}
            if not need_intersection
            else {
                **self.to_dict(),
                "children": [
                    v.to_intersection() for v in self.intersections if v.is_default is False
                ],
            }
        )
