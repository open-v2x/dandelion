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

from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from dandelion.db.base_class import Base, DandelionBase
from dandelion.models.province import Province


class Country(Base, DandelionBase):
    __tablename__ = "country"

    code = Column(type_=String(64), unique=True, index=True, nullable=False)
    name = Column(type_=String(64), nullable=False)

    provinces: List[Province] = relationship("Province", backref="country")

    def __repr__(self) -> str:
        return f"<Country(code='{self.code}', name='{self.name}')>"

    def to_dict(self):
        return dict(code=self.code, name=self.name)

    def to_all_dict(self):
        return {**self.to_dict(), "children": [v.to_all_dict() for v in self.provinces]}
