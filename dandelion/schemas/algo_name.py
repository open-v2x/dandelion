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

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Shared properties
class AlgoNameBase(BaseModel):
    """"""


# Properties to receive via API on creation
class AlgoNameCreate(AlgoNameBase):
    """"""

    module: str = Field(..., alias="module", description="Algo module")
    name: str = Field(..., alias="name", description="Algo name")
    enable: bool = Field(..., alias="enable", description="Algo enable")
    module_path: str = Field(..., alias="module_path", description="Algo path")
    in_use: str = Field(..., alias="in_use", description="Algo in use")


# Properties to receive via API on update
class AlgoNameUpdate(AlgoNameBase):
    """"""

    enable: Optional[bool] = Field(None, alias="enable", description="Algo enable")
    in_use: Optional[str] = Field(None, alias="in_use", description="Algo in use")


class AlgoNameInDBBase(AlgoNameBase):
    class Config:
        orm_mode = True


# Additional properties to return via API
class AlgoName(AlgoNameInDBBase):
    """"""

    id: int = Field(..., alias="id", description="Algo id")
    module: str = Field(..., alias="module", description="Algo module")
    algo: str = Field(..., alias="algo", description="Algo name")
    enable: bool = Field(..., alias="enable", description="Algo enable")
    module_path: str = Field(..., alias="modulePath", description="Algo path")
    in_use: str = Field(..., alias="inUse", description="Algo in use")
    version: List = Field(..., alias="version", description="Algo version list")
    update_time: Optional[datetime] = Field(None, alias="updateTime", description="Update Time")


class AlgoNames(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[AlgoName] = Field(..., alias="data", description="Data")


class AlgoNameEdit(BaseModel):
    module: str = Field(..., alias="module", description="Algo module")
    algo: str = Field(..., alias="algo", description="Algo name")
    enable: bool = Field(..., alias="enable", description="Algo enable")
    module_path: str = Field(..., alias="modulePath", description="Algo path")
    in_use: str = Field(..., alias="inUse", description="Algo in use")
    update_time: Optional[datetime] = Field(None, alias="updateTime", description="Update Time")


class AlgoNameUpdateAll(AlgoNameBase):
    """"""

    module: str = Field(..., alias="module", description="Algo module")
    algo: str = Field(..., alias="algo", description="Algo name")
    enable: Optional[bool] = Field(None, alias="enable", description="Algo enable")
    in_use: Optional[str] = Field(None, alias="inUse", description="Algo in use")
