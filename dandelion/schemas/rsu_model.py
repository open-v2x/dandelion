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
class RSUModelBase(BaseModel):
    """"""


# Properties to receive via API on creation
class RSUModelCreate(BaseModel):
    name: str = Field(..., alias="name", description="RSU Model Name")
    manufacturer: str = Field(..., alias="manufacturer", description="Manufacturer")
    desc: Optional[str] = Field("", alias="desc", description="Description")


# Properties to receive via API on update
class RSUModelUpdate(RSUModelBase):
    name: str = Field(..., alias="name", description="RSU Model Name")
    manufacturer: str = Field(..., alias="manufacturer", description="Manufacturer")
    desc: Optional[str] = Field("", alias="desc", description="Description")


class RSUModelInDBBase(RSUModelBase):
    id: int = Field(..., alias="id", description="RSU Model ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSUModel(RSUModelInDBBase):
    name: str = Field(..., alias="name", description="RSU Model Name")
    manufacturer: str = Field(..., alias="manufacturer", description="Manufacturer")
    desc: str = Field(..., alias="desc", description="Description")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")


class RSUModels(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSUModel] = Field(..., alias="data", description="Data")
