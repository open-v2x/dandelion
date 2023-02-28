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

from sqlalchemy import Boolean, Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from dandelion.db.base_class import Base, DandelionBase
from dandelion.util import Optional as Optional_util


class Intersection(Base, DandelionBase):
    __tablename__ = "intersection"

    area_code = Column(String(64), ForeignKey("area.code", name="intersection_fk_area"))
    code = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(64), nullable=False)
    lng = Column(String(64), nullable=False)
    lat = Column(String(64), nullable=False)

    is_default = Column(Boolean, nullable=False, default=False)

    maps = relationship("Map", backref="intersection")
    rsus = relationship("RSU", backref="intersection")
    rsi_events = relationship("RSIEvent", backref="intersection")

    cameras = relationship("Camera", backref="intersection")
    radars = relationship("Radar", backref="intersection")
    lidars = relationship("Lidar", backref="intersection")
    spats = relationship("Spat", backref="intersection")

    __table_args__ = (UniqueConstraint("area_code", "name"),)

    def __repr__(self) -> str:
        return f"<Intersection(code='{self.code}', name='{self.name}')>"

    def to_dict(self):
        return dict(
            id=self.id,
            code=self.code,
            name=self.name,
            lng=self.lng,
            lat=self.lat,
            **self.to_area(),
        )

    def to_intersection(self):
        return dict(code=self.code, name=self.name)

    def to_area(self):
        return dict(
            countryCode=Optional_util.none(self.area)
            .map(lambda v: v.city)
            .map(lambda v: v.province)
            .map(lambda v: v.country)
            .map(lambda v: v.code)
            .get(),
            countryName=Optional_util.none(self.area)
            .map(lambda v: v.city)
            .map(lambda v: v.province)
            .map(lambda v: v.country)
            .map(lambda v: v.name)
            .get(),
            provinceCode=Optional_util.none(self.area)
            .map(lambda v: v.city)
            .map(lambda v: v.province)
            .map(lambda v: v.code)
            .get(),
            provinceName=Optional_util.none(self.area)
            .map(lambda v: v.city)
            .map(lambda v: v.province)
            .map(lambda v: v.name)
            .get(),
            cityCode=Optional_util.none(self.area)
            .map(lambda v: v.city)
            .map(lambda v: v.code)
            .get(),
            cityName=Optional_util.none(self.area)
            .map(lambda v: v.city)
            .map(lambda v: v.name)
            .get(),
            areaCode=Optional_util.none(self.area).map(lambda v: v.code).get(),
            areaName=Optional_util.none(self.area).map(lambda v: v.name).get(),
        )

    def to_all(self):
        return dict(intersectionCode=self.code, intersectionName=self.name, **self.to_area())
