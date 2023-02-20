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


class SSW(Base, DandelionBase):
    __tablename__ = "ssw"

    sensor_pos = Column(JSON, nullable=False)
    ego_id = Column(String(16), nullable=False)
    ego_pos = Column(JSON, nullable=False)
    speed = Column(Integer, nullable=False)
    heading = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    sec_mark = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<SSW(ego_id='{self.ego_id}'>"

    def to_all_dict(self):
        return dict(
            id=self.id,
            egoID=self.ego_id,
            sensorPos=self.sensor_pos,
            egoPos=self.ego_pos,
            speed=self.speed,
            heading=self.heading,
            width=self.width,
            length=self.length,
            height=self.height,
            secMark=self.sec_mark,
            createTime=self.create_time,
        )
