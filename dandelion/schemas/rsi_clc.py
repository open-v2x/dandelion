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


class RSICLCBase(BaseModel):
    msg_id: Optional[str] = Field(None, alias="msgID", description="MSG ID")
    sec_mark: Optional[int] = Field(None, alias="secMark", description="SEC Mark")
    ref_pos: Optional[REFPOS] = Field(None, alias="refPos", description="3D Coordinates")
    veh_id: Optional[str] = Field(None, alias="vehID", description="Target ID")
    drive_suggestion: Optional[DriveSuggestion] = Field(
        None, alias="driveSuggestion", description="Drive Suggestion"
    )
    info: Optional[int] = Field(None, alias="info", description="Info Type")


class REFPOS(BaseModel):
    lon: int = Field(..., alias="lon", description="Longitude")
    lat: int = Field(..., alias="lat", description="Latitude")
    ele: Optional[int] = Field(None, alias="ele", description="Elevation")


class DriveSuggestion(BaseModel):
    suggestion: int = Field(..., alias="suggestion", description="Suggestion")
    life_time: int = Field(..., alias="lifeTime", description="Life Time")


class RSICLCCreate(RSICLCBase):
    """"""


class RSICLCInDBBase(RSICLCBase):
    id: int = Field(..., alias="id", description="CLC ID")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSICLC(RSICLCInDBBase):
    """"""


class RSICLCs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSICLC] = Field(..., alias="data", description="Data")
