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
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SSWBase(BaseModel):
    sensor_pos: Optional[Dict[str, Any]] = Field(
        None, alias="sensorPos", description="Sensor Position"
    )
    ego_id: Optional[str] = Field(None, alias="egoID", description="ego ID")
    ego_pos: Optional[Dict[str, Any]] = Field(None, alias="egoPos", description="Ego Position")
    speed: Optional[int] = Field(None, alias="speed", description="Speed")
    heading: Optional[int] = Field(None, alias="heading", description="Heading")
    width: Optional[int] = Field(None, alias="width", description="Width")
    length: Optional[int] = Field(None, alias="length", description="Length")
    height: Optional[int] = Field(None, alias="height", description="Height")
    sec_mark: Optional[int] = Field(None, alias="secMark", description="Sec Mark")


class SSWCreate(SSWBase):
    """"""


class SSWUpdate(SSWBase):
    """"""


class SSWInDBBase(SSWBase):
    id: int = Field(..., alias="id", description="CWM ID")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")

    class Config:
        orm_mode = True


# Additional properties to return via API
class SSW(SSWInDBBase):
    """"""


class SSWs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[SSW] = Field(..., alias="data", description="Data")
