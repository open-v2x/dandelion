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


class RSUTMP(Base, DandelionBase):
    __tablename__ = "rsu_tmp"

    rsu_id = Column(String(64), nullable=False)
    rsu_esn = Column(String(64), nullable=False, index=True, unique=True)
    rsu_name = Column(String(64), nullable=False, index=True)
    rsu_status = Column(String(32), nullable=False)
    version = Column(String(64), nullable=False)
    location = Column(JSON, nullable=False)
    config = Column(JSON, nullable=False)

    def __repr__(self) -> str:
        return f"<RSUTMP(id='{self.id}')>"

    def to_dict(self):
        return dict(
            id=self.id,
            rsuId=self.rsu_id,
            rsuName=self.rsu_name,
            rsuEsn=self.rsu_esn,
            version=self.version,
            createTime=self.create_time,
        )
