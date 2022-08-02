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


class RSICLC(Base, DandelionBase):
    __tablename__ = "rsi_clc"

    msg_id = Column(String(length=255), nullable=False, default="")
    sec_mark = Column(Integer, nullable=False, default=0)
    veh_id = Column(String(length=255), nullable=False, default="")
    ref_pos = Column(JSON, nullable=False)
    drive_suggestion = Column(JSON, nullable=False)
    info = Column(Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return (
            f"<RSICLC(msg_id='{self.msg_id}', "
            f"sec_mark='{self.sec_mark}', "
            f"veh_id='{self.veh_id}', "
            f"ref_pos='{self.ref_pos}', "
            f"drive_suggestion='{self.drive_suggestion}', "
            f"info='{self.info}')>"
        )

    def to_all_dict(self):
        return dict(
            id=self.id,
            msgID=self.msg_id,
            secMark=self.sec_mark,
            vehID=self.veh_id,
            refPos=self.ref_pos,
            driveSuggestion=self.drive_suggestion,
            info=self.info,
            createTime=self.create_time,
        )
