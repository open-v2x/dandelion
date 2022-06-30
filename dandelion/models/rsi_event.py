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

import enum

from sqlalchemy import JSON, Boolean, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from dandelion.db.base_class import Base, DandelionBase
from dandelion.util import Optional as Optional_util


class EventClass(enum.Enum):
    # TODO 异常路况
    AbnormalTraffic = 1
    # TODO 恶劣天气
    AdverseWeather = 2
    # TODO 异常车况
    AbnormalVehicle = 3
    # TODO 标志标牌
    TrafficSign = 4


class EventSource(enum.Enum):
    unknown = 1
    police = 2
    government = 3
    meteorological = 4
    internet = 5
    detection = 6


class RSIEvent(Base, DandelionBase):
    __tablename__ = "rsi_event"

    rsu_id = Column(Integer, ForeignKey("rsu.id"))
    area_code = Column(String(64), ForeignKey("area.code"))
    address = Column(String(64), nullable=False, index=True, default="")
    alert_id = Column(String(64), nullable=True, default="")
    duration = Column(Integer, nullable=True, default=0)
    event_status = Column(Boolean, nullable=True, default=True)
    timestamp = Column(String(64), nullable=True, default="", comment="yyyy-MM-ddT HH:mm:ss.SSS Z")
    event_class = Column(Enum(EventClass), nullable=True)
    event_type = Column(Integer, nullable=True, default="")
    event_source = Column(Enum(EventSource), nullable=True)
    event_confidence = Column(Float, nullable=True, default=0)
    event_position = Column(JSON, nullable=True)
    event_radius = Column(Float, nullable=True, default=0)
    event_description = Column(String(255), nullable=True, default="")
    event_priority = Column(Integer, nullable=True)
    reference_paths = Column(JSON, nullable=True)

    rsu = relationship("RSU", backref="rsi_events")

    def __repr__(self) -> str:
        return f"<RSIEvent(id='{self.id}')>"

    def to_all_dict(self):
        return {
            **self.to_dict(),
            **dict(
                alertID=self.alert_id,
                duration=self.duration,
                eventStatus=self.event_status,
                timestamp=self.timestamp,
                eventSource=self.event_source.name,
                eventConfidence=self.event_confidence,
                eventPosition=self.event_position,
                eventRadius=self.event_radius,
                eventDescription=self.event_description,
                eventPriority=self.event_priority,
                reference_paths=self.reference_paths,
            ),
        }

    def to_dict(self):
        return {
            **dict(
                id=self.id,
                rsuName=Optional_util.none(self.rsu).map(lambda v: v.rsu_name).get(),
                rsuEsn=Optional_util.none(self.rsu).map(lambda v: v.rsu_esn).get(),
                address=self.address,
                eventClass=self.event_class.name,
                eventType=self.event_type,
                createTime=self.create_time,
            ),
            **self.area.to_all(),
        }
