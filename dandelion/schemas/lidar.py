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


# Shared properties
class LidarBase(BaseModel):
    """"""


# Properties to receive via API on creation
class LidarCreate(BaseModel):
    sn: str = Field(..., alias="sn", description="Lidar SN")
    name: str = Field(..., alias="name", description="Lidar Name")
    lidar_ip: Optional[str] = Field(None, alias="lidarIP", description="Lidar IP")
    lng: str = Field(..., alias="lng", description="Longitude")
    lat: str = Field(..., alias="lat", description="Latitude")
    elevation: str = Field(..., alias="elevation", description="Elevation")
    towards: str = Field(..., alias="towards", description="Towards")
    point: str = Field(..., alias="point", description="point")
    pole: str = Field(..., alias="pole", description="pole")
    rsu_id: Optional[int] = Field(None, alias="rsuId", description="RSU ID")
    desc: Optional[str] = Field("", alias="desc", description="Description")
    ws_url: Optional[str] = Field("", alias="wsUrl", description="websocket url")


class LidarEnabledUpdate(BaseModel):
    enabled: bool = Field(..., alias="enabled", description="enabled")


# Properties to receive via API on update
class LidarUpdate(LidarBase):
    sn: str = Field(..., alias="sn", description="Lidar SN")
    name: str = Field(..., alias="name", description="Lidar Name")
    lidar_ip: Optional[str] = Field(None, alias="lidarIP", description="Lidar IP")
    lng: str = Field(..., alias="lng", description="Longitude")
    lat: str = Field(..., alias="lat", description="Latitude")
    elevation: str = Field(..., alias="elevation", description="Elevation")
    towards: str = Field(..., alias="towards", description="Towards")
    point: str = Field(..., alias="point", description="point")
    pole: str = Field(..., alias="pole", description="pole")
    rsu_id: Optional[int] = Field(None, alias="rsuId", description="RSU ID")
    desc: Optional[str] = Field("", alias="desc", description="Description")
    ws_url: Optional[str] = Field("", alias="wsUrl", description="websocket url")


class LidarInDBBase(LidarBase):
    id: int = Field(..., alias="id", description="Lidar ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class Lidar(LidarInDBBase):
    sn: str = Field(..., alias="sn", description="Lidar SN")
    name: str = Field(..., alias="name", description="Lidar Name")
    lidar_ip: str = Field(..., alias="lidarIP", description="Lidar IP")
    lng: str = Field(..., alias="lng", description="Longitude")
    lat: str = Field(..., alias="lat", description="Latitude")
    elevation: str = Field(..., alias="elevation", description="Elevation")
    towards: str = Field(..., alias="towards", description="Towards")
    online_status: bool = Field(..., alias="onlineStatus", description="Online Status")
    enabled: bool = Field(..., alias="enabled", description="enabled")
    point: str = Field(..., alias="point", description="point")
    pole: str = Field(..., alias="pole", description="pole")
    rsu_id: int = Field(..., alias="rsuId", description="RSU ID")
    rsu_name: str = Field(..., alias="rsuName", description="RSU Name")
    country_code: str = Field(..., alias="countryCode", description="Country Code")
    country_name: str = Field(..., alias="countryName", description="Country Name")
    province_code: str = Field(..., alias="provinceCode", description="Province Code")
    province_name: str = Field(..., alias="provinceName", description="Province Name")
    city_code: str = Field(..., alias="cityCode", description="City Code")
    city_name: str = Field(..., alias="cityName", description="City Name")
    area_code: str = Field(..., alias="areaCode", description="Area Code")
    area_name: str = Field(..., alias="areaName", description="Area Name")
    desc: str = Field(..., alias="desc", description="Description")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")
    ws_url: Optional[str] = Field("", alias="wsUrl", description="websocket url")


class Lidars(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[Lidar] = Field(..., alias="data", description="Data")
