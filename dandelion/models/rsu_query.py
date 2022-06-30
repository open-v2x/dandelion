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

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from dandelion.db.base_class import Base, DandelionBase


class TimeType(object):
    one_hour = 1
    one_day = 2
    one_week = 3
    # TODO 开机至今
    to_date = 4


class RSUQuery(Base, DandelionBase):
    __tablename__ = "rsu_query"

    query_type = Column(Integer, nullable=False)
    time_type = Column(Integer)
    results = relationship("RSUQueryResult", backref="query")

    def __repr__(self) -> str:
        return f"<RSUQuery(id='{self.id}')>"

    def to_dict(self):
        return dict(
            id=self.id,
            queryType=self.query_type,
            timeType=self.time_type,
            createTime=self.create_time,
            rsus=self.result_dict(),
        )

    def result_dict(self):
        return [v.rsu_dict() for v in self.results]
