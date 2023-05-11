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


class RadarCamera(Base, DandelionBase):
    __tablename__ = "radar_camera"

    name = Column(String(64), nullable=False, index=True, unique=True)
    sn = Column(String(64), nullable=False, index=True, unique=True)
    lng = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    elevation = Column(Float, nullable=False)
    towards = Column(Float, nullable=False)
    point = Column(String(15), nullable=False, doc="点位")
    pole = Column(String(15), nullable=False, doc="杆位")
    video_stream_address = Column(String(255), nullable=False, doc="视频流地址")
    radar_camera_ip = Column(String(15), nullable=False, default="")
    rsu_id = Column(Integer, ForeignKey("rsu.id"))

    status = Column(Boolean, nullable=False, default=False)
    desc = Column(String(255), nullable=False, default="")
    enabled = Column(Boolean, nullable=True, default=True)

    def __repr__(self) -> str:
        return f"<RadarCamera(sn='{self.sn}', name='{self.name}')>"

    def to_all_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            sn=self.sn,
            lng=self.lng,
            lat=self.lat,
            elevation=self.elevation,
            towards=self.towards,
            point=self.point,
            pole=self.pole,
            videoStreamAddress=self.video_stream_address,
            radarCameraIP=self.radar_camera_ip,
            rsuID=self.rsu_id,
            status=self.status,
            rsuName=Optional_util.none(self.rsu).map(lambda v: v.rsu_name).get(),
            desc=self.desc,
            createTime=self.create_time,
            enabled=self.enabled,
        )
