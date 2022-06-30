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

from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import relationship

from dandelion.db.base_class import Base, DandelionBase


class RSULog(Base, DandelionBase):
    __tablename__ = "rsu_log"

    upload_url = Column(String(64), nullable=False)
    user_id = Column(String(64), nullable=False)
    password = Column(String(255), nullable=False)
    transprotocal = Column(Enum("http", "https", "ftp", "sftp", "other"), nullable=False)

    rsus = relationship("RSU", backref="rsu_log")

    def __repr__(self) -> str:
        return f"<RSULog(id='{self.id}')>"

    def to_all_dict(self):
        return dict(
            id=self.id,
            uploadUrl=self.upload_url,
            userId=self.user_id,
            password=self.password,
            transprotocal=self.transprotocal,
            createTime=self.create_time,
            rsus=[dict(id=rsu.id, rsuName=rsu.rsu_name, rsuEsn=rsu.rsu_esn) for rsu in self.rsus],
        )

    def mqtt_dict(self):
        return dict(
            uploadUrl=self.upload_url,
            userId=self.user_id,
            password=self.password,
            transprotocal=self.transprotocal,
        )
