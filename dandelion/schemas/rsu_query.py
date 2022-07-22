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


class RSUInRSUQuery(BaseModel):
    rsu_id: Optional[int] = Field(None, alias="rsuId", description="The ID of the RSU")
    rsu_esn: Optional[str] = Field(None, alias="rsuEsn", description="RSU ESN")
    rsu_name: Optional[str] = Field(None, alias="rsuName", description="RSU name")
    data: Optional[Any] = Field(None, alias="data", description="Query Data")


# Shared properties
class RSUQueryBase(BaseModel):
    """"""


# Properties to receive via API on creation
class RSUQueryCreate(BaseModel):
    query_type: int = Field(..., alias="queryType", description="Query Type")
    time_type: int = Field(..., alias="timeType", description="Time Type")
    rsus: List[int] = Field(..., alias="rsus", description="RSUs")


# Properties to receive via API on update
class RSUQueryUpdate(RSUQueryBase):
    """"""


class RSUQueryInDBBase(RSUQueryBase):
    id: int = Field(..., alias="id", description="RSU Query ID")

    class Config:
        orm_mode = True


class RSUQueryDetailBase(BaseModel):
    rsu_id: Optional[int] = Field(None, alias="rsuId", description="The ID of the RSU")
    rsu_name: str = Field(..., alias="rsuName", description="RSU name")
    rsu_esn: str = Field(..., alias="rsuEsn", description="RSU ESN")
    query_type: int = Field(..., alias="queryType", description="Query Type")
    time_type: int = Field(..., alias="timeType", description="Time Type")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")
    data: List[Dict[str, Any]] = Field(..., alias="data", description="Data")


class RSUQueryDetail(BaseModel):
    data: Optional[Any] = Field(None, alias="data", description="RSU Query Detail")


# Additional properties to return via API
class RSUQuery(RSUQueryInDBBase):
    query_type: int = Field(..., alias="queryType", description="Query Type")
    time_type: int = Field(..., alias="timeType", description="Time Type")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")
    rsus: Optional[List[RSUInRSUQuery]] = Field(None, alias="rsus", description="RSUs")


class RSUQueries(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSUQuery] = Field(..., alias="data", description="Data")
