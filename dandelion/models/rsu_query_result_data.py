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

from sqlalchemy import JSON, Column, ForeignKey, Integer

from dandelion.db.base_class import Base, DandelionBase


class RSUQueryResultData(Base, DandelionBase):
    __tablename__ = "rsu_query_result_data"

    result_id = Column(Integer, ForeignKey("rsu_query_result.id"))
    data = Column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<RSUQueryResultData(id='{self.id}')>"
