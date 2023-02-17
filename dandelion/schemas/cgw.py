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


class CGWBase(BaseModel):
    cgw_level: Optional[int] = Field(None, alias="cgwLevel", description="CGW Level")
    lane_id: Optional[int] = Field(None, alias="laneID", description="Lane ID")
    average_speed: Optional[int] = Field(None, alias="avgSpeed", description="Average Speed")

    sensor_pos: Optional[Dict[str, Any]] = Field(
        None, alias="sensorPos", description="Sensor Position"
    )
    start_point: Optional[Dict[str, Any]] = Field(
        None, alias="startPoint", description="Start Point"
    )
    end_point: Optional[Dict[str, Any]] = Field(None, alias="endPoint", description="End Point")
    sec_mark: Optional[int] = Field(None, alias="secMark", description="Sec Mark")


class CGWCreate(CGWBase):
    """"""


class CGWUpdate(CGWBase):
    """"""


class CGWInDBBase(CGWBase):
    id: int = Field(..., alias="id", description="CWM ID")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")

    class Config:
        orm_mode = True


# Additional properties to return via API
class CGW(CGWInDBBase):
    """"""


class CGWs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[CGW] = Field(..., alias="data", description="Data")
