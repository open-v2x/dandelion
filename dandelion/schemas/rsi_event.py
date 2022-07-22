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
class RSIEventBase(BaseModel):
    """"""


# Properties to receive via API on creation
class RSIEventCreate(BaseModel):
    alert_id: Optional[int] = Field(None, alias="alertID", description="Alert ID")
    duration: Optional[int] = Field(None, alias="duration", description="Duration")
    event_status: Optional[bool] = Field(None, alias="eventStatus", description="Event status")
    timestamp: Optional[str] = Field(None, alias="timeStamp", description="Timestamp")
    event_class: Optional[str] = Field(None, alias="eventClass", description="Event class")
    event_type: Optional[int] = Field(None, alias="eventType", description="Event type")
    event_source: Optional[str] = Field(None, alias="eventSource", description="Event source")
    event_confidence: Optional[float] = Field(
        None, alias="eventConfidence", description="Event confidence"
    )
    event_position: Optional[Dict[str, Any]] = Field(
        None, alias="eventPosition", description="Event position"
    )
    event_radius: Optional[float] = Field(None, alias="eventRadius", description="Event radius")
    event_description: Optional[str] = Field(
        None, alias="eventDescription", description="Event description"
    )
    event_priority: Optional[int] = Field(
        None, alias="eventPriority", description="Event priority"
    )
    reference_paths: Optional[str] = Field(
        None, alias="referencePaths", description="Reference paths"
    )
    area_code: Optional[str] = Field(None, alias="areaCode", description="Area code")


# Properties to receive via API on update
class RSIEventUpdate(RSIEventBase):
    """"""


class RSIEventInDBBase(RSIEventBase):
    id: int = Field(..., alias="id", description="RSI Event ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSIEvent(RSIEventInDBBase):
    rsu_name: str = Field(..., alias="rsuName", description="RSU name")
    rsu_esn: str = Field(..., alias="rsuEsn", description="RSU esn")
    address: str = Field(..., alias="address", description="RSU address")
    event_class: str = Field(..., alias="eventClass", description="Event class")
    event_type: int = Field(..., alias="eventType", description="Event type")
    create_time: datetime = Field(..., alias="createTime", description="Create time")
    country_code: str = Field(..., alias="countryCode", description="Country Code")
    country_name: str = Field(..., alias="countryName", description="Country Name")
    province_code: str = Field(..., alias="provinceCode", description="Province Code")
    province_name: str = Field(..., alias="provinceName", description="Province Name")
    city_code: str = Field(..., alias="cityCode", description="City Code")
    city_name: str = Field(..., alias="cityName", description="City Name")
    area_code: str = Field(..., alias="areaCode", description="Area Code")
    area_name: str = Field(..., alias="areaName", description="Area Name")
    alert_id: str = Field(..., alias="alertID", description="Alert id")
    duration: int = Field(..., alias="duration", description="Duration")
    event_status: bool = Field(..., alias="eventStatus", description="Event status")
    timestamp: str = Field(..., alias="timestamp", description="Timestamp")
    event_source: str = Field(..., alias="eventSource", description="Event source")
    event_confidence: float = Field(..., alias="eventConfidence", description="Event confidence")
    event_position: Optional[Dict[str, Any]] = Field(
        None, alias="eventPosition", description="Event position"
    )
    event_radius: Optional[float] = Field(None, alias="eventRadius", description="Event radius")
    event_description: Optional[str] = Field(
        None, alias="eventDescription", description="Event description"
    )
    event_priority: Optional[int] = Field(
        None, alias="eventPriority", description="Event priority"
    )
    reference_paths: Optional[str] = Field(
        None, alias="referencePaths", description="Reference paths"
    )


class RSIEvents(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSIEvent] = Field(..., alias="data", description="Data")
