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


class RSISDS(Base, DandelionBase):
    __tablename__ = "rsi_sds"

    msg_id = Column(String(length=255), nullable=False, default="")
    equipment_type = Column(Integer, nullable=False, default=0)
    sensor_pos = Column(JSON, nullable=True)
    sec_mark = Column(Integer, nullable=False, default=0)
    ego_id = Column(String(length=255), nullable=False, default="")
    ego_pos = Column(JSON, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<RSISDS(msg_id='{self.msg_id}', "
            f"equipment_type='{self.equipment_type}', "
            f"sensor_pos='{self.sensor_pos}', "
            f"sec_mark='{self.sec_mark}', "
            f"ego_id='{self.ego_id}', "
            f"ego_pos='{self.ego_pos}')>"
        )

    def to_all_dict(self):
        return dict(
            id=self.id,
            msgID=self.msg_id,
            equipmentType=self.equipment_type,
            sensorPos=self.sensor_pos,
            secMark=self.sec_mark,
            egoID=self.ego_id,
            egoPos=self.ego_pos,
            createTime=self.create_time,
        )
