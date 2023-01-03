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

from sqlalchemy import Column, ForeignKey, String, UniqueConstraint

from dandelion.db.base_class import Base, DandelionBase


class AlgoVersion(Base, DandelionBase):
    __tablename__ = "algo_version"

    algo = Column(String(64), ForeignKey("algo_name.name"))
    version = Column(String(64), nullable=False)
    version_path = Column(String(64), nullable=True)

    __table_args__ = (UniqueConstraint("algo", "version"),)

    def __repr__(self) -> str:
        return f"<algo_version(version='{self.version}')>"

    def to_dict(self):
        return {
            **dict(
                id=self.id,
                version=self.version,
                versionPath=self.version_path,
            ),
        }

    def to_all_dict(self):
        return {
            **dict(
                id=self.id,
                version=self.version,
                version_path=self.version_path,
                algo=self.algo,
                module=self.algo_name.module,
            ),
        }
