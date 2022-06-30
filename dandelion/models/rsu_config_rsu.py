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


class RSUConfigRSU(Base, DandelionBase):
    __tablename__ = "rsu_config_rsu"

    rsu_config_id = Column(Integer, ForeignKey("rsu_config.id"))
    rsu_id = Column(Integer, ForeignKey("rsu.id"))
    # TODO 下发状态 0=下发中 1=下发成功 2=下发失败
    status = Column(Integer, nullable=False, default=0)

    rsu = relationship("RSU", backref="rsu_config_rsu")
    rsu_config = relationship("RSUConfig", backref="rsu_config_rsu")

    def __repr__(self) -> str:
        return f"<RSUConfigRSU(id='{self.id}')>"

    def to_dict(self):
        return dict(
            id=self.id,
            rsu_id=self.rsu_id,
            rsu_config_id=self.rsu_config_id,
            status=self.status,
            create_time=self.create_time,
        )

    @staticmethod
    def create(rsu, rsu_config):
        config = RSUConfigRSU()
        config.rsu = rsu
        config.rsu_config = rsu_config
        return config
