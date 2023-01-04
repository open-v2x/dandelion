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

from typing import List, Optional

from pydantic import BaseModel, Field


# Shared properties
class AlgoVersionBase(BaseModel):
    """"""


# Properties to receive via API on creation
class AlgoVersionCreate(AlgoVersionBase):
    """"""

    algo: str = Field(..., alias="algo", description="Algo algo name")
    version: str = Field(..., alias="version", description="Algo version")
    version_path: Optional[str] = Field(
        None, alias="version_path", description="Algo version path"
    )


class AlgoVersionCreateAll(BaseModel):
    """"""

    module: str = Field(..., alias="module", description="Algo Module")
    algo: str = Field(..., alias="algo", description="Algo Name")
    enable: Optional[bool] = Field(None, alias="enable", description="Algo enable")
    in_use: Optional[str] = Field(None, alias="inUse", description="Algo in use")
    module_path: Optional[str] = Field(None, alias="modulePath", description="Algo module path")
    version: str = Field(..., alias="version", description="Algo Version")
    version_path: Optional[str] = Field(None, alias="versionPath", description="Algo version path")


# Properties to receive via API on update
class AlgoVersionUpdate(AlgoVersionBase):
    """"""


class AlgoVersionInDBBase(AlgoVersionBase):
    id: int = Field(..., alias="id", description="Algo ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class AlgoVersion(AlgoVersionInDBBase):
    """"""

    algo: str = Field(..., alias="algo", description="Algo name")
    version: str = Field(..., alias="version", description="Algo Version")
    versionPath: Optional[str] = Field(None, alias="version_path", description="Algo version path")


class AlgoVersionGET(AlgoVersionBase):
    """"""

    id: Optional[int] = Field(None, alias="id", description="Algo id")
    module: str = Field(..., alias="module", description="Algo module")
    algo: str = Field(..., alias="algo", description="Algo name")
    version: str = Field(..., alias="version", description="Algo version list")
    versionPath: Optional[str] = Field(None, alias="version_path", description="Algo version path")


class AlgoVersions(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[AlgoVersionGET] = Field(..., alias="data", description="Data")
