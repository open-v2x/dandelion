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
from typing import List

from pydantic import BaseModel, Field


class RSUsInMapRSU(BaseModel):
    id: int = Field(..., alias="id", description="ID")
    rsu_id: int = Field(..., alias="rsuId", description="RSU ID")
    status: int = Field(..., alias="status", description="Status")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")


# Shared properties
class MapRSUBase(BaseModel):
    map_id: int = Field(..., alias="mapId", description="Map ID")
    rsus: List[RSUsInMapRSU] = Field(..., alias="rsus", description="RSUs")


# Properties to receive via API on creation
class MapRSUCreate(BaseModel):
    rsus: List[str] = Field(..., alias="rsus", description="RSU ESN")


# Properties to receive via API on update
class MapRSUUpdate(MapRSUBase):
    """"""


class MapRSUInDBBase(BaseModel):
    id: int = Field(..., alias="id", description="Map RSU ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class MapRSU(BaseModel):
    data: MapRSUBase = Field(..., alias="data", description="Data")


class MapRSUsBase(MapRSUInDBBase):
    rsu_name: str = Field(..., alias="rsuName", description="RSU Name")
    rsu_sn: str = Field(..., alias="rsuSn", description="RSU SN")
    online_status: bool = Field(..., alias="onlineStatus", description="Online Status")
    rsu_status: str = Field(..., alias="rsuStatus", description="RSU Status")
    delivery_status: int = Field(..., alias="deliveryStatus", description="Delivery Status")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")


class MapRSUs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[MapRSUsBase] = Field(..., alias="data", description="Data")
