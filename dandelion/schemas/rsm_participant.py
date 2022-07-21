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
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# Shared properties
class RSMParticipantBase(BaseModel):
    """"""


# Properties to receive via API on creation
class RSMParticipantCreate(BaseModel):
    """"""


# Properties to receive via API on update
class RSMParticipantUpdate(RSMParticipantBase):
    """"""


class RSMParticipantInDBBase(RSMParticipantBase):
    id: int = Field(..., alias="id", description="RSM Participant ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSMParticipant(RSMParticipantInDBBase):
    ptc_id: int = Field(..., alias="ptcId", description="PTC id")
    ptc_type: str = Field(..., alias="ptcType", description="PTC type")
    ptc_type_name: str = Field(..., alias="ptcTypeName", description="PTC type name")
    source: int = Field(..., alias="source", description="Source")
    sec_mark: int = Field(..., alias="secMark", description="Sec mark")
    lon: int = Field(..., alias="lon", description="Lon")
    lat: int = Field(..., alias="lat", description="Lat")
    accuracy: Optional[str] = Field(None, alias="accuracy", description="Accuracy")
    speed: int = Field(..., alias="speed", description="Speed")
    heading: int = Field(..., alias="heading", description="Heading")
    size: Dict[str, int] = Field(..., alias="size", description="Size")
    create_time: datetime = Field(..., alias="createTime", description="Create time")


class RSMParticipants(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSMParticipant] = Field(..., alias="data", description="Data")
