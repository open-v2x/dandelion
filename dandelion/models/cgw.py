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

from sqlalchemy import JSON, Column, Integer

from dandelion.db.base_class import Base, DandelionBase


class CGW(Base, DandelionBase):
    __tablename__ = "cgw"

    cgw_level = Column(Integer, nullable=False, index=True)
    lane_id = Column(Integer, nullable=False)
    average_speed = Column(Integer, nullable=False)
    sensor_pos = Column(JSON, nullable=False)
    start_point = Column(JSON, nullable=False)
    end_point = Column(JSON, nullable=False)
    sec_mark = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"<CGW(lane_id='{self.lane_id}', " f"cgw_level='{self.cgw_level}'>"

    def to_all_dict(self):
        return dict(
            id=self.id,
            cgwLevel=self.cgw_level,
            laneID=self.lane_id,
            sensorPos=self.sensor_pos,
            startPoint=self.start_point,
            endPoint=self.end_point,
            secMark=self.sec_mark,
            createTime=self.create_time,
            avgSpeed=self.average_speed,
        )
