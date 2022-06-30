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

from enum import Enum

from sqlalchemy import JSON, Column, Enum as db_Enum, ForeignKey, Integer, String

from dandelion.db.base_class import Base, DandelionBase
from dandelion.util import Optional as Optional_util


class PtcType(Enum):
    # TODO
    unknown = "未知类型"
    motor = "机动车"
    non_motor = "非机动车"
    pedestrian = "行人"
    rsu = "RSU设备"


class Participants(Base, DandelionBase):
    __tablename__ = "rsm_participants"

    rsm_id = Column(Integer, ForeignKey("rsm.id"))

    ptc_type = Column(db_Enum(PtcType), nullable=False)
    ptc_id = Column(Integer, nullable=False)
    source = Column(Integer, nullable=False)
    sec_mark = Column(Integer, nullable=True)
    pos = Column(JSON, nullable=False)
    accuracy = Column(String(255), nullable=True)
    speed = Column(Integer, nullable=True)
    heading = Column(Integer, nullable=True)
    size = Column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<Participants(id='{self.id}')>"

    def to_dict(self):
        return dict(
            id=self.id,
            ptcId=self.ptc_id,
            ptcType=self.ptc_type.name,
            ptcTypeName=self.ptc_type.value,
            source=self.source,
            secMark=self.sec_mark,
            lon=Optional_util.none(self.pos).map(lambda v: v.get("lon")).get(),
            lat=Optional_util.none(self.pos).map(lambda v: v.get("lat")).get(),
            accuracy=self.accuracy,
            speed=self.speed,
            heading=self.heading,
            size=self.size,
            createTime=self.create_time,
        )
