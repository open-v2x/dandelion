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

from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from dandelion.db.base_class import Base, DandelionBase


class Reboot(enum.Enum):
    # TODO 0: 不重启, 1: 重启
    not_reboot = 0
    reboot = 1


class MNG(Base, DandelionBase):
    __tablename__ = "mng"

    rsu_id = Column(Integer, ForeignKey("rsu.id"))
    # TODO 心跳上报频率 0: 不上报心跳信息 >0: 表示上报间隔，秒
    heartbeat_rate = Column(Integer, nullable=True, default=60)
    # TODO 设备运行状态上报频率 0: 不上报设备运行状态信息 >0: 表示上报间隔，秒
    running_info_rate = Column(Integer, nullable=True, default=60)
    # TODO 日志上报频率 0: 不上报日志信息 >0: 表示上报间隔，秒
    log_rate = Column(Integer, nullable=True, default=0)
    log_level = Column(Enum("DEBUG", "INFO", "ERROR", "WARN", "NOLog"), nullable=True)
    reboot = Column(Enum(Reboot), nullable=True)
    address_change = Column(JSON, nullable=True)
    extend_config = Column(String(64), nullable=False)

    rsu = relationship("RSU", backref=backref("mng", uselist=False))

    def __repr__(self) -> str:
        return f"<MNG(rsu_id='{self.rsu_id}')>"

    def all_dict(self):
        return dict(
            id=self.id,
            rsuName=self.rsu.rsu_name,
            rsuEsn=self.rsu.rsu_esn,
            hbRate=self.heartbeat_rate,
            runningInfoRate=self.running_info_rate,
            addressChg=self.address_change,
            logLevel=self.log_level,
            reboot=self.reboot.name,
            extendConfig=self.extend_config,
            createTime=self.create_time,
        )

    def mqtt_dict(self):
        return dict(
            rsuName=self.rsu.rsu_name,
            rsuEsn=self.rsu.rsu_esn,
            protocolVersion=self.rsu.version,
            hbRate=self.heartbeat_rate,
            runningInfoRate=self.running_info_rate,
            addressChg=self.address_change,
            logLevel=self.log_level,
            reboot=self.reboot.value,
            extendConfig=self.extend_config,
        )
