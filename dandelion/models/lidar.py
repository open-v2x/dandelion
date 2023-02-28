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


class Lidar(Base, DandelionBase):
    __tablename__ = "lidar"

    sn = Column(String(64), nullable=False, index=True, unique=True)
    name = Column(String(64), nullable=False, index=True, default="")
    lidar_ip = Column(String(15), nullable=False, default="")
    lng = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    elevation = Column(Float, nullable=False)
    towards = Column(Float, nullable=False)
    online_status = Column(Boolean, nullable=False, default=False)
    enabled = Column(Boolean, nullable=False, default=True)
    point = Column(String(15), nullable=False)
    pole = Column(String(15), nullable=False)
    rsu_id = Column(Integer, ForeignKey("rsu.id"))
    desc = Column(String(255), nullable=False, default="")
    ws_url = Column(String(50), nullable=False, default="")
    is_default = Column(Boolean, nullable=False, default=False)
    intersection_code = Column(
        String(64),
        ForeignKey("intersection.code", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Lidar (sn='{self.sn}', name='{self.name}')>"

    def to_dict(self):
        return {
            **dict(
                id=self.id,
                sn=self.sn,
                name=self.name,
                lidarIP=self.lidar_ip,
                lng=self.lng,
                lat=self.lat,
                elevation=self.elevation,
                towards=self.towards,
                onlineStatus=self.online_status,
                enabled=self.enabled,
                point=self.point,
                pole=self.pole,
                rsuId=self.rsu_id,
                rsuName=Optional_util.none(self.rsu).map(lambda v: v.rsu_name).get(),
                desc=self.desc,
                createTime=self.create_time,
                wsUrl=self.ws_url,
            ),
            **Optional_util.none(self.intersection).map(lambda v: v.to_all()).get(),
        }
