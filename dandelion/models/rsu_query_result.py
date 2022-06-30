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


class RSUQueryResult(Base, DandelionBase):
    __tablename__ = "rsu_query_result"

    query_id = Column(Integer, ForeignKey("rsu_query.id"))
    rsu_id = Column(Integer, ForeignKey("rsu.id"))
    rsu = relationship("RSU")
    data = relationship("RSUQueryResultData", backref="result")

    def __repr__(self) -> str:
        return f"<RSUQueryResult(id='{self.id}')>"

    def to_all_dict(self):
        return {**self.to_dict(), **dict(data=[v.data for v in self.data])}

    def to_dict(self):
        return {
            **dict(
                queryType=self.query.query_type,
                timeType=self.query.time_type,
                createTime=self.create_time,
            ),
            **self.rsu_dict(),
        }

    def rsu_dict(self):
        return dict(rsuId=self.rsu.id, rsuName=self.rsu.rsu_name, rsuEsn=self.rsu.rsu_esn)
