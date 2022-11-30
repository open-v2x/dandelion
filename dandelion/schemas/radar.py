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
class RadarBase(BaseModel):
    """"""


# Properties to receive via API on creation
class RadarCreate(BaseModel):
    sn: str = Field(..., alias="sn", description="Radar SN")
    name: str = Field(..., alias="name", description="Radar Name")
    radar_ip: Optional[str] = Field(None, alias="radarIP", description="Radar IP")
    lng: str = Field(..., alias="lng", description="Longitude")
    lat: str = Field(..., alias="lat", description="Latitude")
    elevation: str = Field(..., alias="elevation", description="Elevation")
    towards: str = Field(..., alias="towards", description="Towards")
    rsu_id: Optional[int] = Field(None, alias="rsuId", description="RSU ID")
    desc: Optional[str] = Field("", alias="desc", description="Description")


# Properties to receive via API on update
class RadarUpdate(RadarBase):
    sn: str = Field(..., alias="sn", description="Radar SN")
    name: str = Field(..., alias="name", description="Radar Name")
    radar_ip: Optional[str] = Field(None, alias="radarIP", description="Radar IP")
    lng: str = Field(..., alias="lng", description="Longitude")
    lat: str = Field(..., alias="lat", description="Latitude")
    elevation: str = Field(..., alias="elevation", description="Elevation")
    towards: str = Field(..., alias="towards", description="Towards")
    rsu_id: Optional[int] = Field(None, alias="rsuId", description="RSU ID")
    desc: Optional[str] = Field("", alias="desc", description="Description")


class RadarInDBBase(RadarBase):
    id: int = Field(..., alias="id", description="Radar ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class Radar(RadarInDBBase):
    sn: str = Field(..., alias="sn", description="Radar SN")
    name: str = Field(..., alias="name", description="Radar Name")
    radar_ip: str = Field(..., alias="radarIP", description="Radar IP")
    lng: str = Field(..., alias="lng", description="Longitude")
    lat: str = Field(..., alias="lat", description="Latitude")
    elevation: str = Field(..., alias="elevation", description="Elevation")
    towards: str = Field(..., alias="towards", description="Towards")
    status: bool = Field(..., alias="status", description="Status")
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
    intersection_code: str = Field(..., alias="intersectionCode", description="Intersection Code")
    intersection_name: str = Field(..., alias="intersectionName", description="Intersection Name")
    desc: str = Field(..., alias="desc", description="Description")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")


class Radars(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[Radar] = Field(..., alias="data", description="Data")
