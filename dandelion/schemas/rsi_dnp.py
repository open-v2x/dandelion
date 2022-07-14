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


class RSIDNPBase(BaseModel):
    msg_id: Optional[str] = Field(None, alias="msgID", description="MSG SN")
    sec_mark: Optional[int] = Field(None, alias="secMark", description="Millisecond time")
    ref_pos: Optional[REFPOS] = Field(None, alias="refPos", description="3D coordinates")
    veh_id: Optional[str] = Field(None, alias="vehID", description="Target ID")
    drive_suggestion: Optional[DriveSuggestion] = Field(
        None, alias="driveSuggestion", description="Driving advice"
    )
    path_guidance: Optional[List[PathGuidance]] = Field(
        None, alias="pathGuidance", description="Route plan"
    )
    info: Optional[int] = Field(None, alias="info", description="UseCase type")


class REFPOS(BaseModel):
    lon: int = Field(..., alias="lon", description="Longitude")
    lat: int = Field(..., alias="lat", description="Latitude")
    ele: int = Field(..., alias="ele", description="Elevation")


class DriveSuggestion(BaseModel):
    suggestion: int = Field(..., alias="suggestion", description="Type of driving behavior")
    life_time: int = Field(..., alias="lifeTime", description="Life cycle")


class PathGuidance(BaseModel):
    pos: Optional[REFPOS] = Field(None, alias="suggestion", description="Location")
    speed: Optional[int] = Field(None, alias="speed", description="Speed")
    heading: Optional[int] = Field(None, alias="heading", description="Heading")
    estimated_time: Optional[int] = Field(
        None, alias="estimatedTime", description="Estimated time"
    )


class RSIDNPCreate(RSIDNPBase):
    """"""


class RSIDNPInDBBase(RSIDNPBase):
    id: int = Field(..., alias="id", description="DNP ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSIDNP(RSIDNPInDBBase):
    """"""


class RSIDNPs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSIDNP] = Field(..., alias="data", description="Data")
