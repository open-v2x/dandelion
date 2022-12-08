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

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from dandelion.db.base_class import Base, DandelionBase
from dandelion.util import Optional as Optional_util


class Spat(Base, DandelionBase):
    __tablename__ = "spat"

    intersection_id = Column(String(64), nullable=False, index=True)
    name = Column(String(64), nullable=False, index=True, default="")
    spat_ip = Column(String(15), nullable=False, default="")
    point = Column(String(15), nullable=False, default="")
    online_status = Column(Boolean, nullable=False, default=False)
    enabled = Column(Boolean, nullable=False, default=False)
    phase_id = Column(String(64), nullable=False, index=True)
    light = Column(String(15), nullable=False, default="")
    rsu_id = Column(Integer, ForeignKey("rsu.id"))
    timing = Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    desc = Column(String(255), nullable=False, default="")

    intersection_code = Column(String(64), ForeignKey("intersection.code"))

    __table_args__ = (UniqueConstraint("intersection_id", "phase_id"),)

    def __repr__(self) -> str:
        return f"<Spat(intersection_id='{self.intersection_id}', name='{self.name}')>"

    def to_dict(self):
        return {
            **dict(
                id=self.id,
                intersectionId=self.intersection_id,
                name=self.name,
                spatIP=self.spat_ip,
                point=self.point,
                onlineStatus=self.online_status,
                enabled=self.enabled,
                phaseId=self.phase_id,
                light=self.light,
                rsuId=self.rsu_id,
                timing=self.timing,
                rsuName=Optional_util.none(self.rsu).map(lambda v: v.rsu_name).get(),
                desc=self.desc,
                createTime=self.create_time,
            ),
            **Optional_util.none(self.intersection).map(lambda v: v.to_all()).get(),
        }
