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


# Shared properties
class RSUTMPBase(BaseModel):
    """"""


# Properties to receive via API on creation
class RSUTMPCreate(BaseModel):
    rsu_id: Optional[str] = Field(..., alias="rsuId", description="RSU ID")
    rsu_name: Optional[str] = Field(..., alias="rsuName", description="RSU Name")
    rsu_esn: Optional[str] = Field(..., alias="rsuEsn", description="RSU ESN")
    version: Optional[str] = Field(..., alias="version", description="Version")
    rsu_status: Optional[str] = Field(..., alias="rsuStatus", description="RSU Status")
    location: Optional[Dict[str, float]] = Field(..., alias="location", description="Location")
    config: Optional[Dict[str, Any]] = Field(..., alias="config", description="Config")


# Properties to receive via API on update
class RSUTMPUpdate(RSUTMPBase):
    """"""


class RSUTMPInDBBase(RSUTMPBase):
    id: int = Field(..., alias="id", description="RSU TMP ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSUTMP(RSUTMPInDBBase):
    rsu_id: str = Field(..., alias="rsuId", description="RSU ID")
    rsu_name: str = Field(..., alias="rsuName", description="RSU Name")
    rsu_esn: str = Field(..., alias="rsuEsn", description="RSU ESN")
    version: str = Field(..., alias="version", description="Version")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")


class RSUTMPs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSUTMP] = Field(..., alias="data", description="Data")
