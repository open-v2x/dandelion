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

from sqlalchemy import JSON, Column, Float, ForeignKey, String
from sqlalchemy.orm import deferred, relationship

from dandelion.db.base_class import Base, DandelionBase
from dandelion.util import Optional as Optional_util


class Map(Base, DandelionBase):
    __tablename__ = "map"

    name = Column(String(64), nullable=False, index=True, unique=True)
    intersection_code = Column(String(64), ForeignKey("intersection.code"))
    desc = Column(String(255), nullable=False, default="")
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    data = deferred(Column(JSON, nullable=True))
    rsus = relationship("MapRSU", backref="map")
    bitmap_filename = Column(String(64), nullable=True)

    def __repr__(self) -> str:
        return f"<Map(name='{self.name}')>"

    def to_dict(self):
        return {
            **dict(
                id=self.id,
                name=self.name,
                desc=self.desc,
                amount=len(self.rsus),
                lat=self.lat,
                lng=self.lng,
                createTime=self.create_time,
            ),
            **Optional_util.none(self.intersection).map(lambda v: v.to_all()).orElse({}),
        }
