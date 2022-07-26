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

from sqlalchemy import JSON, Column, Float, Integer, String

from dandelion.db.base_class import Base, DandelionBase


class RSICWM(Base, DandelionBase):
    __tablename__ = "rsi_cwm"

    sensor_pos = Column(JSON, nullable=True)
    event_type = Column(Integer, nullable=False, default=0)
    collision_type = Column(Integer, nullable=False, default=0)
    sec_mark = Column(Integer, nullable=False, default=0)
    ego_id = Column(String(length=255), nullable=False, default="")
    ego_pos = Column(JSON, nullable=True)
    ego_heading = Column(Integer, nullable=False, default=0)
    ego_radius = Column(Float, nullable=False, default=0.0)
    ego_length = Column(Float, nullable=False, default=0.0)
    ego_width = Column(Float, nullable=False, default=0.0)
    ego_kinematics_info = Column(JSON, nullable=True)
    other_id = Column(String(length=255), nullable=False, default="")
    other_pos = Column(JSON, nullable=True)
    other_heading = Column(Integer, nullable=False, default=0)
    other_radius = Column(Float, nullable=False, default=0.0)
    other_length = Column(Float, nullable=False, default=0.0)
    other_width = Column(Float, nullable=False, default=0.0)
    other_kinematics_info = Column(JSON, nullable=True)

    def to_all_dict(self):
        return dict(
            id=self.id,
            sensorPos=self.sensor_pos,
            eventType=self.event_type,
            collisionType=self.collision_type,
            secMark=self.sec_mark,
            egoId=self.ego_id,
            egoPos=self.ego_pos,
            egoHeading=self.ego_heading,
            egoRadius=self.ego_radius,
            egoLength=self.ego_length,
            egoWidth=self.ego_width,
            egoKinematicsInfo=self.ego_kinematics_info,
            otherId=self.other_id,
            otherPos=self.other_pos,
            otherHeading=self.other_heading,
            otherRadius=self.other_radius,
            otherLength=self.other_length,
            otherWidth=self.other_width,
            otherKinematicsInfo=self.other_kinematics_info,
            createTime=self.create_time,
        )
