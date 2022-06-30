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

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from dandelion.db.base_class import Base, DandelionBase
from dandelion.util import Optional as Optional_util


class MapRSU(Base, DandelionBase):
    __tablename__ = "map_rsu"

    map_id = Column(Integer, ForeignKey("map.id"))
    rsu_id = Column(Integer, ForeignKey("rsu.id"))
    # TODO 下发状态 0=下发中 1=下发成功 2=下发失败
    status = Column(type_=Integer, nullable=False, default=0)

    rsu = relationship("RSU")

    def __repr__(self) -> str:
        return f"<MapRSU(rsu_id='{self.rsu_id}')>"

    def to_dict(self):
        return dict(
            id=self.id,
            rsuName=Optional_util.none(self.rsu).map(lambda v: v.rsu_name).get(),
            rsuSn=Optional_util.none(self.rsu).map(lambda v: v.rsu_esn).get(),
            onlineStatus=Optional_util.none(self.rsu).map(lambda v: v.online_status).get(),
            rsuStatus=Optional_util.none(self.rsu).map(lambda v: v.rsu_status).get(),
            deliveryStatus=self.status,
            createTime=self.create_time,
        )
