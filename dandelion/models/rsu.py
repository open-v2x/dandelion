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

from sqlalchemy import JSON, Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from dandelion.db.base_class import Base, DandelionBase


class RSU(Base, DandelionBase):
    __tablename__ = "rsu"

    rsu_id = Column(String(64), nullable=False)
    rsu_esn = Column(String(64), nullable=False, index=True, unique=True, comment="serial number")
    rsu_ip = Column(String(64), nullable=False)
    rsu_name = Column(String(64), index=True, nullable=False)
    version = Column(String(64), nullable=False)
    rsu_status = Column(String(32), index=True, nullable=False)
    enabled = Column(Boolean, nullable=True, default=True)
    location = Column(JSON, nullable=False)
    config = Column(JSON, nullable=False)
    online_status = Column(Boolean, index=True, nullable=False, default=False)
    rsu_model_id = Column(Integer, ForeignKey("rsu_model.id"))
    area_code = Column(String(64), ForeignKey("area.code"))
    address = Column(
        String(255), nullable=False, default="", comment="Installation specific location"
    )
    desc = Column(String(255), nullable=True, default="")
    log_id = Column(Integer, ForeignKey("rsu_log.id"))

    imei = Column(String(64), nullable=True)
    icc_id = Column(String(64), nullable=True)
    communication_type = Column(String(64), nullable=True)
    running_communication_type = Column(String(64), nullable=True)
    transprotocal = Column(String(64), nullable=True)
    software_version = Column(String(64), nullable=True)
    hardware_version = Column(String(64), nullable=True)
    depart = Column(String(64), nullable=True)

    bias_x = Column(Float, nullable=True, default=0.0)
    bias_y = Column(Float, nullable=True, default=0.0)
    rotation = Column(Float, nullable=True, default=0.0)
    reverse = Column(Boolean, nullable=True, default=False)
    scale = Column(Float, nullable=True, default=0.0)
    lane_info = Column(JSON, nullable=True)

    cameras = relationship("Camera", backref="rsu")
    radars = relationship("Radar", backref="rsu")

    def __repr__(self) -> str:
        return f"<RSU(id='{self.id}', rsuId='{self.rsu_id}')>"

    def to_dict(self):
        return dict(
            id=self.id,
            rsuId=self.rsu_id,
            rsuEsn=self.rsu_esn,
            rsuName=self.rsu_name,
            rsuIP=self.rsu_ip,
            version=self.version,
            rsuStatus=self.rsu_status,
            enabled=self.enabled,
            onlineStatus=self.online_status,
            rsuModelId=self.rsu_model_id,
            rsuModelName=self.rsu_model.name if self.rsu_model else "",
            areaCode=self.area_code,
            address=self.address,
            desc=self.desc,
            location=self.location,
            config=self.config,
            createTime=self.create_time,
            updateTime=self.update_time,
        )

    def to_base_dict(self):
        return dict(
            imei=self.imei,
            iccID=self.icc_id,
            communicationType=self.communication_type,
            runningCommunicationType=self.running_communication_type,
            transprotocal=self.transprotocal,
            softwareVersion=self.software_version,
            hardwareVersion=self.hardware_version,
            depart=self.depart,
        )

    def to_all_dict(self):
        return {**self.to_dict(), **self.area.to_all()}

    def to_info_dict(self):
        return {**self.to_all_dict(), **self.to_base_dict(), "config": self.rsu_config_rsu}

    def mqtt_dict(self):
        return dict(
            rsuId=self.rsu_id,
            rsuEsn=self.rsu_esn,
            rsuName=self.rsu_name,
            version=self.version,
            rsuStatus=self.rsu_status,
            location=self.location,
            config=self.config,
        )
