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

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String

from dandelion.db.base_class import Base, DandelionBase
from dandelion.util import Optional as Optional_util


class Camera(Base, DandelionBase):
    __tablename__ = "camera"

    sn = Column(String(64), nullable=False, index=True, unique=True)
    name = Column(String(64), nullable=False, index=True, default="")
    stream_url = Column(String(1024), nullable=False, default="")
    lng = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    elevation = Column(Float, nullable=False)
    towards = Column(Float, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    rsu_id = Column(Integer, ForeignKey("rsu.id"))
    desc = Column(String(255), nullable=False, default="")

    def __repr__(self) -> str:
        return f"<Camera(sn='{self.sn}', name='{self.name}')>"

    def to_dict(self):
        return {
            **dict(
                id=self.id,
                sn=self.sn,
                name=self.name,
                streamUrl=self.stream_url,
                lng=self.lng,
                lat=self.lat,
                elevation=self.elevation,
                towards=self.towards,
                rsuId=self.rsu_id,
                rsuName=Optional_util.none(self.rsu).map(lambda v: v.rsu_name).get(),
                desc=self.desc,
                createTime=self.create_time,
            ),
            **Optional_util.none(self.rsu)
            .map(lambda v: v.intersection)
            .map(lambda v: v.to_all())
            .get(),
        }
