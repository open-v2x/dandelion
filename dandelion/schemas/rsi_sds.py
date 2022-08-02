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

<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> bd4ed84 (feat: Add RSI_CLC RSI_CWM RSI_SDS)
from typing import List, Optional

from pydantic import BaseModel, Field


class RSISDSBase(BaseModel):
    msg_id: Optional[str] = Field(None, alias="msgID", description="MSG ID")
    equipment_type: Optional[int] = Field(
        None, alias="equipmentType", description="Equipment Type"
    )
    sensor_pos: Optional[Position] = Field(None, alias="sensorPos", description="Sensor Position")
    sec_mark: Optional[int] = Field(None, alias="secMark", description="SEC Mark")
    ego_id: Optional[str] = Field(None, alias="egoID", description="EGO ID")
    ego_pos: Optional[Position] = Field(None, alias="egoPos", description="EGO Position")


class Position(BaseModel):
    lon: int = Field(..., alias="lon", description="Longitude")
    lat: int = Field(..., alias="lat", description="Latitude")
    ele: Optional[int] = Field(None, alias="ele", description="Elevation")


class RSISDSCreate(RSISDSBase):
    """"""


class RSISDSInDBBase(RSISDSBase):
    id: int = Field(..., alias="id", description="SDS ID")
<<<<<<< HEAD
    create_time: datetime = Field(..., alias="createTime", description="Create Time")
=======
>>>>>>> bd4ed84 (feat: Add RSI_CLC RSI_CWM RSI_SDS)

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSISDS(RSISDSInDBBase):
    """"""


class RSISDSs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSISDS] = Field(..., alias="data", description="Data")
