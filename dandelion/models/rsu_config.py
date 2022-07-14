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

from sqlalchemy import JSON, Column, String

from dandelion.db.base_class import Base, DandelionBase


class RSUConfig(Base, DandelionBase):
    __tablename__ = "rsu_config"

    name = Column(String(64), nullable=False, index=True, unique=True)
    bsm = Column(JSON, nullable=True)
    rsi = Column(JSON, nullable=True)
    rsm = Column(JSON, nullable=True)
    map = Column(JSON, nullable=True)
    spat = Column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<RSUConfig(id='{self.id}', name='{self.name}')>"

    def to_dict(self):
        return {
            **self.mqtt_dict(),
            **dict(id=self.id, name=self.name, createTime=self.create_time),
        }

    def to_all_dict(self):
        return {
            **self.to_dict(),
            **dict(
                rsus=[
                    {**v.rsu.to_all_dict(), **dict(deliveryStatus=v.status)}
                    for v in self.rsu_config_rsu
                ]
            ),
        }

    def mqtt_dict(self):
        return dict(
            seqNum=self.id,
            bsmConfig=self.bsm,
            rsiConfig=self.rsi,
            spatConfig=self.spat,
            rsmConfig=self.rsm,
            mapConfig=self.map,
        )
